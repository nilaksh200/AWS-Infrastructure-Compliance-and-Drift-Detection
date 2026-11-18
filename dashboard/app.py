from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from dashboard.service import (
    ComplianceService,
    ReportCorruptedError,
    ReportNotFoundError,
    ScanAlreadyInProgressError,
)


def create_app(service: Optional[ComplianceService] = None) -> FastAPI:
    """
    Application factory for the Compliance and Drift Detection Dashboard API.
    """
    compliance_service = service or ComplianceService()

    app = FastAPI(
        title="Infrastructure Compliance & Drift Detection API",
        description="Local REST API for monitoring Terraform S3 baseline compliance and detecting drift.",
        version="1.0.0",
    )

    @app.exception_handler(ReportNotFoundError)
    async def handle_report_not_found(request, exc: ReportNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ReportCorruptedError)
    async def handle_report_corrupted(request, exc: ReportCorruptedError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Compliance report file is corrupted or formatted incorrectly."},
        )

    @app.exception_handler(ScanAlreadyInProgressError)
    async def handle_scan_conflict(request, exc: ScanAlreadyInProgressError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ValueError)
    async def handle_value_error(request, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / "static"
    templates_dir = base_dir / "templates"
    index_file = templates_dir / "index.html"

    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def get_index() -> HTMLResponse:
        """Serves the dashboard HTML single-page application."""
        if index_file.exists():
            return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
        # Fallback if template file is absent
        fallback = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IDPS Infrastructure Compliance Dashboard</title>
</head>
<body>
  <h1>IDPS Infrastructure Compliance Dashboard</h1>
  <p>Backend API active</p>
</body>
</html>"""
        return HTMLResponse(content=fallback)

    @app.get("/api/status")
    async def get_status() -> Dict[str, Any]:
        """Returns safe project metadata and baseline configuration."""
        return compliance_service.get_status()

    @app.get("/api/reports/latest-live")
    async def get_latest_live_report() -> Dict[str, Any]:
        """Returns the last saved verified live AWS scan report."""
        return compliance_service.read_report("live")

    @app.get("/api/reports/simulated")
    async def get_simulated_report() -> Dict[str, Any]:
        """Returns the simulated drift audit report."""
        return compliance_service.read_report("simulated")

    @app.get("/api/reports/compare")
    async def compare_reports() -> Dict[str, Any]:
        """Compares live and simulated reports and identifies drifted properties."""
        return compliance_service.compare_reports()

    @app.post("/api/scan/live")
    async def trigger_live_scan() -> Dict[str, Any]:
        """Triggers a fresh, read-only live scan against AWS."""
        try:
            return await compliance_service.run_live_scan()
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=str(e)) from e

    @app.get("/api/reports/download/{report_type}")
    async def download_report(report_type: str):
        """Downloads either the live or simulated JSON report with strict path whitelist enforcement."""
        if report_type not in compliance_service.ALLOWED_REPORT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid report type '{report_type}'. Allowed values: ['live', 'simulated'].",
            )

        try:
            target_path = compliance_service.get_report_path(report_type)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not target_path.exists() or not target_path.is_file():
            raise HTTPException(
                status_code=404,
                detail=f"Report file '{target_path.name}' not found.",
            )

        return FileResponse(
            path=target_path,
            media_type="application/json",
            filename=target_path.name,
        )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("dashboard.app:app", host="127.0.0.1", port=8000, reload=True)
