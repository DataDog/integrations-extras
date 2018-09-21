import json
import requests
import unicodedata

from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException


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

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        url = instance.get('url', '')
        default_timeout = self.init_config.get('default_timeout', 5)
        timeout = float(instance.get('timeout', default_timeout))
        tags = instance.get('tags', [])

        if not url:
            raise CheckException("Configuration error, please fix conf.yaml")

        try:
            r = requests.get(url)
        except requests.exceptions.Timeout as e:
            raise CheckException('URL: {0} timed out after {1} \
                                 seconds.'.format(url, timeout))
        except requests.exceptions.ConnectionError as e:
            raise CheckException(e)

        if r.status_code != 200:
            raise CheckException('Invalid Status Code, {0} returned a status \
                                 of {1}.'.format(url, r.status_code))

        try:
            stats = json.loads(r.text)
        except ValueError as e:
            raise CheckException('{0} returned an unserializable \
                                 payload'.format(url))

        for k in self.REPL_STATS:
            if k in stats:
                self.safe_submit_metric("riak_repl." + k, stats[k], tags=tags)

        for k in self.REALTIME_QUEUE_STATS:
            if k in stats['realtime_queue_stats']:
                self.safe_submit_metric("riak_repl.realtime_queue_stats."
                                        + k, stats['realtime_queue_stats'][k],
                                        tags=tags)

    def safe_submit_metric(self, name, value, tags=None):
        tags = [] if tags is None else tags
        try:
            self.gauge(name, float(value), tags=tags)
            return
        except ValueError:
            self.log.debug("metric name {0} cannot be converted to a \
                           float: {1}".format(name, value))
            pass

        try:
            self.gauge(name, unicodedata.numeric(value), tags=tags)
            return
        except (TypeError, ValueError):
            self.log.debug("metric name {0} cannot be converted to a \
                           float even using unicode tools:\
                           {1}".format(name, value))
            pass
