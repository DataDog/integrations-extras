# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import mock
import pytest

from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.opa import OpaCheck

from .common import EXPECTED_CHECKS, EXPECTED_METRICS, MOCK_INSTANCE


def get_response(filename):
    metrics_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(metrics_file_path, 'r') as f:
        response = f.read()
    return response


@pytest.fixture()
def mock_metrics():
    text_data = get_response('opa.txt')
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
        OpaCheck('opa', {}, [{}])

    # this should not fail
    OpaCheck('opa', {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_check(aggregator, instance, mock_metrics):
    check = OpaCheck('opa', {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for metric_name, metric_type in EXPECTED_METRICS.items():
        aggregator.assert_metric(metric_name, metric_type=metric_type)

    aggregator.assert_all_metrics_covered()

    aggregator.assert_service_check(
        'opa.prometheus.health',
        status=OpaCheck.OK,
        tags=['endpoint:http://fake.tld/metrics'],
        count=1,
    )

    for check_name in EXPECTED_CHECKS:
        aggregator.assert_service_check(
            check_name,
            status=OpaCheck.OK,
            tags=[],
            count=1,
        )


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance, error_metrics):
    check = OpaCheck('opa', {}, [MOCK_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_INSTANCE)
        aggregator.assert_service_check(
            'opa.prometheus.health',
            status=OpaCheck.CRITICAL,
            tags=['endpoint:http://fake.tld/prometheus'],
            count=1,
        )

        for check_name in EXPECTED_CHECKS:
            aggregator.assert_service_check(
                check_name,
                status=OpaCheck.CRITICAL,
                tags=[],
                count=1,
            )


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = OpaCheck('opa', {}, [instance])

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('opa.health', OpaCheck.OK)
    aggregator.assert_service_check('opa.plugins_health', OpaCheck.OK)
    aggregator.assert_service_check('opa.bundles_health', OpaCheck.OK)

    # the check should send CRTICAL
    instance['opa_url'] = 'http://fake.tld'
    c.check(instance)
    aggregator.assert_service_check('opa.health', OpaCheck.CRITICAL)
    aggregator.assert_service_check('opa.plugins_health', OpaCheck.CRITICAL)
    aggregator.assert_service_check('opa.bundles_health', OpaCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_metrics(aggregator, instance):
    c = OpaCheck('opa', {}, [instance])

    # the check should send OK
    c.check(instance)
    metric_name = 'opa.policies'
    aggregator.assert_metric(metric_name, value=0.0, tags=[], hostname='')

    metric_name = 'opa.request.duration.sum'
    aggregator.assert_metric(metric_name, tags=['code:200', 'handler:index', 'method:get'], hostname='')
    aggregator.assert_metric(metric_name, tags=['code:200', 'handler:health', 'method:get'], hostname='')
    aggregator.assert_metric(metric_name, tags=['code:200', 'handler:v1/policies', 'method:get'], hostname='')

    metric_name = 'opa.request.duration.count'
    aggregator.assert_metric(metric_name, hostname='')

    aggregator.assert_all_metrics_covered()
