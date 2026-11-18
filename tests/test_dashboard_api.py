import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from dashboard.app import create_app
from dashboard.service import (
    ComplianceService,
    ReportCorruptedError,
    ReportNotFoundError,
    ScanAlreadyInProgressError,
)
from engine.models import CheckResult, CheckStatus, ComplianceReport, SecurityBaseline


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


def test_index_placeholder(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "IDPS Infrastructure Compliance Dashboard" in response.text
    assert "Backend API active" in response.text
    assert "checks-table" in response.text
    assert "compare-table" in response.text


def test_static_assets(client: TestClient):
    css_res = client.get("/static/css/dashboard.css")
    assert css_res.status_code == 200
    assert "--bg-primary" in css_res.text

    js_res = client.get("/static/js/app.js")
    assert js_res.status_code == 200
    assert "triggerLiveScan" in js_res.text


def test_status_endpoint(client: TestClient):
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "Policy-Driven Infrastructure Compliance and Drift Detection"
    assert "resource_id" in data
    assert data["baseline_checks_count"] == 7
    assert data["scan_in_progress"] is False
    assert data["live_report_exists"] is True
    assert data["simulated_report_exists"] is True


def test_get_live_report_success(client: TestClient):
    response = client.get("/api/reports/latest-live")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["total"] == 7
    assert data["summary"]["compliant"] == 7
    assert data["summary"]["non_compliant"] == 0
    assert data["summary"]["is_fully_compliant"] is True


def test_get_simulated_report_success(client: TestClient):
    response = client.get("/api/reports/simulated")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["total"] == 7
    assert data["summary"]["compliant"] == 3
    assert data["summary"]["non_compliant"] == 4
    assert data["summary"]["is_fully_compliant"] is False


def test_compare_reports_success(client: TestClient):
    response = client.get("/api/reports/compare")
    assert response.status_code == 200
    data = response.json()

    summary = data["summary"]
    assert summary["total_checks"] == 7
    assert summary["matching_checks"] == 3
    assert summary["drifted_checks"] == 4

    drifted_ids = {c["check_id"] for c in data["checks"] if c["differs"]}
    expected_drifted_ids = {
        "S3_PAB_BLOCK_PUBLIC_ACLS",
        "S3_ENCRYPTION_ALGORITHM",
        "S3_VERSIONING_STATUS",
        "S3_REQUIRED_TAGS",
    }
    assert drifted_ids == expected_drifted_ids


def test_missing_report_returns_404(tmp_path: Path):
    empty_service = ComplianceService(reports_dir=tmp_path)
    app = create_app(service=empty_service)
    test_client = TestClient(app)

    res_live = test_client.get("/api/reports/latest-live")
    assert res_live.status_code == 404
    assert "does not exist" in res_live.json()["detail"]

    res_sim = test_client.get("/api/reports/simulated")
    assert res_sim.status_code == 404

    res_cmp = test_client.get("/api/reports/compare")
    assert res_cmp.status_code == 404


def test_corrupted_report_returns_500(tmp_path: Path):
    bad_file = tmp_path / "live-compliance.json"
    bad_file.write_text("{invalid json", encoding="utf-8")

    service = ComplianceService(reports_dir=tmp_path)
    app = create_app(service=service)
    test_client = TestClient(app)

    res = test_client.get("/api/reports/latest-live")
    assert res.status_code == 500
    assert "corrupted" in res.json()["detail"].lower()


def test_download_report_valid_and_invalid(client: TestClient):
    # Valid live download
    res_live = client.get("/api/reports/download/live")
    assert res_live.status_code == 200
    assert res_live.headers["content-type"] == "application/json"
    assert "live-compliance.json" in res_live.headers.get("content-disposition", "")

    # Valid simulated download
    res_sim = client.get("/api/reports/download/simulated")
    assert res_sim.status_code == 200
    assert res_sim.headers["content-type"] == "application/json"
    assert "simulated-drift.json" in res_sim.headers.get("content-disposition", "")

    # Invalid type
    res_inv = client.get("/api/reports/download/unknown_type")
    assert res_inv.status_code == 400
    assert "Invalid report type" in res_inv.json()["detail"]

    # Path traversal rejection
    res_trav = client.get("/api/reports/download/..%2F..%2Fmain.tf")
    assert res_trav.status_code in (400, 404)


def test_live_scan_success_and_simulated_untouched(tmp_path: Path):
    # Setup initial mock simulated drift report
    sim_file = tmp_path / "simulated-drift.json"
    sim_original_content = json.dumps({"marker": "must_not_be_modified", "summary": {}, "results": []})
    sim_file.write_text(sim_original_content, encoding="utf-8")

    mock_evaluator = MagicMock()
    mock_report = ComplianceReport(
        resource_id="arn:aws:s3:::test-bucket",
        results=[
            CheckResult("TEST_CHECK", "arn:aws:s3:::test-bucket", "test_prop", True, True, CheckStatus.COMPLIANT)
        ],
    )
    mock_evaluator.evaluate_live.return_value = mock_report

    service = ComplianceService(reports_dir=tmp_path, evaluator=mock_evaluator)
    app = create_app(service=service)
    test_client = TestClient(app)

    res = test_client.post("/api/scan/live")
    assert res.status_code == 200
    data = res.json()
    assert data["resource_id"] == "arn:aws:s3:::test-bucket"

    # Verify live report was written
    live_file = tmp_path / "live-compliance.json"
    assert live_file.exists()

    # Crucial assertion: simulated drift report was NOT modified!
    assert sim_file.read_text(encoding="utf-8") == sim_original_content


def test_live_scan_aws_error_handling(tmp_path: Path):
    mock_evaluator = MagicMock()
    mock_evaluator.evaluate_live.side_effect = ConnectionError("Could not connect to AWS endpoint")

    service = ComplianceService(reports_dir=tmp_path, evaluator=mock_evaluator)
    app = create_app(service=service)
    test_client = TestClient(app)

    res = test_client.post("/api/scan/live")
    assert res.status_code == 502
    detail = res.json()["detail"]
    assert "Live AWS scan failed" in detail
    assert "ConnectionError" in detail
    # Ensure no credentials or sensitive internal paths leak
    assert "AWS_SECRET_ACCESS_KEY" not in detail


def test_concurrent_scan_protection(tmp_path: Path):
    import asyncio

    service = ComplianceService(reports_dir=tmp_path)
    # Simulate a scan already locking the service
    asyncio.run(service._scan_lock.acquire())

    app = create_app(service=service)
    test_client = TestClient(app)

    res = test_client.post("/api/scan/live")
    assert res.status_code == 409
    assert "already in progress" in res.json()["detail"]
