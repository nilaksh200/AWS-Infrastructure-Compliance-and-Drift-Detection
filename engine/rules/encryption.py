from __future__ import annotations

from typing import Any, List, Optional

from engine.collector import CollectedS3State
from engine.models import CheckResult, CheckStatus, SecurityBaseline
from engine.rules.base import BaseRule


class S3DefaultEncryptionRule(BaseRule):
    """
    Checks that S3 bucket default server-side encryption matches the expected algorithm (AES256).
    """

    check_id = "S3_ENCRYPTION_ALGORITHM"
    property_name = "server_side_encryption_algorithm"

    def evaluate(self, baseline: SecurityBaseline, collected: CollectedS3State) -> CheckResult:
        expected = baseline.server_side_encryption_algorithm

        if collected.encryption_error:
            err = collected.encryption_error
            code, msg = self.parse_client_error(err)

            # AWS explicitly confirms no encryption configuration exists -> NON_COMPLIANT
            if code in ("ServerSideEncryptionConfigurationNotFoundError", "404"):
                return CheckResult(
                    check_id=self.check_id,
                    resource_id=baseline.bucket_arn,
                    property_name=self.property_name,
                    expected_value=expected,
                    observed_value=None,
                    status=CheckStatus.NON_COMPLIANT,
                    error_code=code,
                    explanation=f"Default server-side encryption is NOT configured on bucket '{baseline.bucket_name}'.",
                )

            # Missing target bucket
            if code in ("NoSuchBucket", "NotFound"):
                return CheckResult(
                    check_id=self.check_id,
                    resource_id=baseline.bucket_arn,
                    property_name=self.property_name,
                    expected_value=expected,
                    observed_value=None,
                    status=CheckStatus.ERROR,
                    error_code=code,
                    explanation=f"Cannot check encryption: target bucket does not exist ({msg}).",
                )

            # Operational/authorization error (AccessDenied, network timeout)
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=None,
                status=CheckStatus.ERROR,
                error_code=code,
                explanation=f"Operational error checking bucket encryption: {msg}",
            )

        enc_data = collected.encryption or {}
        rules: List[Any] = enc_data.get("Rules", [])
        if not rules:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=None,
                status=CheckStatus.NON_COMPLIANT,
                explanation="No encryption rules found in ServerSideEncryptionConfiguration.",
            )

        first_rule = rules[0]
        default_enc = first_rule.get("ApplyServerSideEncryptionByDefault", {})
        observed_algo = default_enc.get("SSEAlgorithm")

        if observed_algo == expected:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=observed_algo,
                status=CheckStatus.COMPLIANT,
                explanation=f"Default server-side encryption algorithm is properly set to {observed_algo}.",
            )
        else:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=observed_algo,
                status=CheckStatus.NON_COMPLIANT,
                explanation=f"Encryption configuration drift: observed '{observed_algo}', expected '{expected}'.",
            )
