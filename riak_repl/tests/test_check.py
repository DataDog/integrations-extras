import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.riak_repl import RiakReplCheck

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
def test_check(aggregator, dd_environment):
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
            "riak_repl.realtime_queue_stats.consumers.unacked",
            "riak_repl.realtime_queue_stats.consumers.errs",
            "riak_repl.realtime_queue_stats.consumers.drops",
            "riak_repl.realtime_queue_stats.consumers.pending",
            "riak_repl.fullsync_coordinator.queued",
            "riak_repl.fullsync_coordinator.in_progress",
            "riak_repl.fullsync_coordinator.waiting_for_retry",
            "riak_repl.fullsync_coordinator.starting",
            "riak_repl.fullsync_coordinator.successful_exits",
            "riak_repl.fullsync_coordinator.error_exits",
            "riak_repl.fullsync_coordinator.retry_exits",
            "riak_repl.fullsync_coordinator.soft_retry_exits",
            "riak_repl.fullsync_coordinator.busy_nodes",
            "riak_repl.fullsync_coordinator.fullsyncs_completed",
            "riak_repl.fullsync_coordinator.last_fullsync_duration",
            "riak_repl.realtime_source.connected.hb_rtt",
            "riak_repl.realtime_source.connected.objects",
            "riak_repl.realtime_sink.connected.deactivated",
            "riak_repl.realtime_sink.connected.source_drops",
            "riak_repl.realtime_sink.connected.pending",
        ]
    }

    c = RiakReplCheck('riak_repl', init_config, {}, None)
    c.check(INSTANCE)

    for key in init_config['keys']:
        aggregator.assert_metric(key, tags=[], at_least=0)

    # Assert coverage for this check on this instance
    aggregator.assert_all_metrics_covered()
    # TODO: there are metrics missing in metadata.csv
    missing_metrics = [
        'riak_repl.realtime_queue_stats.consumers.drops',
        'riak_repl.realtime_queue_stats.consumers.errs',
        'riak_repl.realtime_queue_stats.consumers.pending',
        'riak_repl.realtime_queue_stats.consumers.unacked',
        'riak_repl.realtime_sink.connected.deactivated',
        'riak_repl.realtime_sink.connected.pending',
        'riak_repl.realtime_sink.connected.source_drops',
        'riak_repl.realtime_source.connected.hb_rtt',
        'riak_repl.realtime_source.connected.objects',
    ]
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), exclude=missing_metrics)
