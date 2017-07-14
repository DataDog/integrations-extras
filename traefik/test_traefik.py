# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import os
from mock import MagicMock
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest


@attr(requires='traefik')
class TestTraefik(AgentCheckTest):
    CHECK_NAME = "traefik"
    NAMESPACE = "traefik"
    METRICS = [
        NAMESPACE + '.request.duration.count',
        NAMESPACE + '.request.duration.sum',
        NAMESPACE + '.requests.total',
    ]

    def test_check(self):
        instance = {
            'prometheus_endpoint': 'http://localhost/metrics',
        }

        content_type = 'text/plain; version=0.0.4'
        f_name = os.path.join(os.path.dirname(__file__), 'ci', 'metrics.txt')
        with open(f_name, 'r') as f:
            bin_data = f.read()
        mocks = {
            'poll': MagicMock(return_value=[content_type, bin_data])
        }
        self.run_check({'instances': [instance]}, mocks=mocks)

        for metric in self.METRICS:
            self.assertMetric(metric)

        self.coverage_report()
