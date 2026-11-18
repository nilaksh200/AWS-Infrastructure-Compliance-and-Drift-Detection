from engine.evaluator import ComplianceEvaluator
from engine.models import CheckStatus


def test_all_rules_compliant(baseline, compliant_state):
    evaluator = ComplianceEvaluator()
    report = evaluator.evaluate(baseline, compliant_state)

    assert report.total_checks == 7
    assert report.compliant_count == 7
    assert report.non_compliant_count == 0
    assert report.error_count == 0
    assert report.is_fully_compliant is True

    for result in report.results:
        assert result.status == CheckStatus.COMPLIANT
        assert "properly" in result.explanation.lower() or "active" in result.explanation.lower() or "present" in result.explanation.lower()
