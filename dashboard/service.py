from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine.baseline_loader import BaselineLoader, BaselineLoaderError
from engine.collector import S3Collector
from engine.evaluator import ComplianceEvaluator
from engine.models import ComplianceReport, SecurityBaseline
from engine.reporter import ComplianceReporter

logger = logging.getLogger(__name__)


class ReportNotFoundError(Exception):
    """Raised when a requested compliance report file does not exist."""
    pass


class ReportCorruptedError(Exception):
    """Raised when a compliance report file contains invalid JSON or schema."""
    pass


class ScanAlreadyInProgressError(Exception):
    """Raised when a live scan is requested while another scan is executing."""
    pass


class ComplianceService:
    """
    Service layer bridging the dashboard API with the core compliance engine.
    Ensures safe, read-only evaluation, strict file path validation, and non-blocking I/O.
    """

    ALLOWED_REPORT_TYPES: Dict[str, str] = {
        "live": "live-compliance.json",
        "simulated": "simulated-drift.json",
    }

    def __init__(
        self,
        reports_dir: Optional[Path] = None,
        terraform_dir: Optional[Path] = None,
        evaluator: Optional[ComplianceEvaluator] = None,
        collector: Optional[S3Collector] = None,
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.reports_dir = (reports_dir or (base_dir / "reports")).resolve()
        self.terraform_dir = (terraform_dir or (base_dir / "terraform")).resolve()
        self.evaluator = evaluator or ComplianceEvaluator()
        self.collector = collector
        self._scan_lock = asyncio.Lock()

    def get_report_path(self, report_type: str) -> Path:
        """
        Resolves and validates the report file path using a fixed whitelist.
        Guards strictly against arbitrary file access and path traversal.
        """
        if report_type not in self.ALLOWED_REPORT_TYPES:
            raise ValueError(
                f"Invalid report type '{report_type}'. Allowed: {list(self.ALLOWED_REPORT_TYPES.keys())}"
            )

        filename = self.ALLOWED_REPORT_TYPES[report_type]
        resolved_path = (self.reports_dir / filename).resolve()

        # Path traversal guard
        if not resolved_path.is_relative_to(self.reports_dir):
            raise ValueError("Path traversal violation detected.")

        return resolved_path

    def read_report(self, report_type: str) -> Dict[str, Any]:
        """
        Safely reads and parses one of the whitelisted report files.
        """
        path = self.get_report_path(report_type)
        if not path.exists() or not path.is_file():
            raise ReportNotFoundError(f"Report '{report_type}' does not exist at {path.name}.")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict) or "results" not in data or "summary" not in data:
                raise ReportCorruptedError(f"Report '{report_type}' has invalid structure.")

            return data
        except json.JSONDecodeError as e:
            raise ReportCorruptedError(f"Report '{report_type}' contains invalid JSON: {e}") from e

    def get_baseline(self) -> SecurityBaseline:
        """
        Loads the expected security baseline from Terraform outputs, falling back
        to the standard security baseline definition if Terraform CLI is unavailable.
        """
        try:
            return BaselineLoader.from_terraform_cli(self.terraform_dir)
        except Exception as e:
            logger.info("Falling back to standard baseline: %s", e)
            return SecurityBaseline(
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

    def get_status(self) -> Dict[str, Any]:
        """
        Returns safe system metadata without exposing credentials or environment variables.
        """
        baseline = self.get_baseline()
        live_path = self.get_report_path("live")
        sim_path = self.get_report_path("simulated")

        return {
            "project_name": "Policy-Driven Infrastructure Compliance and Drift Detection",
            "resource_id": baseline.bucket_arn,
            "bucket_name": baseline.bucket_name,
            "aws_region": baseline.aws_region,
            "baseline_checks_count": 7,
            "scan_in_progress": self._scan_lock.locked(),
            "live_report_exists": live_path.exists() and live_path.is_file(),
            "simulated_report_exists": sim_path.exists() and sim_path.is_file(),
            "expected_baseline": baseline.to_dict(),
        }

    def compare_reports(self) -> Dict[str, Any]:
        """
        Compares the saved live report against the simulated drift report on a per-check basis.
        """
        live = self.read_report("live")
        simulated = self.read_report("simulated")

        live_results = {r["check_id"]: r for r in live.get("results", [])}
        sim_results = {r["check_id"]: r for r in simulated.get("results", [])}

        all_check_ids = list(dict.fromkeys(list(live_results.keys()) + list(sim_results.keys())))

        checks_comparison: List[Dict[str, Any]] = []
        matching_count = 0
        drift_count = 0

        for check_id in all_check_ids:
            l_check = live_results.get(check_id)
            s_check = sim_results.get(check_id)

            l_val = l_check.get("observed_value") if l_check else None
            s_val = s_check.get("observed_value") if s_check else None
            l_stat = l_check.get("status") if l_check else "MISSING"
            s_stat = s_check.get("status") if s_check else "MISSING"

            expected = l_check.get("expected_value") if l_check else (
                s_check.get("expected_value") if s_check else None
            )
            prop = l_check.get("property_name") if l_check else (
                s_check.get("property_name") if s_check else check_id
            )

            differs = (l_val != s_val) or (l_stat != s_stat)
            if differs:
                drift_count += 1
            else:
                matching_count += 1

            checks_comparison.append({
                "check_id": check_id,
                "property_name": prop,
                "expected_value": expected,
                "live_value": l_val,
                "live_status": l_stat,
                "simulated_value": s_val,
                "simulated_status": s_stat,
                "differs": differs,
                "explanation": (
                    s_check.get("explanation")
                    if (differs and s_check)
                    else (l_check.get("explanation") if l_check else "")
                ),
            })

        return {
            "resource_id": live.get("resource_id", simulated.get("resource_id", "unknown")),
            "live_timestamp": live.get("timestamp"),
            "simulated_timestamp": simulated.get("timestamp"),
            "summary": {
                "total_checks": len(all_check_ids),
                "matching_checks": matching_count,
                "drifted_checks": drift_count,
                "live_summary": live.get("summary", {}),
                "simulated_summary": simulated.get("summary", {}),
            },
            "checks": checks_comparison,
        }

    async def run_live_scan(self) -> Dict[str, Any]:
        """
        Triggers a fresh, read-only live scan against AWS in a worker thread.
        Guarded against concurrent execution and strictly overwrites only the live report.
        """
        if self._scan_lock.locked():
            raise ScanAlreadyInProgressError("A live scan is already in progress.")

        async with self._scan_lock:
            baseline = self.get_baseline()
            evaluator = self.evaluator
            collector = self.collector

            def _sync_scan() -> ComplianceReport:
                return evaluator.evaluate_live(baseline, collector=collector)

            try:
                report = await asyncio.to_thread(_sync_scan)
            except Exception as e:
                logger.error("Live AWS scan failed: %s", type(e).__name__)
                # Do not leak AWS stack traces or internal secrets
                raise RuntimeError(f"Live AWS scan failed due to operational error: {type(e).__name__}") from e

            # Save strictly to live report file; NEVER touch simulated drift report
            live_path = self.get_report_path("live")
            ComplianceReporter.save_json(report, live_path)

            return report.to_dict()
