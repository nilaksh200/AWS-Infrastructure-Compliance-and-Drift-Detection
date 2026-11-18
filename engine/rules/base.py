from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from botocore.exceptions import ClientError

from engine.collector import CollectedS3State
from engine.models import CheckResult, CheckStatus, SecurityBaseline


class BaseRule(ABC):
    """Abstract base class for independent compliance checks."""

    @property
    @abstractmethod
    def check_id(self) -> str:
        pass

    @property
    @abstractmethod
    def property_name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, baseline: SecurityBaseline, collected: CollectedS3State) -> CheckResult:
        pass

    @staticmethod
    def parse_client_error(error: Exception) -> Tuple[Optional[str], str]:
        """Extracts standard AWS error code and message."""
        if isinstance(error, ClientError):
            err_dict = error.response.get("Error", {})
            return err_dict.get("Code"), err_dict.get("Message", str(error))
        return type(error).__name__, str(error)

    @classmethod
    def handle_missing_bucket_error(
        cls, check_id: str, property_name: str, baseline: SecurityBaseline, error: Exception
    ) -> CheckResult:
        code, msg = cls.parse_client_error(error)
        if code in ("NoSuchBucket", "404", "NotFound"):
            status = CheckStatus.ERROR
            explanation = f"Target bucket '{baseline.bucket_name}' does not exist in AWS: {msg}"
        elif code in ("AccessDenied", "403"):
            status = CheckStatus.ERROR
            explanation = f"Access denied reading bucket '{baseline.bucket_name}': {msg}"
        else:
            status = CheckStatus.ERROR
            explanation = f"Operational error querying bucket '{baseline.bucket_name}': {msg}"

        return CheckResult(
            check_id=check_id,
            resource_id=baseline.bucket_arn,
            property_name=property_name,
            expected_value=None,
            observed_value=None,
            status=status,
            error_code=code,
            explanation=explanation,
        )
