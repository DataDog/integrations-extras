import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.wayfinder import WayfinderCheck

from .common import MOCK_INSTANCE

EXPECTED_METRICS = {
    "wayfinder.workqueue.unfinished_work_seconds",
    "wayfinder.workqueue.retries.count",
    "wayfinder.workqueue.queue_duration_seconds.bucket",
    "wayfinder.workqueue.queue_duration_seconds.sum",
    "wayfinder.workqueue.queue_duration_seconds.count",
    "wayfinder.workqueue.depth",
    "wayfinder.workqueue.adds_total.count",
    "wayfinder.controller_runtime.reconcile_total.count",
    "wayfinder.controller_runtime.reconcile_errors_total.count",
    "wayfinder.controller_runtime.reconcile_time_seconds.bucket",
    "wayfinder.controller_runtime.reconcile_time_seconds.sum",
    "wayfinder.controller_runtime.reconcile_time_seconds.count",
    "wayfinder.controller_runtime.max_concurrent_reconciles",
    "wayfinder.controller_runtime.active_workers",
}


@pytest.mark.unit
def test_config():
    with pytest.raises(ConfigurationError):
        WayfinderCheck('wayfinder', {}, [{}])

    # this should not fail
    WayfinderCheck('wayfinder', {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_service_check(aggregator):
    check = WayfinderCheck('wayfinder', {}, [MOCK_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_INSTANCE)
        aggregator.assert_service_check()


@pytest.mark.unit
def test_mock_assert_metrics(dd_run_check, aggregator, check, mock_metrics):
    dd_run_check(check)
    for metric_name in EXPECTED_METRICS:
        aggregator.assert_metric(metric_name)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
