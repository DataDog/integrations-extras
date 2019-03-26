# stdlib
from collections import namedtuple
from six import iteritems
from six.moves.urllib.parse import urlparse, urljoin
from distutils.version import LooseVersion

# 3rd party
import requests

# project
from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.headers import headers


EVENT_TYPE = SOURCE_TYPE_NAME = 'logstash'

LogstashInstanceConfig = namedtuple(
    'LogstashInstanceConfig', [
        'service_check_tags',
        'tags',
        'timeout',
        'url',
        'ssl_verify',
        'ssl_cert',
        'ssl_key',
    ])


class LogstashCheck(AgentCheck):
    DEFAULT_VERSION = '1.0.0'
    DEFAULT_TIMEOUT = 5
    SERVICE_CHECK_CONNECT_NAME = 'logstash.can_connect'

    STATS_METRICS = {
        "logstash.process.open_file_descriptors": ("gauge", "process.open_file_descriptors"),
        "logstash.process.peak_open_file_descriptors": ("gauge", "process.peak_open_file_descriptors"),
        "logstash.process.max_file_descriptors": ("gauge", "process.max_file_descriptors"),
        "logstash.process.mem.total_virtual_in_bytes": ("gauge", "process.mem.total_virtual_in_bytes"),
        "logstash.process.cpu.total_in_millis": ("gauge", "process.cpu.total_in_millis"),
        "logstash.process.cpu.percent": ("gauge", "process.cpu.percent"),
        "logstash.process.cpu.load_average.1m": ("gauge", "process.cpu.load_average.1m"),
        "logstash.process.cpu.load_average.5m": ("gauge", "process.cpu.load_average.5m"),
        "logstash.process.cpu.load_average.15m": ("gauge", "process.cpu.load_average.15m"),
        "logstash.jvm.threads.count": ("gauge", "jvm.threads.count"),
        "logstash.jvm.threads.peak_count": ("gauge", "jvm.threads.peak_count"),
        "logstash.jvm.mem.heap_used_percent": ("gauge", "jvm.mem.heap_used_percent"),
        "logstash.jvm.mem.heap_committed_in_bytes": ("gauge", "jvm.mem.heap_committed_in_bytes"),
        "logstash.jvm.mem.heap_max_in_bytes": ("gauge", "jvm.mem.heap_max_in_bytes"),
        "logstash.jvm.mem.heap_used_in_bytes": ("gauge", "jvm.mem.heap_used_in_bytes"),
        "logstash.jvm.mem.non_heap_used_in_bytes": ("gauge", "jvm.mem.non_heap_used_in_bytes"),
        "logstash.jvm.mem.non_heap_committed_in_bytes": ("gauge", "jvm.mem.non_heap_committed_in_bytes"),
        "logstash.jvm.mem.pools.survivor.peak_used_in_bytes": ("gauge", "jvm.mem.pools.survivor.peak_used_in_bytes"),
        "logstash.jvm.mem.pools.survivor.used_in_bytes": ("gauge", "jvm.mem.pools.survivor.used_in_bytes"),
        "logstash.jvm.mem.pools.survivor.peak_max_in_bytes": ("gauge", "jvm.mem.pools.survivor.peak_max_in_bytes"),
        "logstash.jvm.mem.pools.survivor.max_in_bytes": ("gauge", "jvm.mem.pools.survivor.max_in_bytes"),
        "logstash.jvm.mem.pools.survivor.committed_in_bytes": ("gauge", "jvm.mem.pools.survivor.committed_in_bytes"),
        "logstash.jvm.mem.pools.old.peak_used_in_bytes": ("gauge", "jvm.mem.pools.old.peak_used_in_bytes"),
        "logstash.jvm.mem.pools.old.used_in_bytes": ("gauge", "jvm.mem.pools.old.used_in_bytes"),
        "logstash.jvm.mem.pools.old.peak_max_in_bytes": ("gauge", "jvm.mem.pools.old.peak_max_in_bytes"),
        "logstash.jvm.mem.pools.old.max_in_bytes": ("gauge", "jvm.mem.pools.old.max_in_bytes"),
        "logstash.jvm.mem.pools.old.committed_in_bytes": ("gauge", "jvm.mem.pools.old.committed_in_bytes"),
        "logstash.jvm.mem.pools.young.peak_used_in_bytes": ("gauge", "jvm.mem.pools.young.peak_used_in_bytes"),
        "logstash.jvm.mem.pools.young.used_in_bytes": ("gauge", "jvm.mem.pools.young.used_in_bytes"),
        "logstash.jvm.mem.pools.young.peak_max_in_bytes": ("gauge", "jvm.mem.pools.young.peak_max_in_bytes"),
        "logstash.jvm.mem.pools.young.max_in_bytes": ("gauge", "jvm.mem.pools.young.max_in_bytes"),
        "logstash.jvm.mem.pools.young.committed_in_bytes": ("gauge", "jvm.mem.pools.young.committed_in_bytes"),
        "logstash.jvm.gc.collectors.old.collection_time_in_millis":
            ("gauge", "jvm.gc.collectors.old.collection_time_in_millis"),
        "logstash.jvm.gc.collectors.old.collection_count": ("gauge", "jvm.gc.collectors.old.collection_count"),
        "logstash.jvm.gc.collectors.young.collection_time_in_millis":
            ("gauge", "jvm.gc.collectors.young.collection_time_in_millis"),
        "logstash.jvm.gc.collectors.young.collection_count": ("gauge", "jvm.gc.collectors.young.collection_count"),
        "logstash.reloads.successes": ("gauge", "reloads.successes"),
        "logstash.reloads.failures": ("gauge", "reloads.failures")
    }

    PIPELINE_METRICS = {
        "logstash.pipeline.events.duration_in_millis": ("gauge", "pipeline.events.duration_in_millis"),
        "logstash.pipeline.events.in": ("gauge", "pipeline.events.in"),
        "logstash.pipeline.events.out": ("gauge", "pipeline.events.out"),
        "logstash.pipeline.events.filtered": ("gauge", "pipeline.events.filtered"),
        "logstash.pipeline.reloads.successes": ("gauge", "pipeline.reloads.successes"),
        "logstash.pipeline.reloads.failures": ("gauge", "pipeline.reloads.failures")
    }

    PIPELINE_INPUTS_METRICS = {
        "logstash.pipeline.plugins.inputs.events.out": ("gauge", "events.out"),
        "logstash.pipeline.plugins.inputs.events.queue_push_duration_in_millis":
            ("gauge", "events.queue_push_duration_in_millis")
    }

    PIPELINE_OUTPUTS_METRICS = {
        "logstash.pipeline.plugins.outputs.events.in": ("gauge", "events.in"),
        "logstash.pipeline.plugins.outputs.events.out": ("gauge", "events.out"),
        "logstash.pipeline.plugins.outputs.events.duration_in_millis": ("gauge", "events.duration_in_millis")
    }

    PIPELINE_FILTERS_METRICS = {
        "logstash.pipeline.plugins.filters.events.in": ("gauge", "events.in"),
        "logstash.pipeline.plugins.filters.events.out": ("gauge", "events.out"),
        "logstash.pipeline.plugins.filters.events.duration_in_millis": ("gauge", "events.duration_in_millis")
    }

    def get_instance_config(self, instance):
        url = instance.get('url')
        if url is None:
            raise Exception("A URL must be specified in the instance")

        # Support URLs that have a path in them from the config, for
        # backwards-compatibility.
        parsed = urlparse(url)
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

        config = LogstashInstanceConfig(
            service_check_tags=service_check_tags,
            ssl_cert=instance.get('ssl_cert'),
            ssl_key=instance.get('ssl_key'),
            ssl_verify=instance.get('ssl_verify', False),
            tags=tags,
            timeout=timeout,
            url=url
        )
        return config

    def _get_data(self, url, config, send_sc=True):
        """ Hit a given URL and return the parsed json
        """
        auth = None

        # Load SSL configuration, if available.
        # ssl_verify can be a bool or a string
        # (http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification)
        if isinstance(config.ssl_verify, (bool, str)):
            verify = config.ssl_verify
        else:
            self.log.error("ssl_verify in the configuration file must be a bool or a string.")
            verify = None
        if config.ssl_cert and config.ssl_key:
            cert = (config.ssl_cert, config.ssl_key)
        elif config.ssl_cert:
            cert = config.ssl_cert
        else:
            cert = None

        try:
            resp = requests.get(
                url,
                timeout=config.timeout,
                headers=headers(self.agentConfig),
                auth=auth,
                verify=verify,
                cert=cert
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

    def _get_logstash_version(self, config):
        """ Get the running version of logstash.
        """
        try:
            data = self._get_data(config.url, config, send_sc=False)
            version = data['version']
        except Exception as e:
            self.warning(
                "Error while trying to get Logstash version "
                "from %s %s. Defaulting to version %s."
                % (config.url, str(e), self.DEFAULT_VERSION)
            )
            version = self.DEFAULT_VERSION

        self.service_metadata('version', version)
        self.log.debug("Logstash version is %s" % version)
        return version

    def check(self, instance):
        config = self.get_instance_config(instance)

        version = self._get_logstash_version(config)

        stats_metrics = dict(self.STATS_METRICS)
        stats_metrics.update(self.PIPELINE_METRICS)

        stats_url = urljoin(config.url, '/_node/stats')
        stats_data = self._get_data(stats_url, config)

        self._process_stats_data(stats_data, stats_metrics, config)

        if version and LooseVersion(version) < LooseVersion("6.0.0"):
            self._process_pipeline_plugins_data(
                stats_data['pipeline']['plugins'],
                self.PIPELINE_INPUTS_METRICS, config, 'inputs', 'input_name')
            self._process_pipeline_plugins_data(
                stats_data['pipeline']['plugins'],
                self.PIPELINE_OUTPUTS_METRICS, config, 'outputs',
                'output_name')
            self._process_pipeline_plugins_data(
                stats_data['pipeline']['plugins'],
                self.PIPELINE_FILTERS_METRICS, config, 'filters',
                'filter_name')
        elif version and LooseVersion(version) > LooseVersion("6.0.0"):
            for name, pipeline in stats_data['pipelines'].iteritems():
                self._process_pipeline_plugins_data(
                    pipeline['plugins'],
                    self.PIPELINE_INPUTS_METRICS, config, 'inputs', 'input_name', name)
                self._process_pipeline_plugins_data(
                    pipeline['plugins'],
                    self.PIPELINE_OUTPUTS_METRICS, config, 'outputs', 'output_name', name)
                self._process_pipeline_plugins_data(
                    pipeline['plugins'],
                    self.PIPELINE_FILTERS_METRICS, config, 'filters', 'filter_name', name)

        self.service_check(
            self.SERVICE_CHECK_CONNECT_NAME,
            AgentCheck.OK,
            tags=config.service_check_tags
        )

    def _process_stats_data(self, data, stats_metrics, config):
        for metric, desc in iteritems(stats_metrics):
            self._process_metric(data, metric, *desc, tags=config.tags)

    def _process_pipeline_plugins_data(
        self,
        pipeline_plugins_data,
        pipeline_plugins_metrics,
        config,
        plugin_type,
        tag_name,
        pipeline_name=""
    ):
        for plugin_data in pipeline_plugins_data.get(plugin_type, []):
            plugin_name = plugin_data.get('name')

            metrics_tags = list(config.tags)

            if not plugin_name:
                plugin_name = 'unknown'

            metrics_tags.append(
                u"{}:{}".format(tag_name, plugin_name)
            )

            if pipeline_name:
                metrics_tags.append(
                    u"{}:{}".format("pipeline_name", pipeline_name)
                )

            for metric, desc in iteritems(pipeline_plugins_metrics):
                self._process_metric(
                    plugin_data, metric, *desc,
                    tags=metrics_tags)

    def _process_metric(self, data, metric, xtype, path,
                        tags=None, hostname=None):
        """data: dictionary containing all the stats
        metric: datadog metric
        path: corresponding path in data, flattened, e.g. thread_pool.bulk.queue
        """
        value = data

        # Traverse the nested dictionaries
        for key in path.split('.'):
            if value is not None:
                value = value.get(key, None)
            else:
                break

        if value is not None:
            if xtype == "gauge":
                self.gauge(metric, value, tags=tags, hostname=hostname)
            else:
                self.rate(metric, value, tags=tags, hostname=hostname)
        else:
            self._metric_not_found(metric, path)

    def _metric_not_found(self, metric, path):
        self.log.debug("Metric not found: %s -> %s", path, metric)
