# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import logging
import os

# stdlib
import threading
import time
import unittest

import mock

# project
from aggregator import MetricsAggregator

# 3p
from nose.plugins.attrib import attr

log = logging.getLogger('hbase_regionserver_test')

STATSD_PORT = 8121

LOG_INFO = {
    'log_to_event_viewer': False,
    'log_to_syslog': False,
    'syslog_host': None,
    'syslog_port': None,
    'log_level': logging.INFO,
    'disable_file_logging': True,
    'collector_log_file': '/tmp/collector.log',
    'forwarder_log_file': '/tmp/forwarder.log',
    'dogstatsd_log_file': '/tmp/dogstatsd.log',
    'jmxfetch_log_file': '/tmp/datadog/jmxfetch.log',
    'go-metro_log_file': '/tmp/datadog/go-metro.log',
}

with mock.patch('config.get_logging_config', return_value=LOG_INFO):
    from dogstatsd import Server
    from jmxfetch import JMXFetch


class DummyReporter(threading.Thread):
    def __init__(self, metrics_aggregator):
        threading.Thread.__init__(self)
        self.finished = threading.Event()
        self.metrics_aggregator = metrics_aggregator
        self.interval = 10
        self.metrics = None
        self.finished = False
        self.start()

    def run(self):
        while not self.finished:
            time.sleep(self.interval)
            self.flush()

    def flush(self):
        metrics = self.metrics_aggregator.flush()
        if metrics:
            self.metrics = metrics


@attr(requires='hbase_regionserver')
class TestHbase_regionserver(unittest.TestCase):
    """Basic Test for hbase_regionserver integration."""

    def setUp(self):
        aggregator = MetricsAggregator("test_host")
        self.server = Server(aggregator, "localhost", STATSD_PORT)
        self.reporter = DummyReporter(aggregator)

        self.t1 = threading.Thread(target=self.server.start)
        self.t1.start()

        confd_path = os.path.join(os.path.dirname(__file__), 'ci/resources/')

        self.jmx_daemon = JMXFetch(confd_path, {'dogstatsd_port': STATSD_PORT})
        self.t2 = threading.Thread(target=self.jmx_daemon.run)
        self.t2.start()

    def tearDown(self):
        self.server.stop()
        self.reporter.finished = True
        self.jmx_daemon.terminate()

    def testCustomJMXMetric(self):
        count = 0
        while self.reporter.metrics is None:
            time.sleep(1)
            count += 1
            if count > 60:
                raise Exception("No metrics were received in 60 seconds")

        metrics = self.reporter.metrics
        self.assertTrue(isinstance(metrics, list))
        self.assertTrue(len(metrics) > 0)

        self.assertTrue(
            len(
                [
                    t
                    for t in metrics
                    if "jvm." in t['metric'] and "instance:hbase_regionserver-localhost-10102" in t['tags']
                ]
            )
            >= 13,
            metrics,
        )

        # waiting for receiving metrics which appears after a while.
        count = 0
        while True:
            metrics = self.reporter.metrics
            mutations_metrics = [
                t
                for t in metrics
                if "hbase.regionserver.server.mutations" in t['metric']
                and "instance:hbase_regionserver-localhost-10102" in t['tags']
            ]
            slow_appned_metrics = [
                t
                for t in metrics
                if "hbase.regionserver.server.slow_append" in t['metric']
                and "instance:hbase_regionserver-localhost-10102" in t['tags']
            ]
            # hedged_metrics = [t for t in metrics if "hbase.regionserver.server.hedged_read" in t['metric'] and "instance:hbase_regionserver-localhost-10102" in t['tags']]  # noqa: E501
            # pause_time_metrics = [t for t in metrics if "hbase.regionserver.server.pause_time" in t['metric'] and "instance:hbase_regionserver-localhost-10102" in t['tags']]  # noqa: E501
            time.sleep(1)
            count += 1
            if len(mutations_metrics) >= 2 and len(slow_appned_metrics) >= 1:
                break
            elif count <= 60:
                continue
            else:
                log.info(metrics)
                raise Exception("enough metrics were received in 60 seconds")

        # hbase.regionserver.server.hedged_read* and hbase.regionserver.server.pause* is ignored here
        # because these metrics won't emit until these process will actually happen.
        metrics = [
            t
            for t in self.reporter.metrics
            if "hbase." in t['metric'] and "instance:hbase_regionserver-localhost-10102" in t['tags']
        ]
        num_total = 159
        num_hedged_read = 2
        num_pause = 14
        num = len(metrics)
        log.info(num)
        self.assertTrue(num >= (num_total - num_hedged_read - num_pause), metrics)
