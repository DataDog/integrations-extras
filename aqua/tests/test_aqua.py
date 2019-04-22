# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import json
import os

from mock import MagicMock

from datadog_checks.aqua import AquaCheck

from .common import HERE

EXPECTED_VALUES = (
    ("aqua.images", 9),
    ("aqua.scan_queue", 0),
    ("aqua.audit.access", 2),
    ("aqua.vulnerabilities", 49),
    ("aqua.enforcers", 0),
    ("aqua.running_containers", 0),
)


def test_check(aggregator, instance):
    """
    Testing Aqua check.
    Add e2e eventually https://github.com/aquasecurity/microscanner
    """
    check = AquaCheck('aqua', {}, {})
    check.validate_instance = MagicMock(return_value=None)
    check.get_aqua_token = MagicMock(return_value="test")

    def mock_perform(inst, url, token):
        if url == '/api/v1/dashboard':
            with open(os.path.join(HERE, 'fixtures', 'aqua_base_metrics.json'), 'r') as f:
                return json.load(f)
        elif url == '/api/v1/hosts':
            with open(os.path.join(HERE, 'fixtures', 'aqua_hosts_metrics.json'), 'r') as f:
                return json.load(f)
        elif url == '/api/v1/audit/access_totals?alert=-1&limit=100&time=hour&type=all':
            with open(os.path.join(HERE, 'fixtures', 'aqua_audit_metrics.json'), 'r') as f:
                return json.load(f)
        elif url == '/api/v1/scanqueue/summary':
            with open(os.path.join(HERE, 'fixtures', 'aqua_scan_queues_metrics.json'), 'r') as f:
                return json.load(f)

    check._perform_query = MagicMock(side_effect=mock_perform)

    check.check(instance)
    for metric, value in EXPECTED_VALUES:
        aggregator.assert_metric(metric, value=value)

    aggregator.assert_service_check(check.SERVICE_CHECK_NAME)
    aggregator.assert_all_metrics_covered()
