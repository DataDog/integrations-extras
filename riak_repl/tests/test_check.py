import pytest

from datadog_checks.riak_repl import RiakReplCheck
from datadog_checks.errors import CheckException

from .common import INSTANCE

def test_config():
    c = RiakReplCheck('riak_repl', {}, {}, None)

    # Empty instance
    instance = {}
    with pytest.raises(CheckException):
        c.check(instance)

    # Timeout
    instance = {'url': 'http://foobar'}
    with pytest.raises(CheckException):
        c.check(instance)

    # Statuscode
    instance = {'url': 'https://google.com/404'}
    with pytest.raises(CheckException):
        c.check(instance)

    # Decode Error
    instance = {'url': 'https://google.com'}
    with pytest.raises(CheckException):
        c.check(instance)


@pytest.mark.integration
def test_service_check(aggregator, dd_environment):
    init_config = {
        'keys': [
            "riak_repl.server_bytes_sent",
            "riak_repl.server_bytes_recv",
            "riak_repl.server_connects",
            "riak_repl.server_connect_errors",
            "riak_repl.server_fullsyncs",
            "riak_repl.client_bytes_sent",
            "riak_repl.client_bytes_recv",
            "riak_repl.client_connects",
            "riak_repl.client_connect_errors",
            "riak_repl.client_redirect",
            "riak_repl.objects_dropped_no_clients",
            "riak_repl.objects_dropped_no_leader",
            "riak_repl.objects_sent",
            "riak_repl.objects_forwarded",
            "riak_repl.elections_elected",
            "riak_repl.elections_leader_changed",
            "riak_repl.rt_source_errors",
            "riak_repl.rt_sink_errors",
            "riak_repl.rt_dirty",
            "riak_repl.realtime_send_kbps",
            "riak_repl.realtime_recv_kbps",
            "riak_repl.fullsync_send_kbps",
            "riak_repl.fullsync_recv_kbps",
            "riak_repl.realtime_queue_stats.percent_bytes_used",
            "riak_repl.realtime_queue_stats.bytes",
            "riak_repl.realtime_queue_stats.max_bytes",
            "riak_repl.realtime_queue_stats.overload_drops",
            "riak_repl.fullsync_coordinator.riak_west_1.queued",
            "riak_repl.fullsync_coordinator.riak_west_1.in_progress",
            "riak_repl.fullsync_coordinator.riak_west_1.waiting_for_retry",
            "riak_repl.fullsync_coordinator.riak_west_1.starting",
            "riak_repl.fullsync_coordinator.riak_west_1.successful_exits",
            "riak_repl.fullsync_coordinator.riak_west_1.error_exits",
            "riak_repl.fullsync_coordinator.riak_west_1.retry_exits",
            "riak_repl.fullsync_coordinator.riak_west_1.soft_retry_exits",
            "riak_repl.fullsync_coordinator.riak_west_1.busy_nodes",
            "riak_repl.fullsync_coordinator.riak_west_1.fullsyncs_completed"
        ]
    }

    c = RiakReplCheck('riak_repl', init_config, {}, None)

    c.check(INSTANCE)
    for key in init_config['keys']:
        aggregator.assert_metric(key, tags=[])

    # Assert coverage for this check on this instance
    aggregator.assert_all_metrics_covered()
