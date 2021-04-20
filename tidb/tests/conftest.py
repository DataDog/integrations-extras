import os

import mock
import pytest

from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()
HOST = get_docker_hostname()
TIDB_PORT = 10080
TIKV_PORT = 20180
PD_PORT = 2379


@pytest.fixture()
def mock_tidb_metrics():
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: get_mock_metrics("mock_tidb_metrics.txt").split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield


@pytest.fixture()
def mock_pd_metrics():
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: get_mock_metrics("mock_pd_metrics.txt").split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield


@pytest.fixture()
def mock_tikv_metrics():
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: get_mock_metrics("mock_tikv_metrics.txt").split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield


@pytest.fixture(scope="session")
def tidb_instance():
    return {'prometheus_url': "http://{}:{}/metrics".format(HOST, TIDB_PORT), 'namespace': 'tidb'}


@pytest.fixture(scope="session")
def tikv_instance():
    return {'prometheus_url': "http://{}:{}/metrics".format(HOST, TIKV_PORT), 'namespace': 'tikv'}


@pytest.fixture(scope="session")
def pd_instance():
    return {'prometheus_url': "http://{}:{}/metrics".format(HOST, PD_PORT), 'namespace': 'pd'}


def get_mock_metrics(filename):
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(f_name, 'r') as f:
        text_data = f.read()
    return text_data
