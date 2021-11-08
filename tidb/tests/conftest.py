import os

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


# Mock metrics


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


# TiDB check instances for different components


@pytest.fixture(scope="session")
def tidb_instance():
    return {
        'tidb_metric_url': "http://{}:{}/metrics".format(HOST, TIDB_PORT),
        'max_returned_metrics': "10000",
        'tags': ['tidb_cluster_name:test'],
    }


@pytest.fixture(scope="session")
def pd_instance():
    return {
        'pd_metric_url': "http://{}:{}/metrics".format(HOST, PD_PORT),
        'max_returned_metrics': "10000",
        'tags': ['tidb_cluster_name:test'],
    }


@pytest.fixture(scope="session")
def tikv_instance():
    return {
        'tikv_metric_url': "http://{}:{}/metrics".format(HOST, TIKV_PORT),
        'max_returned_metrics': "10000",
        'tags': ['tidb_cluster_name:test'],
    }


# Excepted results


EXPECTED_TIDB = {
    'metrics': {
        'tidb_cluster.tidb_executor_statement_total': [
            'tidb_cluster_component:tidb',
            'type:Use',
            'tidb_cluster_name:test',
        ],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:10080/metrics',
            'tidb_cluster_component:tidb',
            'tidb_cluster_name:test',
        ],
    },
}

EXPECTED_PD = {
    'metrics': {
        'tidb_cluster.pd_cluster_tso': ['dc:global', 'tidb_cluster_component:pd', 'type:tso', 'tidb_cluster_name:test'],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:2379/metrics',
            'tidb_cluster_component:pd',
            'tidb_cluster_name:test',
        ],
    },
}

EXPECTED_TIKV = {
    'metrics': {
        'tidb_cluster.tikv_allocator_stats': ['tidb_cluster_component:tikv', 'type:metadata', 'tidb_cluster_name:test'],
    },
    'service_check': {
        'tidb_cluster.prometheus.health': [
            'endpoint:http://localhost:20180/metrics',
            'tidb_cluster_component:tikv',
            'tidb_cluster_name:test',
        ],
    },
}


# Integration test docker-compose environment


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'compose', 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(
        compose_file,
        endpoints=[
            "http://{}:{}/metrics".format(HOST, TIDB_PORT),
            "http://{}:{}/metrics".format(HOST, TIKV_PORT),
            "http://{}:{}/metrics".format(HOST, PD_PORT),
        ],
        sleep=3,
    ):
        yield
