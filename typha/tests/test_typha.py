# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import mock
import pytest

from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.typha import TyphaCheck

from .common import EXPECTED_METRICS, EXPECTED_CHECKS, MOCK_INSTANCE


def get_response(filename):
    metrics_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(metrics_file_path, 'r') as f:
        response = f.read()
    return response


@pytest.fixture()
def mock_typha_metrics():
    text_data = get_response('metrics.txt')
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200, iter_lines=lambda **kwargs: text_data.split("\n"), headers={'Content-Type': "text/plain"}
        ),
    ):
        yield


@pytest.fixture()
def error_instance():
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(status_code=502, headers={'Content-Type': "text/plain"}),
    ):
        yield


@pytest.mark.unit
def test_config():
    with pytest.raises((CheckException, ConfigurationError)):
        TyphaCheck('typha', {}, [{}])

    # this should not fail
    TyphaCheck('typha', {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_typha_metrics(aggregator, instance, mock_typha_metrics):
    check = TyphaCheck('typha', {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for metric_name, metric_type in EXPECTED_METRICS.items():
        aggregator.assert_metric(metric_name, metric_type=metric_type, at_least=0)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_check(aggregator, instance, mock_typha_metrics):
    check = TyphaCheck('typha', {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for check_name in EXPECTED_CHECKS:
        aggregator.assert_service_check(
            check_name,
            status=TyphaCheck.OK,
            tags=[],
            count=1,
        )


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance, error_instance):
    check = TyphaCheck('typha', {}, [MOCK_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_INSTANCE)

        for check_name in EXPECTED_CHECKS:
            aggregator.assert_service_check(
                check_name,
                status=TyphaCheck.CRITICAL,
                tags=[],
                count=1,
            )
