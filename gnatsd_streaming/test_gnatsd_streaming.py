# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p

# project
from check import AgentCheck
from tests.checks.common import AgentCheckTest

# NOTE: Feel free to declare multiple test classes if needed

@attr(requires='gnatsd_streaming')
class TestGnatsdStreaming(AgentCheckTest):
    """Basic Test for gnatsd_streaming integration."""
    CHECK_NAME = 'gnatsd_streaming'

    CONNECTION_FAILURE = [{
        'host': 'http://totally_not_locallhost',
        'port': 8222
    }]

    CONNECTION_SUCCESS = [{
        'host': 'http://localhost',
        'port': 8222,
        'pagination_limit': 1
    }]

    def test_connection_failure(self):
        config = {'instances': self.CONNECTION_FAILURE}
        self.assertRaises(
            Exception,
            lambda: self.run_check(config)
        )
        self.assertServiceCheck('gnatsd_streaming.can_connect', status=AgentCheck.CRITICAL, count=1)

    def test_metrics(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)

        self.assertServiceCheck('gnatsd_streaming.can_connect', status=AgentCheck.OK, count=1)
        self.assertMetric('gnatsd.streaming.serverz.clients', metric_type='gauge')
        self.assertMetric('gnatsd.streaming.serverz.subscriptions', metric_type='count')
        self.assertMetric('gnatsd.streaming.serverz.channels', metric_type='gauge')
        self.assertMetric('gnatsd.streaming.serverz.total_msgs', metric_type='count')
        self.assertMetric('gnatsd.streaming.serverz.total_bytes', metric_type='count')
        self.assertMetric('gnatsd.streaming.storez.total_msgs', metric_type='count')
        self.assertMetric('gnatsd.streaming.storez.total_bytes', metric_type='count')
        self.assertMetric('gnatsd.streaming.clientsz.total', metric_type='gauge')
        self.assertMetric('gnatsd.streaming.channelsz.total', metric_type='gauge')
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type='count')
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel1.bytes', metric_type='count')
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel2.msgs', metric_type='count')
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel2.bytes', metric_type='count')
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel3.msgs', metric_type='count')
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel3.bytes', metric_type='count')

        self.coverage_report()

    def test_metric_tags(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)

        self.assertMetricTagPrefix('gnatsd.streaming.serverz.clients', 'nss-cluster_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.serverz.clients', 'nss-server_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.serverz.clients', 'nss-version', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.serverz.clients', 'nss-go', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.storez.total_msgs', 'nss-cluster_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.storez.total_msgs', 'nss-server_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.clientsz.total', 'nss-cluster_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.clientsz.total', 'nss-server_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.channelsz.total', 'nss-cluster_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.streaming.channelsz.total', 'nss-server_id', at_least=1)

    def test_failover_event(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)
        self.check.ft_status = 'FT_STANDBY'
        self.run_check(config)
        self.assertEvent('NATS Streaming Server Changed Status from FT_STANDBY to FT_ACTIVE', count=1)


    def test_deltas(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type='count', value=10)
        self.run_check(config)
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type='count', value=0)
        self.run_check(config)
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type='count', value=0)
        self.run_check(config)
        self.assertMetric('gnatsd.streaming.channelsz.channels.test_channel1.msgs', metric_type='count', value=0)
