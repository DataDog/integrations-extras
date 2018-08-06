# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest
from mock import MagicMock
from datadog_checks.bind9_check import bind9_check
import os

HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'http://10.10.1.101:8080'

@pytest.fixture()
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator

@pytest.fixture
def instance():
    return {
        'url': URL
    }

def test_check(aggregator, instance):
	c = bind9_check('bind9_check', {}, {}, None)
	c.check(instance)

	with open(os.path.join(HERE,'sample_stats.xml'), 'r') as file :
		c.getStatsFromUrl = MagicMock(return_value=file)
	stats = c.getStatsFromUrl(c, URL)
	c.getStatsFromUrl.assert_called_with(c, URL )
	aggregator.assert_all_metrics_covered()
