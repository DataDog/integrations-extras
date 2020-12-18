# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import mock
import pytest

from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.open_policy_agent import OpenPolicyAgentCheck

from .common import EXPECTED_CHECKS, EXPECTED_METRICS, MOCK_INSTANCE


def get_response(filename):
    metrics_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(metrics_file_path, 'r') as f:
        response = f.read()
    return response


@pytest.fixture()
def mock_metrics():
    text_data = get_response('open_policy_agent.txt')
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200, iter_lines=lambda **kwargs: text_data.split("\n"), headers={'Content-Type': "text/plain"}
        ),
    ):
        yield


@pytest.fixture()
def error_metrics():
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(status_code=502, headers={'Content-Type': "text/plain"}),
    ):
        yield


@pytest.mark.unit
def test_config():
    with pytest.raises((CheckException, ConfigurationError)):
        OpenPolicyAgentCheck('open_policy_agent', {}, [{}])

    # this should not fail
    OpenPolicyAgentCheck('open_policy_agent', {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_check(aggregator, instance, mock_metrics):
    check = OpenPolicyAgentCheck('open_policy_agent', {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for metric_name, metric_type in EXPECTED_METRICS.items():
        aggregator.assert_metric(metric_name, metric_type=metric_type)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)

    aggregator.assert_service_check(
        'open_policy_agent.prometheus.health',
        status=OpenPolicyAgentCheck.OK,
        tags=['endpoint:http://fake.tld/metrics'],
        count=1,
    )

    for check_name in EXPECTED_CHECKS:
        aggregator.assert_service_check(
            check_name,
            status=OpenPolicyAgentCheck.OK,
            tags=[],
            count=1,
        )


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance, error_metrics):
    check = OpenPolicyAgentCheck('open_policy_agent', {}, [MOCK_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_INSTANCE)
        aggregator.assert_service_check(
            'open_policy_agent.prometheus.health',
            status=OpenPolicyAgentCheck.CRITICAL,
            tags=['endpoint:http://fake.tld/prometheus'],
            count=1,
        )

        for check_name in EXPECTED_CHECKS:
            aggregator.assert_service_check(
                check_name,
                status=OpenPolicyAgentCheck.CRITICAL,
                tags=[],
                count=1,
            )


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = OpenPolicyAgentCheck('open_policy_agent', {}, [instance])

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('open_policy_agent.health', status=OpenPolicyAgentCheck.OK)
    aggregator.assert_service_check('open_policy_agent.plugins_health', status=OpenPolicyAgentCheck.OK)
    aggregator.assert_service_check('open_policy_agent.bundles_health', status=OpenPolicyAgentCheck.OK)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check_error(aggregator, instance):
    instance.update({'opa_url': 'http://fake.tld'})
    c = OpenPolicyAgentCheck('open_policy_agent', {}, [instance])

    # the check should send CRITICAL
    c.check(instance)
    aggregator.assert_service_check('open_policy_agent.health', status=OpenPolicyAgentCheck.CRITICAL)
    aggregator.assert_service_check('open_policy_agent.plugins_health', status=OpenPolicyAgentCheck.CRITICAL)
    aggregator.assert_service_check('open_policy_agent.bundles_health', status=OpenPolicyAgentCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_metrics(aggregator, instance):
    c = OpenPolicyAgentCheck('open_policy_agent', {}, [instance])

    # the check should send OK
    c.check(instance)
    metric_name = 'open_policy_agent.policies'
    aggregator.assert_metric(metric_name, value=0.0, tags=[], hostname='')

    metric_name = 'open_policy_agent.request.duration.sum'
    aggregator.assert_metric(metric_name, tags=['code:200', 'handler:index', 'method:get'], hostname='')
    aggregator.assert_metric(metric_name, tags=['code:200', 'handler:health', 'method:get'], hostname='')
    aggregator.assert_metric(metric_name, tags=['code:200', 'handler:v1/policies', 'method:get'], hostname='')

    metric_name = 'open_policy_agent.request.duration.count'
    aggregator.assert_metric(metric_name, hostname='')

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)
