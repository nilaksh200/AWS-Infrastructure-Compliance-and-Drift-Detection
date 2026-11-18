from engine.models import CheckResult, CheckStatus, ComplianceReport, SecurityBaseline


def test_check_result_to_dict():
    res = CheckResult(
        check_id="TEST_CHECK",
        resource_id="arn:aws:s3:::test-bucket",
        property_name="test_prop",
        expected_value=True,
        observed_value=True,
        status=CheckStatus.COMPLIANT,
        explanation="Test explanation",
    )
    d = res.to_dict()
    assert d["check_id"] == "TEST_CHECK"
    assert d["status"] == "COMPLIANT"
    assert d["expected_value"] is True
    assert d["observed_value"] is True
    assert d["error_code"] is None
    assert "timestamp" in d


def test_compliance_report_properties():
    res1 = CheckResult("C1", "arn", "p1", True, True, CheckStatus.COMPLIANT)
    res2 = CheckResult("C2", "arn", "p2", True, False, CheckStatus.NON_COMPLIANT)
    res3 = CheckResult("C3", "arn", "p3", True, None, CheckStatus.ERROR, error_code="AccessDenied")

    report = ComplianceReport(resource_id="arn", results=[res1, res2, res3])

    assert report.total_checks == 3
    assert report.compliant_count == 1
    assert report.non_compliant_count == 1
    assert report.error_count == 1
    assert report.is_fully_compliant is False

    d = report.to_dict()
    assert d["summary"]["total"] == 3
    assert d["summary"]["compliant"] == 1
    assert d["summary"]["is_fully_compliant"] is False


def test_compliance_report_fully_compliant():
    res1 = CheckResult("C1", "arn", "p1", True, True, CheckStatus.COMPLIANT)
    res2 = CheckResult("C2", "arn", "p2", True, True, CheckStatus.COMPLIANT)
    report = ComplianceReport(resource_id="arn", results=[res1, res2])
    assert report.is_fully_compliant is True
