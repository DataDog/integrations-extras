
import pytest


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance)
    metrics = [
        'resin.connection_count',
        'resin.connection_active_count',
        'resin.connection_idle_count',
        'resin.connection_create_count',
        'resin.max_connections',
        'resin.max_overflow_connections',
        'resin.max_create_connections',
        'resin.thread_active_count',
        'resin.thread_count',
        'resin.thread_idle_count',
        'resin.thread_max',
        'resin.thread_wait_count'
    ]
    for metric in metrics:
        aggregator.assert_metric(metric)
