# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import os
import json

import pytest
from mock import MagicMock

from datadog_checks.aqua import AquaCheck


CHECK_NAME = 'aqua'
HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def instance():
    return {
        'url': 'http://localhost:8080',
        'api_user': 'foo',
        'password': 'bar',
        'tags': ['foo:bar']
    }


@pytest.fixture()
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator


EXPECTED_VALUES = (
    ("aqua.images", 9),
    ("aqua.scan_queue", 0),
    ("aqua.audit.access", 2),
    ("aqua.vulnerabilities", 49),
    ("aqua.enforcers", 0),
    ("aqua.running_containers", 0)
)


def test_check(aggregator, instance):
    """
    Testing Aqua check.
    """
    check = AquaCheck('aqua', {}, {})
    check.validate_instance = MagicMock(return_value=None)
    check.get_aqua_token = MagicMock(return_value="test")

    def mock_perform(inst, url, token):
        if url == '/api/v1/dashboard':
            with open(os.path.join(HERE, 'aqua_base_metrics.json'), 'r') as f:
                return json.load(f)
        elif url == '/api/v1/hosts':
            with open(os.path.join(HERE, 'aqua_hosts_metrics.json'), 'r') as f:
                return json.load(f)
        elif url == '/api/v1/audit/access_totals?alert=-1&limit=100&time=hour&type=all':
            with open(os.path.join(HERE, 'aqua_audit_metrics.json'), 'r') as f:
                return json.load(f)
        elif url == '/api/v1/scanqueue/summary':
            with open(os.path.join(HERE, 'aqua_scan_queues_metrics.json'), 'r') as f:
                return json.load(f)
    check._perform_query = MagicMock(side_effect=mock_perform)

    check.check(instance)
    for metric, value in EXPECTED_VALUES:
        aggregator.assert_metric(metric, value=value)

    aggregator.assert_service_check(check.SERVICE_CHECK_NAME)
    # Raises when COVERAGE=true and coverage < 100%
    aggregator.assert_all_metrics_covered()
