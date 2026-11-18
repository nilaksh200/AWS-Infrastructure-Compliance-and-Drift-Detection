from engine.evaluator import ComplianceEvaluator
from engine.models import CheckStatus
from engine.rules.encryption import S3DefaultEncryptionRule
from engine.rules.public_access_block import S3BlockPublicAclsRule
from engine.rules.versioning import S3VersioningRule
from tests.conftest import make_client_error


def test_access_denied_classified_as_error(baseline, compliant_state):
    compliant_state.public_access_block_error = make_client_error("AccessDenied", "User not authorized", 403)
    rule = S3BlockPublicAclsRule()
    res = rule.evaluate(baseline, compliant_state)

    assert res.status == CheckStatus.ERROR
    assert res.error_code == "AccessDenied"
    assert "operational error" in res.explanation.lower()


def test_missing_bucket_error(baseline, compliant_state):
    compliant_state.encryption_error = make_client_error("NoSuchBucket", "Bucket does not exist", 404)
    rule = S3DefaultEncryptionRule()
    res = rule.evaluate(baseline, compliant_state)

    assert res.status == CheckStatus.ERROR
    assert res.error_code == "NoSuchBucket"
    assert "target bucket does not exist" in res.explanation.lower()


def test_network_connection_error(baseline, compliant_state):
    compliant_state.versioning_error = ConnectionResetError("Connection reset by peer")
    rule = S3VersioningRule()
    res = rule.evaluate(baseline, compliant_state)

    assert res.status == CheckStatus.ERROR
    assert res.error_code == "ConnectionResetError"


def test_partial_scan_one_error_others_continue(baseline, compliant_state):
    # Public Access Block has an AccessDenied error, but Encryption, Versioning, Tags succeed
    compliant_state.public_access_block = None
    compliant_state.public_access_block_error = make_client_error("AccessDenied", "Forbidden", 403)

    evaluator = ComplianceEvaluator()
    report = evaluator.evaluate(baseline, compliant_state)

    # 4 PAB checks fail with ERROR, 3 remaining checks are COMPLIANT
    assert report.total_checks == 7
    assert report.error_count == 4
    assert report.compliant_count == 3
    assert report.non_compliant_count == 0
    assert report.is_fully_compliant is False

    # Verify that encryption and versioning ran properly despite PAB error
    enc_results = [r for r in report.results if r.check_id == "S3_ENCRYPTION_ALGORITHM"]
    assert len(enc_results) == 1
    assert enc_results[0].status == CheckStatus.COMPLIANT


def test_partial_scan_unhandled_rule_exception_does_not_abort_evaluator(baseline, compliant_state):
    class BrokenRule:
        check_id = "BROKEN_RULE"
        property_name = "broken"

        def evaluate(self, b, c):
            raise RuntimeError("Unexpected internal crash")

    evaluator = ComplianceEvaluator(rules=[BrokenRule(), S3DefaultEncryptionRule()])  # type: ignore
    report = evaluator.evaluate(baseline, compliant_state)

    assert report.total_checks == 2
    assert report.error_count == 1
    assert report.compliant_count == 1
    assert report.results[0].status == CheckStatus.ERROR
    assert report.results[0].error_code == "RuntimeError"
    assert report.results[1].status == CheckStatus.COMPLIANT
