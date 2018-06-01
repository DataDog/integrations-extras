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

@attr(requires='gnatsd')
class TestGnatsd(AgentCheckTest):
    """Basic Test for gnatsd integration."""
    CHECK_NAME = 'gnatsd'

    CONNECTION_FAILURE = [{
        'host': 'http://totally_not_locallhost',
        'port': 8222
    }]

    CONNECTION_SUCCESS = [{
        'host': 'http://localhost',
        'port': 8222
    }]

    def test_connection_failure(self):
        config = {'instances': self.CONNECTION_FAILURE}
        self.assertRaises(
            Exception,
            lambda: self.run_check(config)
        )
        self.assertServiceCheck('gnatsd.can_connect', status=AgentCheck.CRITICAL, count=1)
        self.coverage_report()

    def test_metrics(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)

        self.assertServiceCheck('gnatsd.can_connect', status=AgentCheck.OK, count=1)
        self.assertMetric('gnatsd.varz.connections', metric_type='gauge')
        self.assertMetric('gnatsd.varz.subscriptions', metric_type='gauge')
        self.assertMetric('gnatsd.varz.slow_consumers', metric_type='count')
        self.assertMetric('gnatsd.varz.remotes', metric_type='gauge')
        self.assertMetric('gnatsd.varz.routes', metric_type='gauge')
        self.assertMetric('gnatsd.varz.in_msgs', metric_type='count')
        self.assertMetric('gnatsd.varz.out_msgs', metric_type='count')
        self.assertMetric('gnatsd.varz.in_bytes', metric_type='count')
        self.assertMetric('gnatsd.varz.out_bytes', metric_type='count')
        self.assertMetric('gnatsd.varz.mem', metric_type='gauge')
        self.assertMetric('gnatsd.connz.num_connections', metric_type='gauge')
        self.assertMetric('gnatsd.connz.total', metric_type='count')
        self.assertMetric('gnatsd.connz.connections.foo-sub.pending_bytes', metric_type='gauge')
        self.assertMetric('gnatsd.connz.connections.foo-sub.in_msgs', metric_type='count')
        # We sent 2 messages to this queue in the ci setup
        self.assertMetric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type='count', value=2)
        self.assertMetric('gnatsd.connz.connections.foo-sub.subscriptions', metric_type='gauge')
        self.assertMetric('gnatsd.connz.connections.foo-sub.in_bytes', metric_type='count')
        self.assertMetric('gnatsd.connz.connections.foo-sub.out_bytes', metric_type='count')
        self.assertMetric('gnatsd.connz.connections.unnamed.pending_bytes', metric_type='gauge')
        self.assertMetric('gnatsd.connz.connections.unnamed.in_msgs', metric_type='count')
        # We sent 1 message to this queue in the ci setup
        self.assertMetric('gnatsd.connz.connections.unnamed.out_msgs', metric_type='count', value=1)
        self.assertMetric('gnatsd.connz.connections.unnamed.subscriptions', metric_type='gauge')
        self.assertMetric('gnatsd.connz.connections.unnamed.in_bytes', metric_type='count')
        self.assertMetric('gnatsd.connz.connections.unnamed.out_bytes', metric_type='count')
        self.assertMetric('gnatsd.routez.num_routes', metric_type='gauge')
        self.assertMetric('gnatsd.routez.routes.172_17_0_2.in_msgs', metric_type='count')
        self.assertMetric('gnatsd.routez.routes.172_17_0_2.out_msgs', metric_type='count')
        self.assertMetric('gnatsd.routez.routes.172_17_0_2.subscriptions', metric_type='gauge')
        self.assertMetric('gnatsd.routez.routes.172_17_0_2.in_bytes', metric_type='count')
        self.assertMetric('gnatsd.routez.routes.172_17_0_2.out_bytes', metric_type='count')
        self.assertMetric('gnatsd.routez.routes.172_17_0_2.pending_size', metric_type='gauge')
        self.coverage_report()

    def test_metric_tags(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)

        self.assertMetricTagPrefix('gnatsd.varz.connections', 'gnatsd-server_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-cid', at_least=1)
        self.assertMetricTagPrefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-ip', at_least=1)
        self.assertMetricTagPrefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-name', at_least=1)
        self.assertMetricTagPrefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-lang', at_least=1)
        self.assertMetricTagPrefix('gnatsd.connz.connections.foo-sub.out_msgs', 'gnatsd-version', at_least=1)
        self.assertMetricTagPrefix('gnatsd.routez.routes.172_17_0_2.in_msgs', 'gnatsd-rid', at_least=1)
        self.assertMetricTagPrefix('gnatsd.routez.routes.172_17_0_2.in_msgs', 'gnatsd-remote_id', at_least=1)
        self.assertMetricTagPrefix('gnatsd.routez.routes.172_17_0_2.in_msgs', 'gnatsd-ip', at_least=1)

    def test_deltas(self):
        config = {'instances': self.CONNECTION_SUCCESS}
        self.run_check(config)
        self.assertMetric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type='count', value=2)
        self.run_check(config)
        self.assertMetric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type='count', value=0)
        self.run_check(config)
        self.assertMetric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type='count', value=0)
        self.run_check(config)
        self.assertMetric('gnatsd.connz.connections.foo-sub.out_msgs', metric_type='count', value=0)
