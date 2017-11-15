# stdlib
from nose.plugins.attrib import attr

# 3p
import requests

# project
from tests.checks.common import AgentCheckTest
from config import get_version


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
    "logstash.jvm.gc.collectors.old.collection_time_in_millis": ("gauge", "jvm.gc.collectors.old.collection_time_in_millis"),
    "logstash.jvm.gc.collectors.old.collection_count": ("gauge", "jvm.gc.collectors.old.collection_count"),
    "logstash.jvm.gc.collectors.young.collection_time_in_millis": ("gauge", "jvm.gc.collectors.young.collection_time_in_millis"),
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
    "logstash.pipeline.plugins.inputs.events.queue_push_duration_in_millis": ("gauge", "events.queue_push_duration_in_millis")
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

@attr(requires='logstash')
class TestLogstash(AgentCheckTest):
    """Basic Test for logstash integration."""
    CHECK_NAME = 'logstash'

    def test_check(self):
        conf_hostname = "foo"
        port = 9600
        bad_port = 9405
        url = 'http://localhost:{0}'.format(port)
        bad_url = 'http://localhost:{0}'.format(bad_port)

        agent_config = {
            "hostname": conf_hostname, "version": get_version(),
            "api_key": "bar"
        }

        tags = [u"foo:bar", u"baz"]

        input_tag = [u"input_name:stdin"]
        output_tag = [u"output_name:stdout"]
        filter_tag = [u"filter_name:json"]

        config = {
            'instances': [
                {'url': url, 'tags': tags},  # One with tags not external
                {'url': bad_url},  # One bad url
            ]
        }

        self.assertRaises(
            requests.exceptions.ConnectionError,
            self.run_check, config=config, agent_config=agent_config)

        default_tags = ["url:http://localhost:{0}".format(port)]

        instance_config = self.check.get_instance_config(config['instances'][0])

        logstash_version = self.check._get_logstash_version(instance_config)

        expected_metrics = dict(STATS_METRICS)

        if logstash_version < [6, 0, 0]:
            expected_metrics.update(PIPELINE_METRICS)
            expected_metrics.update(PIPELINE_INPUTS_METRICS)
            expected_metrics.update(PIPELINE_OUTPUTS_METRICS)
            expected_metrics.update(PIPELINE_FILTERS_METRICS)

        good_sc_tags = ['host:localhost', 'port:{0}'.format(port)]
        bad_sc_tags = ['host:localhost', 'port:{0}'.format(bad_port)]

        for m_name, desc in expected_metrics.iteritems():
            m_tags = tags + default_tags
            if m_name in PIPELINE_INPUTS_METRICS:
                m_tags = m_tags + input_tag
            if m_name in PIPELINE_OUTPUTS_METRICS:
                m_tags = m_tags + output_tag
            if m_name in PIPELINE_FILTERS_METRICS:
                m_tags = m_tags + filter_tag
            if desc[0] == "gauge":
                self.assertMetric(
                    m_name, tags=m_tags, count=1, hostname=conf_hostname)

        self.assertServiceCheckOK('logstash.can_connect',
                                  tags=good_sc_tags + tags,
                                  count=1)
        self.assertServiceCheckCritical('logstash.can_connect',
                                        tags=bad_sc_tags,
                                        count=1)

        # Assert service metadata
        self.assertServiceMetadata(['version'], count=2)

        self.coverage_report()
