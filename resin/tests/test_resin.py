import pytest


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance)
    metrics = [
        'resin.connection_active_count',
        'resin.connection_idle_count',
        'resin.connection_busy_count_total',
        'resin.connection_new_count_total',
        'resin.max_connections',
        'resin.max_overflow_connections',
        'resin.max_create_connections',
        'resin.thread_active_count',
        'resin.thread_count',
        'resin.thread_idle_count',
        'resin.thread_max',
        'resin.thread_wait_count',
    ]
    for metric in metrics:
        # The metrix are prefixed with jmx because they are the Cluster metrics which do not have an alias
        aggregator.assert_metric('jmx.' + metric)
    # aggregator.assert_service_check('resin.can_connect') ToDo, uncoment when this is available for jmx checks
