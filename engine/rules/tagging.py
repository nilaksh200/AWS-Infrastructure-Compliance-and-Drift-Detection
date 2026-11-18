from __future__ import annotations

from typing import Dict, List, Optional

from engine.collector import CollectedS3State
from engine.models import CheckResult, CheckStatus, SecurityBaseline
from engine.rules.base import BaseRule


class S3RequiredTagsRule(BaseRule):
    """
    Checks that all required governance and security tags exist on the S3 bucket and match expected values.
    """

    check_id = "S3_REQUIRED_TAGS"
    property_name = "required_tags"

    def evaluate(self, baseline: SecurityBaseline, collected: CollectedS3State) -> CheckResult:
        expected: Dict[str, str] = baseline.required_tags

        if collected.tags_error:
            err = collected.tags_error
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
                    explanation=f"Cannot check tags: target bucket does not exist ({msg}).",
                )

            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=None,
                status=CheckStatus.ERROR,
                error_code=code,
                explanation=f"Operational error checking bucket tags: {msg}",
            )

        observed_tags = collected.tags or {}
        missing_keys: List[str] = []
        mismatched: List[str] = []

        for req_k, req_v in expected.items():
            if req_k not in observed_tags:
                missing_keys.append(req_k)
            elif observed_tags[req_k] != req_v:
                mismatched.append(f"{req_k} (expected '{req_v}', observed '{observed_tags[req_k]}')")

        if not missing_keys and not mismatched:
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=observed_tags,
                status=CheckStatus.COMPLIANT,
                explanation="All required governance tags are present and match baseline definitions.",
            )
        else:
            issues = []
            if missing_keys:
                issues.append(f"missing tags: {', '.join(missing_keys)}")
            if mismatched:
                issues.append(f"tag value mismatches: {', '.join(mismatched)}")
            return CheckResult(
                check_id=self.check_id,
                resource_id=baseline.bucket_arn,
                property_name=self.property_name,
                expected_value=expected,
                observed_value=observed_tags,
                status=CheckStatus.NON_COMPLIANT,
                explanation=f"Tagging drift detected: {'; '.join(issues)}.",
            )
