from engine.models import CheckStatus
from engine.rules.encryption import S3DefaultEncryptionRule
from engine.rules.public_access_block import (
    S3BlockPublicAclsRule,
    S3BlockPublicPolicyRule,
    S3IgnorePublicAclsRule,
    S3RestrictPublicBucketsRule,
)
from engine.rules.tagging import S3RequiredTagsRule
from engine.rules.versioning import S3VersioningRule
from tests.conftest import make_client_error


# 1. Independent Public Access Block failures
def test_pab_block_public_acls_drift(baseline, compliant_state):
    compliant_state.public_access_block["BlockPublicAcls"] = False
    rule = S3BlockPublicAclsRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert res.observed_value is False
    assert "drift" in res.explanation.lower()


def test_pab_ignore_public_acls_drift(baseline, compliant_state):
    compliant_state.public_access_block["IgnorePublicAcls"] = False
    rule = S3IgnorePublicAclsRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert res.observed_value is False


def test_pab_block_public_policy_drift(baseline, compliant_state):
    compliant_state.public_access_block["BlockPublicPolicy"] = False
    rule = S3BlockPublicPolicyRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert res.observed_value is False


def test_pab_restrict_public_buckets_drift(baseline, compliant_state):
    compliant_state.public_access_block["RestrictPublicBuckets"] = False
    rule = S3RestrictPublicBucketsRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert res.observed_value is False


def test_pab_configuration_absent_drift(baseline, compliant_state):
    compliant_state.public_access_block = None
    compliant_state.public_access_block_error = make_client_error(
        "NoSuchPublicAccessBlockConfiguration", "No configuration found", 404
    )
    rule = S3BlockPublicAclsRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert "not present" in res.explanation.lower()


# 2. Encryption failures
def test_encryption_missing_drift(baseline, compliant_state):
    compliant_state.encryption = None
    compliant_state.encryption_error = make_client_error(
        "ServerSideEncryptionConfigurationNotFoundError", "Encryption not set", 404
    )
    rule = S3DefaultEncryptionRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert "NOT configured" in res.explanation


def test_encryption_wrong_algorithm_drift(baseline, compliant_state):
    compliant_state.encryption = {
        "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}}]
    }
    rule = S3DefaultEncryptionRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert res.observed_value == "aws:kms"
    assert "drift" in res.explanation.lower()


def test_encryption_empty_rules_drift(baseline, compliant_state):
    compliant_state.encryption = {"Rules": []}
    rule = S3DefaultEncryptionRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert "No encryption rules found" in res.explanation


# 3. Versioning failures
def test_versioning_suspended_drift(baseline, compliant_state):
    compliant_state.versioning = {"Status": "Suspended"}
    rule = S3VersioningRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert res.observed_value == "Suspended"
    assert "drift" in res.explanation.lower()


def test_versioning_unconfigured_drift(baseline, compliant_state):
    compliant_state.versioning = {}
    rule = S3VersioningRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert "never been enabled" in res.explanation.lower()


# 4. Tagging failures
def test_tagging_missing_tag_drift(baseline, compliant_state):
    compliant_state.tags = {
        "Project": "idps-compliance",
        "Environment": "dev",
        # ManagedBy is missing
    }
    rule = S3RequiredTagsRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert "missing tags: ManagedBy" in res.explanation


def test_tagging_mismatched_value_drift(baseline, compliant_state):
    compliant_state.tags = {
        "Project": "idps-compliance",
        "Environment": "prod",  # expected dev
        "ManagedBy": "Terraform",
    }
    rule = S3RequiredTagsRule()
    res = rule.evaluate(baseline, compliant_state)
    assert res.status == CheckStatus.NON_COMPLIANT
    assert "tag value mismatches" in res.explanation
