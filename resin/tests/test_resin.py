import pytest

from datadog_checks.dev.jmx import JVM_E2E_METRICS
from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance)
    metrics = [
        'resin.thread_pool.thread_active_count',
        'resin.thread_pool.thread_count',
        'resin.thread_pool.thread_idle_count',
        'resin.thread_pool.thread_max',
        'resin.thread_pool.thread_wait_count',
        'resin.connection_pool.connection_active_count',
        'resin.connection_pool.connection_count',
        'resin.connection_pool.connection_create_count',
        'resin.connection_pool.connection_idle_count',
        'resin.connection_pool.max_connections',
        'resin.connection_pool.max_create_connections',
        'resin.connection_pool.max_overflow_connections',
    ]
    for metric in metrics + JVM_E2E_METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), exclude=JVM_E2E_METRICS)

    # aggregator.assert_service_check('resin.can_connect') ToDo, uncoment when this is available for jmx checks
