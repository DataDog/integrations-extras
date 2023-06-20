from typing import Any, Callable, Dict  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.scalr import ScalrCheck

SCALR_ACCOUNT_METRICS = {
    "environments.count",
    "workspaces.count",
    "runs.count",
    "runs.successful",
    "runs.failed",
    "runs.awaiting_confirmation",
    "runs.concurrency",
    "runs.queue_size",
    "quota.max_concurrency",
    "billing.runs.count",
    "billing.run_minutes.count",
    "billing.flex_runs.count",
    "billing.flex_run_minutes.count",
}

SCALR_ACCOUNTS_RESPONSE = '''
{
    "data": [
        {
          "attributes": {},
          "id": "acc-test",
          "relationships": {},
          "type": "accounts"
        }
    ]
}
'''


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
        'http://acc_name.localhost/api/iacp/v3/accounts/acc-test/metrics',
        text=SCALR_METRICS_RESPONSE,
    )

    requests_mock.get(
        'http://acc_name.localhost/api/iacp/v3/accounts?filter[name]=acc_name',
        text=SCALR_ACCOUNTS_RESPONSE,
    )

    check = ScalrCheck('scalr', {}, [instance])
    dd_run_check(check)

    for metric_name in SCALR_ACCOUNT_METRICS:
        aggregator.assert_metric('scalr.' + metric_name)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check('scalr.can_connect', ScalrCheck.OK)


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance, requests_mock):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    requests_mock.get(
        'http://acc_name.localhost/api/iacp/v3/accounts?filter[name]=acc_name',
        text=SCALR_ACCOUNTS_RESPONSE,
    )
    requests_mock.get('http://acc_name.localhost/api/iacp/v3/accounts/acc-test/metrics')
    check = ScalrCheck('scalr', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('scalr.can_connect', ScalrCheck.CRITICAL)
