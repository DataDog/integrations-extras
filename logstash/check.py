# stdlib
from collections import namedtuple
import urlparse

# 3p
import requests

# project
from checks import AgentCheck
from util import headers

class NodeNotFound(Exception):
    pass

LSInstanceConfig = namedtuple(
    'LSInstanceConfig', [
        'service_check_tags',
        'tags',
        'timeout',
        'url',
    ])

class LSCheck(AgentCheck):
    SERVICE_CHECK_CONNECT_NAME = 'logstash.can_connect'

    DEFAULT_TIMEOUT = 5

    STATS_METRICS = {
        "logstash.jvm.gc.collectors.old.collection_count": ("gauge", "jvm.gc.collectors.old.collection_count"),
        "logstash.jvm.gc.collectors.old.collection_time_in_millis": ("gauge", "jvm.gc.collectors.old.collection_time_in_millis"),
        "logstash.jvm.gc.collectors.young.collection_count": ("gauge", "jvm.gc.collectors.young.collection_count"),
        "logstash.jvm.gc.collectors.young.collection_time_in_millis": ("gauge", "jvm.gc.collectors.young.collection_time_in_millis"),
        "logstash.jvm.mem.heap_committed_in_bytes": ("gauge", "jvm.mem.heap_committed_in_bytes"),
        "logstash.jvm.mem.heap_max_in_bytes": ("gauge", "jvm.mem.heap_max_in_bytes"),
        "logstash.jvm.mem.heap_used_in_bytes": ("gauge", "jvm.mem.heap_used_in_bytes"),
        "logstash.jvm.mem.heap_used_percent": ("gauge", "jvm.mem.heap_used_percent"),
        "logstash.jvm.mem.non_heap_committed_in_bytes": ("gauge", "jvm.mem.non_heap_committed_in_bytes"),
        "logstash.jvm.mem.non_heap_used_in_bytes": ("gauge", "jvm.mem.non_heap_used_in_bytes"),
        "logstash.jvm.mem.pools.old.committed_in_bytes": ("gauge", "jvm.mem.pools.old.committed_in_bytes"),
        "logstash.jvm.mem.pools.old.max_in_bytes": ("gauge", "jvm.mem.pools.old.max_in_bytes"),
        "logstash.jvm.mem.pools.old.peak_max_in_bytes": ("gauge", "jvm.mem.pools.old.peak_max_in_bytes"),
        "logstash.jvm.mem.pools.old.peak_used_in_bytes": ("gauge", "jvm.mem.pools.old.peak_used_in_bytes"),
        "logstash.jvm.mem.pools.old.used_in_bytes": ("gauge", "jvm.mem.pools.old.used_in_bytes"),
        "logstash.jvm.mem.pools.survivor.committed_in_bytes": ("gauge", "jvm.mem.pools.survivor.committed_in_bytes"),
        "logstash.jvm.mem.pools.survivor.max_in_bytes": ("gauge", "jvm.mem.pools.survivor.max_in_bytes"),
        "logstash.jvm.mem.pools.survivor.peak_max_in_bytes": ("gauge", "jvm.mem.pools.survivor.peak_max_in_bytes"),
        "logstash.jvm.mem.pools.survivor.peak_used_in_bytes": ("gauge", "jvm.mem.pools.survivor.peak_used_in_bytes"),
        "logstash.jvm.mem.pools.survivor.used_in_bytes": ("gauge", "jvm.mem.pools.survivor.used_in_bytes"),
        "logstash.jvm.mem.pools.young.committed_in_bytes": ("gauge", "jvm.mem.pools.young.committed_in_bytes"),
        "logstash.jvm.mem.pools.young.max_in_bytes": ("gauge", "jvm.mem.pools.young.max_in_bytes"),
        "logstash.jvm.mem.pools.young.peak_max_in_bytes": ("gauge", "jvm.mem.pools.young.peak_max_in_bytes"),
        "logstash.jvm.mem.pools.young.peak_used_in_bytes": ("gauge", "jvm.mem.pools.young.peak_used_in_bytes"),
        "logstash.jvm.mem.pools.young.used_in_bytes": ("gauge", "jvm.mem.pools.young.used_in_bytes"),
        "logstash.jvm.threads.count": ("gauge", "jvm.threads.count"),
        "logstash.jvm.threads.peak_count": ("gauge", "jvm.threads.peak_count"),
        "logstash.jvm.uptime_in_millis": ("gauge", "jvm.uptime_in_millis"),
        "logstash.pipeline.events.duration_in_millis": ("gauge", "pipeline.events.duration_in_millis"),
        "logstash.pipeline.events.filtered": ("gauge", "pipeline.events.filtered"),
        "logstash.pipeline.events.in": ("gauge", "pipeline.events.in"),
        "logstash.pipeline.events.out": ("gauge", "pipeline.events.out"),
        "logstash.pipeline.reloads.failures": ("gauge", "pipeline.reloads.failures"),
        "logstash.pipeline.reloads.last_error": ("gauge", "pipeline.reloads.last_error"),
        "logstash.pipeline.reloads.successes": ("gauge", "pipeline.reloads.successes"),
        "logstash.process.cpu.load_average.15m": ("gauge", "process.cpu.load_average.15m"),
        "logstash.process.cpu.load_average.1m": ("gauge", "process.cpu.load_average.1m"),
        "logstash.process.cpu.load_average.5m": ("gauge", "process.cpu.load_average.5m"),
        "logstash.process.cpu.percent": ("gauge", "process.cpu.percent"),
        "logstash.process.cpu.total_in_millis": ("gauge", "process.cpu.total_in_millis"),
        "logstash.process.max_file_descriptors": ("gauge", "process.max_file_descriptors"),
        "logstash.process.mem.total_virtual_in_bytes": ("gauge", "process.mem.total_virtual_in_bytes"),
        "logstash.process.open_file_descriptors": ("gauge", "process.open_file_descriptors"),
        "logstash.process.peak_open_file_descriptors": ("gauge", "process.peak_open_file_descriptors"),
        "logstash.reloads.failures": ("gauge", "reloads.failures"),
        "logstash.reloads.successes": ("gauge", "reloads.successes"),
        "logstash.os.cgroup.cpuacct.usage_nanos": ("gauge", "os.cgroup.cpuacct.usage_nanos"),
        "logstash.os.cpu.cfs_period_micros": ("gauge", "os.cpu.cfs_period_micros"),
        "logstash.os.cpu.cfs_quota_micros": ("gauge", "os.cpu.cfs_quota_micros"),
        "logstash.os.cpu.stat.number_of_elasped_periods": ("gauge","os.cpu.stat.number_of_elasped_periods"),
        "logstash.os.cpu.stat.number_of_times_throttled": ("gauge", "os.cpu.stat.number_of_times_throttled"),
        "logstash.os.cpu.stat.time_throttled_nanos": ("gauge", "os.cpu.stat.time_throttled_nanos")
    }
    SOURCE_TYPE_NAME = 'logstash'

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def get_instance_config(self, instance):
        url = instance.get('url')
        if url is None:
            raise Exception("A URL must be specified in the instance")

        # Support URLs that have a path in them from the config, for
        # backwards-compatibility.
        parsed = urlparse.urlparse(url)
        if parsed[2] != "":
            url = "%s://%s" % (parsed[0], parsed[1])
        port = parsed.port
        host = parsed.hostname

        custom_tags = instance.get('tags', [])
        service_check_tags = [
            'host:%s' % host,
            'port:%s' % port
        ]
        service_check_tags.extend(custom_tags)
        # Tag by URL so we can differentiate the metrics
        # from multiple instances
        tags = ['url:%s' % url]
        tags.extend(custom_tags)

        timeout = instance.get('timeout') or self.DEFAULT_TIMEOUT

        config = LSInstanceConfig(
            service_check_tags=service_check_tags,
            tags=tags,
            timeout=timeout,
            url=url,
        )
        return config

    def check(self, instance):
        config = self.get_instance_config(instance)

        # Define parameters (URLs and metrics)
        node_stats_url = "/_node/stats"
        stats_metrics = dict(self.STATS_METRICS)

        # Load node stats data.

        stats_url = urlparse.urljoin(config.url, node_stats_url)
        stats_data = self._get_data(stats_url, config)
        metric_hostname = None
        metrics_tags = list(config.tags)
        for metric, desc in stats_metrics.iteritems():
                self._process_metric(
                    stats_data, metric, *desc,
                    tags=metrics_tags, hostname=metric_hostname
                )

        # If we're here we did not have any LS conn issues
        self.service_check(
            self.SERVICE_CHECK_CONNECT_NAME,
            AgentCheck.OK,
            tags=config.service_check_tags
        )

    def _get_data(self, url, config, send_sc=True):
        """ Hit a given URL and return the parsed json
        """
        try:
            resp = requests.get(
                url,
                timeout=config.timeout,
                headers=headers(self.agentConfig)
            )
            resp.raise_for_status()
        except Exception as e:
            if send_sc:
                self.service_check(
                    self.SERVICE_CHECK_CONNECT_NAME,
                    AgentCheck.CRITICAL,
                    message="Error {0} when hitting {1}".format(e, url),
                    tags=config.service_check_tags
                )
            raise

        return resp.json()

    def _process_metric(self, data, metric, xtype, path, xform=None,
                        tags=None, hostname=None):
        """data: dictionary containing all the stats
        metric: datadog metric
        path: corresponding path in data, flattened, e.g. thread_pool.bulk.queue
        xform: a lambda to apply to the numerical value
        """
        value = data

        # Traverse the nested dictionaries
        for key in path.split('.'):
            if value is not None:
                value = value.get(key, None)
            else:
                break

        if value is not None:
            if xform:
                value = xform(value)
            if xtype == "gauge":
                self.gauge(metric, value, tags=tags, hostname=hostname)
            else:
                self.rate(metric, value, tags=tags, hostname=hostname)
        else:
            self._metric_not_found(metric, path)

    def _metric_not_found(self, metric, path):
        self.log.debug("Metric not found: %s -> %s", path, metric)
