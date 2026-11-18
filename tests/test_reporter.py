import json

from engine.models import CheckResult, CheckStatus, ComplianceReport
from engine.reporter import ComplianceReporter


def test_reporter_terminal_and_json():
    res1 = CheckResult("C1", "arn", "p1", True, True, CheckStatus.COMPLIANT, explanation="OK")
    res2 = CheckResult("C2", "arn", "p2", True, False, CheckStatus.NON_COMPLIANT, explanation="Drift")
    report = ComplianceReport(resource_id="arn:aws:s3:::my-bucket", results=[res1, res2])

    term_out = ComplianceReporter.to_terminal(report)
    assert "INFRASTRUCTURE COMPLIANCE & DRIFT DETECTION AUDIT REPORT" in term_out
    assert "DRIFT DETECTED" in term_out
    assert "arn:aws:s3:::my-bucket" in term_out
    assert "[PASS] COMPLIANT" in term_out
    assert "[FAIL] NON_COMPLIANT" in term_out

    json_out = ComplianceReporter.to_json(report)
    parsed = json.loads(json_out)
    assert parsed["resource_id"] == "arn:aws:s3:::my-bucket"
    assert parsed["summary"]["total"] == 2
    assert parsed["summary"]["compliant"] == 1
    assert parsed["summary"]["non_compliant"] == 1
    assert parsed["summary"]["is_fully_compliant"] is False
    assert len(parsed["results"]) == 2


def test_reporter_save_json_valid(tmp_path):
    res = CheckResult("C1", "arn", "p1", True, True, CheckStatus.COMPLIANT, explanation="OK")
    report = ComplianceReport(resource_id="arn:aws:s3:::my-bucket", results=[res])

    dest = tmp_path / "subdir" / "audit_report.json"
    saved_path = ComplianceReporter.save_json(report, dest)

    assert saved_path == dest
    assert dest.exists()

    content = json.loads(dest.read_text(encoding="utf-8"))
    assert content["resource_id"] == "arn:aws:s3:::my-bucket"
    assert content["summary"]["total"] == 1
    assert content["results"][0]["check_id"] == "C1"
    assert content["results"][0]["status"] == "COMPLIANT"


def test_reporter_save_json_invalid_directory(tmp_path):
    import pytest

    res = CheckResult("C1", "arn", "p1", True, True, CheckStatus.COMPLIANT)
    report = ComplianceReport(resource_id="arn:aws:s3:::my-bucket", results=[res])

    # Target is an existing directory, not a file
    with pytest.raises(IsADirectoryError, match="Target path is an existing directory"):
        ComplianceReporter.save_json(report, tmp_path)


def test_cli_output_argument_success(tmp_path):
    from engine.main import main

    report_file = tmp_path / "reports" / "mock_scan.json"
    exit_code = main(["--mock", "--output", str(report_file)])

    assert exit_code == 0
    assert report_file.exists()

    data = json.loads(report_file.read_text(encoding="utf-8"))
    assert data["resource_id"] == "arn:aws:s3:::idps-compliance-dev-640110193463-ap-south-1"
    assert data["summary"]["total"] == 7
    assert data["summary"]["compliant"] == 7
    assert data["summary"]["is_fully_compliant"] is True


def test_cli_output_argument_invalid_path(tmp_path, capsys):
    from engine.main import main

    # Passing directory instead of file path to --output
    exit_code = main(["--mock", "--output", str(tmp_path)])

    assert exit_code == 2
    captured = capsys.readouterr()
    assert "Error saving report" in captured.err
