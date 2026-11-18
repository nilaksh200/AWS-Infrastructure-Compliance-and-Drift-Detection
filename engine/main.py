from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from engine.baseline_loader import BaselineLoader
from engine.collector import CollectedS3State, S3Collector
from engine.evaluator import ComplianceEvaluator
from engine.models import CheckStatus, SecurityBaseline
from engine.reporter import ComplianceReporter


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m engine.main",
        description="Policy-Driven Infrastructure Compliance and Drift Detection Engine.",
    )
    parser.add_argument(
        "--format",
        choices=["terminal", "json"],
        default="terminal",
        help="Report output format (default: terminal).",
    )
    parser.add_argument(
        "--terraform-dir",
        type=Path,
        default=None,
        help="Path to terraform directory containing outputs (default: ./terraform).",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Safe offline validation mode. Uses synthetic state without contacting AWS.",
    )
    parser.add_argument(
        "--mock-drift",
        action="store_true",
        help="Safe offline mode simulating configuration drift without contacting AWS.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Optional file path to save the scan report as JSON for documentation.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=None,
        help="Alias for --output.",
    )
    return parser


def build_mock_state(baseline: SecurityBaseline, simulate_drift: bool = False) -> CollectedS3State:
    """Creates synthetic collected state for safe offline demonstration."""
    if not simulate_drift:
        return CollectedS3State(
            bucket_name=baseline.bucket_name,
            bucket_exists=True,
            public_access_block={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
            encryption={
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "AES256"
                        }
                    }
                ]
            },
            versioning={"Status": "Enabled"},
            tags={
                "Project": "idps-compliance",
                "Environment": "dev",
                "ManagedBy": "Terraform",
            },
        )
    else:
        return CollectedS3State(
            bucket_name=baseline.bucket_name,
            bucket_exists=True,
            public_access_block={
                "BlockPublicAcls": False,  # Drift
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
            encryption={
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "aws:kms"  # Drift
                        }
                    }
                ]
            },
            versioning={"Status": "Suspended"},  # Drift
            tags={
                "Project": "idps-compliance",
                "Environment": "dev",
                # "ManagedBy" missing (Drift)
            },
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    # 1. Determine baseline
    try:
        if args.mock or args.mock_drift:
            baseline = SecurityBaseline(
                bucket_name="idps-compliance-dev-640110193463-ap-south-1",
                bucket_arn="arn:aws:s3:::idps-compliance-dev-640110193463-ap-south-1",
                aws_region="ap-south-1",
                server_side_encryption_algorithm="AES256",
                versioning_status="Enabled",
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True,
                required_tags={
                    "Project": "idps-compliance",
                    "Environment": "dev",
                    "ManagedBy": "Terraform",
                },
            )
        else:
            baseline = BaselineLoader.from_terraform_cli(terraform_dir=args.terraform_dir)
    except Exception as e:
        print(f"Error loading baseline: {e}", file=sys.stderr)
        return 2

    # 2. Evaluate
    evaluator = ComplianceEvaluator()
    if args.mock or args.mock_drift:
        collected = build_mock_state(baseline, simulate_drift=args.mock_drift)
        report = evaluator.evaluate(baseline, collected)
    else:
        report = evaluator.evaluate_live(baseline)

    # 3. Format and Output
    if args.format == "json":
        output_text = ComplianceReporter.to_json(report)
    else:
        output_text = ComplianceReporter.to_terminal(report)

    output_dest = args.output or args.output_file
    if output_dest:
        try:
            ComplianceReporter.save_json(report, output_dest)
        except Exception as e:
            print(f"Error saving report to '{output_dest}': {e}", file=sys.stderr)
            return 2

    print(output_text)

    # Return status code based on compliance
    if report.error_count > 0:
        return 2
    if report.non_compliant_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
