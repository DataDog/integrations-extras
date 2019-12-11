# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import mock
import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.cert_manager import CertManagerCheck

from .common import EXPECTED_METRICS, MOCK_INSTANCE


def get_response(filename):
    metrics_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(metrics_file_path, 'r') as f:
        response = f.read()
    return response


@pytest.fixture()
def mock_metrics():
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', 'cert_manager.txt')
    with open(f_name, 'r') as f:
        text_data = f.read()
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200, iter_lines=lambda **kwargs: text_data.split("\n"), headers={'Content-Type': "text/plain"}
        ),
    ):
        yield


@pytest.mark.unit
def test_config():
    with pytest.raises(CheckException):
        CertManagerCheck('cert-manager', {}, {}, [{}])

    # this should not fail
    CertManagerCheck('cert-manager', {}, {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_check(aggregator, instance, mock_metrics):
    check = CertManagerCheck('cert_manager', {}, {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for metric_name, metric_type in EXPECTED_METRICS.items():
        aggregator.assert_metric(metric_name, metric_type=metric_type)

    aggregator.assert_all_metrics_covered()

    aggregator.assert_service_check(
        'cert_manager.prometheus.health',
        status=CertManagerCheck.OK,
        tags=['endpoint:http://fake.tld/prometheus'],
        count=1,
    )
