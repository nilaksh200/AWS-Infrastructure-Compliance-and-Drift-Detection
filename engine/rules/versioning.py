from __future__ import annotations

from typing import Optional

from engine.collector import CollectedS3State
from engine.models import CheckResult, CheckStatus, SecurityBaseline
from engine.rules.base import BaseRule


class S3VersioningRule(BaseRule):
    """
    Checks that S3 bucket versioning status matches the baseline ('Enabled').
    """

    check_id = "S3_VERSIONING_STATUS"
    property_name = "versioning_status"

    def evaluate(self, baseline: SecurityBaseline, collected: CollectedS3State) -> CheckResult:
        expected = baseline.versioning_status

        if collected.versioning_error:
            err = collected.versioning_error
            code, msg = self.parse_client_error(err)

            if code in ("NoSuchBucket", "NotFound"):
                return CheckResult(
                    check_id=self.check_id,
                    resource_id=baseline.bucket_arn,
                    property_name=self.property_name,
                    expected_value=expected,
                    observed_value=None,
                    status=CheckStatus.ERROR,
                    error_code=code,
                    explanation=f"Cannot check versioning: target bucket does not exist ({msg}).",
                )

            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=None,
                status=CheckStatus.ERROR,
                error_code=code,
                explanation=f"Operational error checking bucket versioning: {msg}",
            )

        ver_data = collected.versioning or {}
        observed_status: Optional[str] = ver_data.get("Status")

        # If bucket versioning was never enabled, Status key is omitted by AWS API
        if observed_status is None:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value="Disabled/Unconfigured",
                status=CheckStatus.NON_COMPLIANT,
                explanation=f"Versioning has never been enabled on bucket '{baseline.bucket_name}'.",
            )

        if observed_status == expected:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=observed_status,
                status=CheckStatus.COMPLIANT,
                explanation=f"Bucket versioning status is active and verified as '{observed_status}'.",
            )
        else:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=observed_status,
                status=CheckStatus.NON_COMPLIANT,
                explanation=f"Versioning drift detected: observed status '{observed_status}', expected '{expected}'.",
            )
