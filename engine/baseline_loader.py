from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from engine.models import SecurityBaseline


class BaselineLoaderError(Exception):
    """Raised when the expected security baseline cannot be loaded or validated."""
    pass


class BaselineLoader:
    """
    Loads and normalizes the desired security baseline from Terraform outputs.
    Avoids duplicating values while ensuring explicit, type-checked expected criteria.
    """

    DEFAULT_TERRAFORM_DIR = Path(__file__).resolve().parent.parent / "terraform"

    @classmethod
    def from_terraform_cli(cls, terraform_dir: Optional[Path] = None) -> SecurityBaseline:
        """
        Executes `terraform -chdir=<dir> output -json` to extract current deployment outputs.
        """
        tf_dir = terraform_dir or cls.DEFAULT_TERRAFORM_DIR
        if not tf_dir.exists():
            raise BaselineLoaderError(f"Terraform directory does not exist: {tf_dir}")

        try:
            cmd = ["terraform", f"-chdir={tf_dir}", "output", "-json"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except FileNotFoundError:
            raise BaselineLoaderError("Terraform CLI not found on system PATH.")
        except subprocess.TimeoutExpired:
            raise BaselineLoaderError("Timed out executing 'terraform output -json'.")
        except Exception as e:
            raise BaselineLoaderError(f"Failed to execute terraform output command: {e}")

        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip()
            raise BaselineLoaderError(f"Terraform output command failed with code {result.returncode}: {err}")

        try:
            raw_outputs = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise BaselineLoaderError(f"Failed to parse Terraform output JSON: {e}")

        return cls.from_dict(raw_outputs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SecurityBaseline:
        """
        Parses raw Terraform output dictionary (format: {key: {'value': ...}} or flat {key: value}).
        """
        if not isinstance(data, dict):
            raise BaselineLoaderError(f"Expected dict for baseline outputs, got {type(data).__name__}")

        def get_val(key: str) -> Any:
            if key in data:
                entry = data[key]
                if isinstance(entry, dict) and "value" in entry:
                    return entry["value"]
                return entry
            return None

        bucket_name = get_val("bucket_name")
        if not bucket_name or not isinstance(bucket_name, str):
            raise BaselineLoaderError("Missing or invalid 'bucket_name' in Terraform outputs.")

        bucket_arn = get_val("bucket_arn")
        if not bucket_arn or not isinstance(bucket_arn, str):
            # Construct standard ARN if not explicitly provided
            bucket_arn = f"arn:aws:s3:::{bucket_name}"

        aws_region = get_val("aws_region") or os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
        encryption = get_val("server_side_encryption_algorithm") or "AES256"
        versioning = get_val("versioning_status") or "Enabled"

        return SecurityBaseline(
            bucket_name=bucket_name,
            bucket_arn=bucket_arn,
            aws_region=aws_region,
            server_side_encryption_algorithm=encryption,
            versioning_status=versioning,
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
