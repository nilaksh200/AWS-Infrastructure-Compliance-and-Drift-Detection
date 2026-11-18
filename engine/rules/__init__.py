from engine.rules.base import BaseRule
from engine.rules.encryption import S3DefaultEncryptionRule
from engine.rules.public_access_block import (
    S3BlockPublicAclsRule,
    S3BlockPublicPolicyRule,
    S3IgnorePublicAclsRule,
    S3RestrictPublicBucketsRule,
)
from engine.rules.tagging import S3RequiredTagsRule
from engine.rules.versioning import S3VersioningRule

ALL_RULES = [
    S3BlockPublicAclsRule(),
    S3IgnorePublicAclsRule(),
    S3BlockPublicPolicyRule(),
    S3RestrictPublicBucketsRule(),
    S3DefaultEncryptionRule(),
    S3VersioningRule(),
    S3RequiredTagsRule(),
]

__all__ = [
    "BaseRule",
    "ALL_RULES",
    "S3BlockPublicAclsRule",
    "S3IgnorePublicAclsRule",
    "S3BlockPublicPolicyRule",
    "S3RestrictPublicBucketsRule",
    "S3DefaultEncryptionRule",
    "S3VersioningRule",
    "S3RequiredTagsRule",
]
