import os
from copy import deepcopy

import mock
import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

HERE = get_here()
HOST = get_docker_hostname()
TIDB_PORT = 10080
TIKV_PORT = 20180
PD_PORT = 2379
TIFLASH_PROXY_PORT = 20292
TIFLASH_PORT = 8234
TICDC_PORT = 8301
DM_MASTER_PORT = 8261
DM_WORKER_PORT = 8262
PUMP_PORT = 8250


# mock metrics


@pytest.fixture()
def mock_tidb_metrics():
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: _get_mock_metrics("mock_tidb_metrics.txt").split("\n"),
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
            iter_lines=lambda **kwargs: _get_mock_metrics("mock_pd_metrics.txt").split("\n"),
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
            iter_lines=lambda **kwargs: _get_mock_metrics("mock_tikv_metrics.txt").split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield


def _get_mock_metrics(filename):
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(f_name, 'r') as f:
        text_data = f.read()
    return text_data


# tidb check instance


_instance = {
    'tidb_metric_url': "http://{}:{}/metrics".format(HOST, TIDB_PORT),
    'tikv_metric_url': "http://{}:{}/metrics".format(HOST, TIKV_PORT),
    'pd_metric_url': "http://{}:{}/metrics".format(HOST, PD_PORT),
}


@pytest.fixture(scope="session")
def required_instances():
    base = deepcopy(_instance)
    base.update({'max_returned_metrics': "10000"})
    return base


@pytest.fixture(scope="session")
def customized_metric_instance():
    base = deepcopy(required_instances)
    base.update({"tidb_customized_metrics": [{"tidb_tikvclient_rawkv_cmd_seconds": "tikvclient_rawkv_cmd_seconds"}]})
    return base


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'compose', 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file, endpoints=list(_instance.values()), sleep=3):
        yield
