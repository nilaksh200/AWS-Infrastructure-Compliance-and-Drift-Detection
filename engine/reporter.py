from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union

from engine.models import CheckStatus, ComplianceReport


class ComplianceReporter:
    """
    Renders compliance reports to human-readable terminal text and machine-readable JSON.
    """

    STATUS_ICONS = {
        CheckStatus.COMPLIANT: "[PASS]",
        CheckStatus.NON_COMPLIANT: "[FAIL]",
        CheckStatus.ERROR: "[ERR ]",
    }

    @classmethod
    def to_json(cls, report: ComplianceReport, indent: int = 2) -> str:
        """Serializes report to structured JSON format."""
        return json.dumps(report.to_dict(), indent=indent)

    @classmethod
    def save_json(cls, report: ComplianceReport, file_path: Union[str, Path], indent: int = 2) -> Path:
        """
        Saves report as formatted JSON to a specified local file path.
        Validates target path and creates parent directories if necessary.
        """
        target = Path(file_path)
        if target.is_dir():
            raise IsADirectoryError(f"Target path is an existing directory, not a file: {target}")

        try:
            if target.parent:
                target.parent.mkdir(parents=True, exist_ok=True)
            content = cls.to_json(report, indent=indent)
            target.write_text(content, encoding="utf-8")
        except Exception as e:
            raise OSError(f"Failed to write report to '{target}': {e}") from e

        return target

    @classmethod
    def to_terminal(cls, report: ComplianceReport) -> str:
        """Renders formatted ASCII table and summary for CLI output."""
        lines = []
        lines.append("=" * 80)
        lines.append("  INFRASTRUCTURE COMPLIANCE & DRIFT DETECTION AUDIT REPORT")
        lines.append("=" * 80)
        lines.append(f"Resource ARN:  {report.resource_id}")
        lines.append(f"Timestamp:     {report.timestamp}")
        lines.append("-" * 80)

        # Header
        col_id = "CHECK ID"
        col_prop = "PROPERTY"
        col_status = "STATUS"
        col_exp = "EXPECTED"
        col_obs = "OBSERVED"
        lines.append(f"{col_id:<30} {col_status:<10} {col_exp:<12} {col_obs:<12}")
        lines.append("-" * 80)

        for res in report.results:
            icon = cls.STATUS_ICONS.get(res.status, "[UNK ]")
            status_str = f"{icon} {res.status.value}"
            exp_str = str(res.expected_value) if res.expected_value is not None else "N/A"
            obs_str = str(res.observed_value) if res.observed_value is not None else (res.error_code or "N/A")

            # Truncate if long
            if len(exp_str) > 12:
                exp_str = exp_str[:9] + "..."
            if len(obs_str) > 12:
                obs_str = obs_str[:9] + "..."

            lines.append(f"{res.check_id:<30} {status_str:<10} {exp_str:<12} {obs_str:<12}")
            lines.append(f"  Explanation: {res.explanation}")
            lines.append("")

        lines.append("=" * 80)
        lines.append("  AUDIT SUMMARY")
        lines.append("=" * 80)
        lines.append(f"Total Evaluated Checks:  {report.total_checks}")
        lines.append(f"Compliant:               {report.compliant_count}")
        lines.append(f"Non-Compliant (Drift):   {report.non_compliant_count}")
        lines.append(f"Operational Errors:      {report.error_count}")

        if report.is_fully_compliant:
            verdict = "COMPLIANT - All security baselines match live AWS state."
        elif report.error_count > 0:
            verdict = "INCOMPLETE / ERRORS - One or more checks failed due to operational or permission issues."
        else:
            verdict = "DRIFT DETECTED - Configuration deviations require investigation."

        lines.append(f"Overall Posture:         {verdict}")
        lines.append("=" * 80)
        return "\n".join(lines)
