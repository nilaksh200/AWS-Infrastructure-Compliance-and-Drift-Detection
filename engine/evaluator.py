from __future__ import annotations

from typing import List, Optional

from engine.collector import CollectedS3State, S3Collector
from engine.models import CheckResult, CheckStatus, ComplianceReport, SecurityBaseline
from engine.rules import ALL_RULES, BaseRule


class ComplianceEvaluator:
    """
    Orchestrates compliance evaluation by comparing the desired security baseline
    against collected live AWS state across all defined rules.
    """

    def __init__(self, rules: Optional[List[BaseRule]] = None):
        self.rules = rules if rules is not None else ALL_RULES

    def evaluate(self, baseline: SecurityBaseline, collected: CollectedS3State) -> ComplianceReport:
        report = ComplianceReport(resource_id=baseline.bucket_arn)

        for rule in self.rules:
            try:
                result = rule.evaluate(baseline, collected)
            except Exception as e:
                # Catch unexpected rule runtime exceptions so other rules still run
                result = CheckResult(
                    check_id=rule.check_id,
                    resource_id=baseline.bucket_arn,
                    property_name=rule.property_name,
                    expected_value=None,
                    observed_value=None,
                    status=CheckStatus.ERROR,
                    error_code=type(e).__name__,
                    explanation=f"Unhandled exception during rule execution: {e}",
                )
            report.results.append(result)

        return report

    def evaluate_live(
        self, baseline: SecurityBaseline, collector: Optional[S3Collector] = None
    ) -> ComplianceReport:
        """
        Gathers live state via collector and performs evaluation.
        """
        coll = collector or S3Collector(region_name=baseline.aws_region)
        collected_state = coll.collect(baseline.bucket_name)
        return self.evaluate(baseline, collected_state)
