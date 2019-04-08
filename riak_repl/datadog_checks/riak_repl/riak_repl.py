import json
import requests
import unicodedata

from six import iteritems

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException


class RiakReplCheck(AgentCheck):

    REPL_STATS = [
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
        "fullsync_recv_kbps"
    ]

    REALTIME_QUEUE_STATS = [
        "percent_bytes_used",
        "bytes",
        "max_bytes",
        "overload_drops"
    ]

    FULLSYNC_COORDINATOR = [
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
        "last_fullsync_duration"
    ]

    def check(self, instance):
        url = instance.get('url', '')
        default_timeout = instance.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))
        tags = instance.get('tags', [])

        if not url:
            raise CheckException("Configuration error, please fix conf.yaml")

        try:
            r = requests.get(url, timeout=timeout)
        except requests.exceptions.Timeout:
            raise CheckException('URL: {0} timed out after {1} \
                                 seconds.'.format(url, timeout))
        except requests.exceptions.ConnectionError as e:
            raise CheckException(e)

        if r.status_code != 200:
            raise CheckException('Invalid Status Code, {0} returned a status \
                                 of {1}.'.format(url, r.status_code))

        try:
            stats = json.loads(r.text)
        except ValueError:
            raise CheckException('{0} returned an unserializable \
                                 payload'.format(url))

        for key, val in iteritems(stats):
            if key in self.REPL_STATS:
                self.safe_submit_metric("riak_repl." + key, val, tags=tags)

        if stats['realtime_enabled'] is not None:
            for key, val in iteritems(stats['realtime_queue_stats']):
                if key in self.REALTIME_QUEUE_STATS:
                    self.safe_submit_metric("riak_repl.realtime_queue_stats."
                                            + key, val, tags=tags)

        for c in stats['connected_clusters']:
            cluster = c.replace("-", "_")
            if c not in stats['fullsync_coordinator']:
                continue
            for key, val in iteritems(stats['fullsync_coordinator'][c]):
                if key in self.FULLSYNC_COORDINATOR:
                    self.safe_submit_metric("riak_repl.fullsync_coordinator."
                                            + cluster + "." + key,
                                            val, tags=tags)

    def safe_submit_metric(self, name, value, tags=None):
        tags = [] if tags is None else tags
        try:
            self.gauge(name, float(value), tags=tags)
            return
        except ValueError:
            self.log.debug("metric name {0} cannot be converted to a \
                           float: {1}".format(name, value))

        try:
            self.gauge(name, unicodedata.numeric(value), tags=tags)
            return
        except (TypeError, ValueError):
            self.log.debug("metric name {0} cannot be converted to a \
                           float even using unicode tools:\
                           {1}".format(name, value))
