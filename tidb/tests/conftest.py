import os
from copy import deepcopy

import mock
import pytest

from datadog_checks.dev import get_docker_hostname, get_here

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


def get_mock_metrics(filename):
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(f_name, 'r') as f:
        text_data = f.read()
    return text_data


# tidb check instance


required_instance = {
    'tidb_metric_url': "http://{}:{}/metrics".format(HOST, TIDB_PORT),
    'tikv_metric_url': "http://{}:{}/metrics".format(HOST, TIKV_PORT),
    'pd_metric_url': "http://{}:{}/metrics".format(HOST, PD_PORT),
}


@pytest.fixture(scope="session")
def full_instance():
    base = deepcopy(required_instance)
    base.update(
        {
            "tiflash_metric_url": "http://{}:{}/metrics".format(HOST, TIFLASH_PORT),
            "tiflash_proxy_metric_url": "http://{}:{}/metrics".format(HOST, TIFLASH_PROXY_PORT),
            "ticdc_metric_url": "http://{}:{}/metrics".format(HOST, TICDC_PORT),
            "dm_master_metric_url": "http://{}:{}/metrics".format(HOST, DM_MASTER_PORT),
            "dm_worker_metric_url": "http://{}:{}/metrics".format(HOST, DM_WORKER_PORT),
            "pump_metric_url": "http://{}:{}/metrics".format(HOST, PUMP_PORT),
        }
    )
    return base


@pytest.fixture(scope="session")
def customized_metric_instance():
    base = deepcopy(required_instance)
    base.update({"tidb_customized_metrics": [{"tidb_tikvclient_rawkv_cmd_seconds": "tikvclient_rawkv_cmd_seconds"}]})
    return base


# openmetrics check instances


@pytest.fixture(scope="session")
def tidb_instance():
    return {'prometheus_url': "http://{}:{}/metrics".format(HOST, TIDB_PORT), 'namespace': 'tidb'}


@pytest.fixture(scope="session")
def tikv_instance():
    return {'prometheus_url': "http://{}:{}/metrics".format(HOST, TIKV_PORT), 'namespace': 'tikv'}


@pytest.fixture(scope="session")
def pd_instance():
    return {'prometheus_url': "http://{}:{}/metrics".format(HOST, PD_PORT), 'namespace': 'pd'}
