# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest
from datadog_checks.bind9_check import bind9_check



@pytest.fixture()
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator

@pytest.fixture
def instance():
    return {
        'url': 'http://10.10.1.101:8080'
    }

def test_check(aggregator, instance):
	c = bind9_check('bind9_check', {}, {}, None)
	c.check(instance)
	aggregator.assert_all_metrics_covered()
