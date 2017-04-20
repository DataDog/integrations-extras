# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import os
import time
import socket

# stdlib
from nose.plugins.attrib import attr
import requests
# 3p

# project
from tests.checks.common import AgentCheckTest, load_check

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

# NOTE: Feel free to declare multiple test classes if needed

@attr(requires='logstash')
class TestLogstash(AgentCheckTest):
    """Basic Test for logstash integration."""
    CHECK_NAME = 'logstash'

    def test_check(self):
        """
        Testing Logstash check.
        """
        agent_config = {
            "hostname": "foo",
            "version": "1.0",
            "api_key": "bar"
        }
        host = 'localhost'
        port = '9600'
        bad_port = '9605'
        url = 'http://{0}:{1}'.format(host, port)
        bad_url = 'http://{0}:{1}'.format(host, bad_port)
        bad_instance_tag = [u"bad"]
        tags = [u"foo:bar", u"baz"]
        config = {
            'instances': [
                {'url': url, 'tags': tags},
                {'url': bad_url, 'tags': bad_instance_tag}
            ]
        }

        self.assertRaises(
            requests.exceptions.ConnectionError,
            self.run_check, config=config, agent_config=agent_config)

        expected_metrics = STATS_METRICS
        instance_config = self.check.get_instance_config(config['instances'][0])
        
        metric_tags = ['url:{0}'.format(url)] + tags

        for m_name, desc in expected_metrics.iteritems():
            if desc[0] == "gauge":
                self.assertMetric(m_name, tags=metric_tags, at_least=1)

        good_sc_tags = ['host:{0}'.format(host), 'port:{0}'.format(port)] + tags
        bad_sc_tags = ['host:{0}'.format(host), 'port:{0}'.format(bad_port)] + bad_instance_tag

        self.assertServiceCheckOK('logstash.can_connect',
                                  tags=good_sc_tags,
                                  count=1)
        self.assertServiceCheckCritical('logstash.can_connect',
                                        tags=bad_sc_tags,
                                        count=1)

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
