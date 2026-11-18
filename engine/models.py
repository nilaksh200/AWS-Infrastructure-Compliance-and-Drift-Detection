from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class CheckStatus(str, Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    ERROR = "ERROR"


@dataclass
class CheckResult:
    check_id: str
    resource_id: str
    property_name: str
    expected_value: Any
    observed_value: Any
    status: CheckStatus
    error_code: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    explanation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "check_id": self.check_id,
            "resource_id": self.resource_id,
            "property_name": self.property_name,
            "expected_value": self.expected_value,
            "observed_value": self.observed_value,
            "status": self.status.value if isinstance(self.status, CheckStatus) else str(self.status),
            "error_code": self.error_code,
            "timestamp": self.timestamp,
            "explanation": self.explanation,
        }


@dataclass
class SecurityBaseline:
    bucket_name: str
    bucket_arn: str
    aws_region: str
    server_side_encryption_algorithm: str = "AES256"
    versioning_status: str = "Enabled"
    block_public_acls: bool = True
    block_public_policy: bool = True
    ignore_public_acls: bool = True
    restrict_public_buckets: bool = True
    required_tags: Dict[str, str] = field(default_factory=lambda: {
        "Project": "idps-compliance",
        "Environment": "dev",
        "ManagedBy": "Terraform",
    })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket_name": self.bucket_name,
            "bucket_arn": self.bucket_arn,
            "aws_region": self.aws_region,
            "server_side_encryption_algorithm": self.server_side_encryption_algorithm,
            "versioning_status": self.versioning_status,
            "block_public_acls": self.block_public_acls,
            "block_public_policy": self.block_public_policy,
            "ignore_public_acls": self.ignore_public_acls,
            "restrict_public_buckets": self.restrict_public_buckets,
            "required_tags": self.required_tags,
        }


@dataclass
class ComplianceReport:
    resource_id: str
    results: List[CheckResult] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def total_checks(self) -> int:
        return len(self.results)

    @property
    def compliant_count(self) -> int:
        return sum(1 for r in self.results if r.status == CheckStatus.COMPLIANT)

    @property
    def non_compliant_count(self) -> int:
        return sum(1 for r in self.results if r.status == CheckStatus.NON_COMPLIANT)

    @property
    def error_count(self) -> int:
        return sum(1 for r in self.results if r.status == CheckStatus.ERROR)

    @property
    def is_fully_compliant(self) -> bool:
        return self.total_checks > 0 and self.compliant_count == self.total_checks

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "resource_id": self.resource_id,
            "summary": {
                "total": self.total_checks,
                "compliant": self.compliant_count,
                "non_compliant": self.non_compliant_count,
                "errors": self.error_count,
                "is_fully_compliant": self.is_fully_compliant,
            },
            "results": [r.to_dict() for r in self.results],
        }
