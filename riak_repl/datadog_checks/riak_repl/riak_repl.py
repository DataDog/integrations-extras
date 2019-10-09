import json

import requests
from six import iteritems

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException


class RiakReplCheck(AgentCheck):

    REPL_STATS = {
        "server_bytes_sent": "gauge",
        "server_bytes_recv": "gauge",
        "server_connects": "gauge",
        "server_connect_errors": "gauge",
        "server_fullsyncs": "gauge",
        "client_bytes_sent": "gauge",
        "client_bytes_recv": "gauge",
        "client_connects": "gauge",
        "client_connect_errors": "gauge",
        "client_redirect": "gauge",
        "objects_dropped_no_clients": "gauge",
        "objects_dropped_no_leader": "gauge",
        "objects_sent": "gauge",
        "objects_forwarded": "gauge",
        "elections_elected": "gauge",
        "elections_leader_changed": "gauge",
        "rt_source_errors": "gauge",
        "rt_sink_errors": "gauge",
        "rt_dirty": "gauge",
        "realtime_send_kbps": "gauge",
        "realtime_recv_kbps": "gauge",
        "fullsync_send_kbps": "gauge",
        "fullsync_recv_kbps": "gauge",
    }

    REALTIME_QUEUE_STATS = {
        "percent_bytes_used": "gauge",
        "bytes": "gauge",
        "max_bytes": "gauge",
        "overload_drops": "gauge",
    }

    REALTIME_QUEUE_STATS_CONSUMERS = {"pending": "gauge", "unacked": "gauge", "drops": "gauge", "errs": "gauge"}

    REALTIME_SOURCE_CONN = {"hb_rtt": "gauge", "sent_seq": "gauge", "objects": "gauge"}

    REALTIME_SINK_CONN = {
        "deactivated": "gauge",
        "source_drops": "gauge",
        "expect_seq": "gauge",
        "acked_seq": "gauge",
        "pending": "gauge",
    }

    FULLSYNC_COORDINATOR = {
        "queued": "gauge",
        "in_progress": "gauge",
        "waiting_for_retry": "gauge",
        "starting": "gauge",
        "successful_exits": "gauge",
        "error_exits": "gauge",
        "retry_exits": "gauge",
        "soft_retry_exits": "gauge",
        "busy_nodes": "gauge",
        "fullsyncs_completed": "gauge",
        "last_fullsync_duration": "gauge",
    }

    def check(self, instance):
        url = instance.get('url', '')
        connected_clusters = instance.get('connected_clusters', '')
        default_timeout = instance.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))
        tags = instance.get('tags', [])

        if not url:
            raise CheckException("Configuration error, please fix conf.yaml")

        try:
            r = requests.get(url, timeout=timeout)
        except requests.exceptions.Timeout:
            raise CheckException('URL: {} timed out after {} seconds.'.format(url, timeout))
        except requests.exceptions.ConnectionError as e:
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
                self.safe_submit_metric(
                    "riak_repl." + key, val, self.REPL_STATS.get(key), tags=tags + ['cluster:%s' % cluster]
                )

        if stats['realtime_started'] is not None:
            for key, val in iteritems(stats['realtime_queue_stats']):
                if key in self.REALTIME_QUEUE_STATS:
                    self.safe_submit_metric(
                        "riak_repl.realtime_queue_stats." + key,
                        val,
                        self.REALTIME_QUEUE_STATS.get(key),
                        tags=tags + ['cluster:%s' % cluster],
                    )

        for c in connected_clusters:

            if stats['fullsync_enabled'] is not None:
                if self.exists(stats['fullsync_coordinator'], [c]):
                    for key, val in iteritems(stats['fullsync_coordinator'][c]):
                        if key in self.FULLSYNC_COORDINATOR:
                            self.safe_submit_metric(
                                "riak_repl.fullsync_coordinator." + key,
                                val,
                                self.FULLSYNC_COORDINATOR.get(key),
                                tags=tags + ['cluster:%s' % c],
                            )

            if stats['realtime_started'] is not None:
                if self.exists(stats['sources'], ['source_stats', 'rt_source_connected_to']):
                    for key, val in iteritems(stats['sources']['source_stats']['rt_source_connected_to']):
                        if key in self.REALTIME_SOURCE_CONN:
                            self.safe_submit_metric(
                                "riak_repl.realtime_source.connected." + key,
                                val,
                                self.REALTIME_SOURCE_CONN.get(key),
                                tags=tags + ['cluster:%s' % c],
                            )

                if self.exists(stats['realtime_queue_stats'], ['consumers', c]):
                    for key, val in iteritems(stats['realtime_queue_stats']['consumers'][c]):
                        if key in self.REALTIME_QUEUE_STATS_CONSUMERS:
                            self.safe_submit_metric(
                                "riak_repl.realtime_queue_stats.consumers." + key,
                                val,
                                self.REALTIME_QUEUE_STATS_CONSUMERS.get(key),
                                tags=tags + ['cluster:%s' % c],
                            )

            if self.exists(stats['sinks'], ['sink_stats', 'rt_sink_connected_to']):
                for key, val in iteritems(stats['sinks']['sink_stats']['rt_sink_connected_to']):
                    if key in self.REALTIME_SINK_CONN:
                        self.safe_submit_metric(
                            "riak_repl.realtime_sink.connected." + key,
                            val,
                            self.REALTIME_SINK_CONN.get(key),
                            tags=tags + ['cluster:%s' % c],
                        )

    def safe_submit_metric(self, name, value, type, tags=None):
        type = "gauge" if type is None else type
        tags = [] if tags is None else tags

        if type == "gauge":
            try:
                self.gauge(name, float(value), tags=tags)
                return
            except ValueError:
                self.log.debug("metric name {0} cannot be converted to a float: {1}".format(name, value))
                pass

    def exists(self, obj, nest):
        _key = nest.pop(0)
        if _key in obj:
            return self.exists(obj[_key], nest) if nest else obj[_key]
