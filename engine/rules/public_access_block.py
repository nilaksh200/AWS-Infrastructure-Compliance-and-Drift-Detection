from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError

from engine.collector import CollectedS3State
from engine.models import CheckResult, CheckStatus, SecurityBaseline
from engine.rules.base import BaseRule


class _AbstractPABRule(BaseRule):
    """Base class for the 4 public access block settings."""

    pab_key: str = ""

    def evaluate(self, baseline: SecurityBaseline, collected: CollectedS3State) -> CheckResult:
        expected = getattr(baseline, self.property_name.lower()) if hasattr(baseline, self.property_name.lower()) else True

        # Check for errors during collection
        if collected.public_access_block_error:
            err = collected.public_access_block_error
            code, msg = self.parse_client_error(err)

            # If NoSuchPublicAccessBlockConfiguration, the setting is absent/disabled -> NON_COMPLIANT
            if code in ("NoSuchPublicAccessBlockConfiguration", "404"):
                return CheckResult(
                    check_id=self.check_id,
                    resource_id=baseline.bucket_arn,
                    property_name=self.property_name,
                    expected_value=expected,
                    observed_value=False,
                    status=CheckStatus.NON_COMPLIANT,
                    error_code=code,
                    explanation=f"Public Access Block configuration is not present on bucket '{baseline.bucket_name}'.",
                )

            # Check if bucket itself is missing
            if code in ("NoSuchBucket", "NotFound"):
                return CheckResult(
                    check_id=self.check_id,
                    resource_id=baseline.bucket_arn,
                    property_name=self.property_name,
                    expected_value=expected,
                    observed_value=None,
                    status=CheckStatus.ERROR,
                    error_code=code,
                    explanation=f"Cannot check Public Access Block: target bucket does not exist ({msg}).",
                )

            # Operational/authorization error
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=None,
                status=CheckStatus.ERROR,
                error_code=code,
                explanation=f"Operational error checking Public Access Block: {msg}",
            )

        # Inspect collected settings
        pab_conf = collected.public_access_block or {}
        observed: Any = pab_conf.get(self.pab_key)

        if observed is None:
            # Setting missing in config
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=None,
                status=CheckStatus.NON_COMPLIANT,
                explanation=f"{self.property_name} is missing or undefined in bucket PublicAccessBlockConfiguration.",
            )

        if bool(observed) == bool(expected):
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=bool(observed),
                status=CheckStatus.COMPLIANT,
                explanation=f"{self.property_name} is properly enforced as {observed}.",
            )
        else:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=bool(observed),
                status=CheckStatus.NON_COMPLIANT,
                explanation=f"Configuration drift: {self.property_name} is {observed}, but expected {expected}.",
            )


class S3BlockPublicAclsRule(_AbstractPABRule):
    check_id = "S3_PAB_BLOCK_PUBLIC_ACLS"
    property_name = "block_public_acls"
    pab_key = "BlockPublicAcls"


class S3IgnorePublicAclsRule(_AbstractPABRule):
    check_id = "S3_PAB_IGNORE_PUBLIC_ACLS"
    property_name = "ignore_public_acls"
    pab_key = "IgnorePublicAcls"


class S3BlockPublicPolicyRule(_AbstractPABRule):
    check_id = "S3_PAB_BLOCK_PUBLIC_POLICY"
    property_name = "block_public_policy"
    pab_key = "BlockPublicPolicy"


class S3RestrictPublicBucketsRule(_AbstractPABRule):
    check_id = "S3_PAB_RESTRICT_PUBLIC_BUCKETS"
    property_name = "restrict_public_buckets"
    pab_key = "RestrictPublicBuckets"
