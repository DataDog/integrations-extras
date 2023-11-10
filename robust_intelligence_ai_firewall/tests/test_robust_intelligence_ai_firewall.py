import os
from typing import Any, Callable, Dict  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev import get_here
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.robust_intelligence_ai_firewall import RobustIntelligenceAiFirewallCheck

METRICS = [
    "robust_intelligence_ai_firewall.firewall_requests.count",
    "robust_intelligence_ai_firewall.rule_evaluated.count",
]


def test_check(dd_run_check, aggregator, instance, mock_http_response):
    fixtures_path = os.path.join(get_here(), 'fixtures', 'firewall_metrics.txt')
    mock_http_response(file_path=fixtures_path)

    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = RobustIntelligenceAiFirewallCheck('robust_intelligence_ai_firewall', {}, [instance])
    dd_run_check(check)

    for metric in METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_metric_type=False)
