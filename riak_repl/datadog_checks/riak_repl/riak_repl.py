import json
import unicodedata

from requests.exceptions import ConnectionError, Timeout
from six import iteritems

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException


class RiakReplCheck(AgentCheck):

    REPL_STATS = {
        "server_bytes_sent",
        "server_bytes_recv",
        "server_connects",
        "server_connect_errors",
        "server_fullsyncs",
        "client_bytes_sent",
        "client_bytes_recv",
        "client_connects",
        "client_connect_errors",
        "client_redirect",
        "objects_dropped_no_clients",
        "objects_dropped_no_leader",
        "objects_sent",
        "objects_forwarded",
        "elections_elected",
        "elections_leader_changed",
        "rt_source_errors",
        "rt_sink_errors",
        "rt_dirty",
        "realtime_send_kbps",
        "realtime_recv_kbps",
        "fullsync_send_kbps",
        "fullsync_recv_kbps",
    }

    REALTIME_QUEUE_STATS = {"percent_bytes_used", "bytes", "max_bytes", "overload_drops"}

    REALTIME_QUEUE_STATS_CONSUMERS = {"pending", "unacked", "drops", "errs"}

    REALTIME_SOURCE_CONN = {"hb_rtt", "sent_seq", "objects"}

    REALTIME_SINK_CONN = {"deactivated", "source_drops", "expect_seq", "acked_seq", "pending"}

    FULLSYNC_COORDINATOR = {
        "queued",
        "in_progress",
        "waiting_for_retry",
        "starting",
        "successful_exits",
        "error_exits",
        "retry_exits",
        "soft_retry_exits",
        "busy_nodes",
        "fullsyncs_completed",
        "last_fullsync_duration",
    }

    def check(self, instance):
        url = instance.get('url', '')
        connected_clusters = instance.get('connected_clusters', '')
        tags = instance.get('tags', [])

        if not url:
            raise CheckException("Configuration error, please fix conf.yaml")

        try:
            r = self.http.get(url)
        except Timeout:
            raise CheckException('URL: {} timed out after {} seconds.'.format(url, self.http.options['timeout']))
        except ConnectionError as e:
            raise CheckException(e)

        if r.status_code != 200:
            raise CheckException('Invalid Status Code, {} returned a status of {}.'.format(url, r.status_code))

        try:
            stats = json.loads(r.text)
        except ValueError:
            raise CheckException('{} returned an unserializable payload'.format(url))

        cluster = stats['cluster_name']

        for key, val in iteritems(stats):
            if key in self.REPL_STATS:
                self.safe_submit_metric("riak_repl." + key, val, tags=tags + ['cluster:%s' % cluster])

        if stats['realtime_started'] is not None:
            for key, val in iteritems(stats['realtime_queue_stats']):
                if key in self.REALTIME_QUEUE_STATS:
                    self.safe_submit_metric(
                        "riak_repl.realtime_queue_stats." + key, val, tags=tags + ['cluster:%s' % cluster]
                    )

        for c in connected_clusters:

            if stats['fullsync_enabled'] is not None:
                if self.exists(stats['fullsync_coordinator'], [c]):
                    for key, val in iteritems(stats['fullsync_coordinator'][c]):
                        if key in self.FULLSYNC_COORDINATOR:
                            self.safe_submit_metric(
                                "riak_repl.fullsync_coordinator." + key, val, tags=tags + ['cluster:%s' % c]
                            )

            if stats['realtime_started'] is not None:
                if self.exists(stats['sources'], ['source_stats', 'rt_source_connected_to']):
                    for key, val in iteritems(stats['sources']['source_stats']['rt_source_connected_to']):
                        if key in self.REALTIME_SOURCE_CONN:
                            self.safe_submit_metric(
                                "riak_repl.realtime_source.connected." + key, val, tags=tags + ['cluster:%s' % c]
                            )

                if self.exists(stats['realtime_queue_stats'], ['consumers', c]):
                    for key, val in iteritems(stats['realtime_queue_stats']['consumers'][c]):
                        if key in self.REALTIME_QUEUE_STATS_CONSUMERS:
                            self.safe_submit_metric(
                                "riak_repl.realtime_queue_stats.consumers." + key, val, tags=tags + ['cluster:%s' % c]
                            )

            if (
                self.exists(stats['sinks'], ['sink_stats', 'rt_sink_connected_to'])
                and type(stats['sinks']['sink_stats']['rt_sink_connected_to']) is dict
            ):
                for key, val in iteritems(stats['sinks']['sink_stats']['rt_sink_connected_to']):
                    if key in self.REALTIME_SINK_CONN:
                        self.safe_submit_metric(
                            "riak_repl.realtime_sink.connected." + key, val, tags=tags + ['cluster:%s' % c]
                        )

    def safe_submit_metric(self, name, value, tags=None):
        tags = [] if tags is None else tags
        try:
            self.gauge(name, float(value), tags=tags)
            return
        except ValueError:
            self.log.debug("metric name %s cannot be converted to a float: %s", name, value)

        try:
            self.gauge(name, unicodedata.numeric(value), tags=tags)
            return
        except (TypeError, ValueError):
            self.log.debug("metric name %s cannot be converted to a float even using unicode tools: %s", name, value)

    def exists(self, obj, nest):
        _key = nest.pop(0)
        if _key in obj:
            return self.exists(obj[_key], nest) if nest else obj[_key]
