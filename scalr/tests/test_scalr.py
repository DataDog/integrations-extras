from typing import Any, Callable, Dict

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.scalr import ScalrCheck

SCALR_ACCOUNT_METRICS = {
    "environments-count": "environments.count",
    "workspaces-count": "workspaces.count",
    "runs-count": "runs.count",
    "runs-successful": "runs.successful",
    "runs-failed": "runs.failed",
    "runs-awaiting-confirmation": "runs.awaiting_confirmation",
    "runs-concurrency": "runs.concurrency",
    "runs-queue-size": "runs.queue_size",
    "quota-max-concurrency": "quota.max_concurrency",
    "billings-runs-count": "billing.runs.count",
    "billings-run-minutes-count": "billing.run_minutes.count",
    "billings-flex-runs-count": "billing.flex_runs.count",
    "billings-flex-runs-minutes-count": "billing.flex_run_minutes.count",
}


def test_check(dd_run_check, aggregator, instance, requests_mock):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    SCALR_METRICS_RESPONSE = '''
    {
      "billings-flex-runs-count": 0,
      "billings-flex-runs-minutes-count": 0,
      "billings-run-minutes-count": 50,
      "billings-runs-count": 10,
      "environments-count": 4,
      "quota-max-concurrency": 10,
      "runs-awaiting-confirmation": 1,
      "runs-concurrency": 0,
      "runs-count": 10,
      "runs-failed": 2,
      "runs-queue-size": 2,
      "runs-successful": 6,
      "workspaces-count": 3
    }'''

    requests_mock.get(
        'http://localhost/api/iacp/v3/integrations/datadog/account/acc-test/metrics',
        text=SCALR_METRICS_RESPONSE,
    )

    check = ScalrCheck('scalr', {}, [instance])
    dd_run_check(check)

    for check_name in ScalrCheck.SCALR_ACCOUNT_METRICS.values():
        aggregator.assert_metric('scalr.' + check_name)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = ScalrCheck('scalr', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('scalr.can_connect', ScalrCheck.CRITICAL)
