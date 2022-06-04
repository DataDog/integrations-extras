import os

import mock
import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = f'http://{get_docker_hostname()}:2020/api/v1/metrics/prometheus'
INSTANCE = {'url': URL}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker/docker-compose.yaml')
    with docker_run(compose_file, endpoints=[URL]):
        yield INSTANCE


@pytest.fixture
def instance():
    return {
        'metrics_endpoint': 'http://127.0.0.1:2020/api/v1/metrics/prometheus',
    }


@pytest.fixture()
def mock_data():
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', 'metrics.txt')
    with open(f_name, 'r') as f:
        text_data = f.read()
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200, iter_lines=lambda **kwargs: text_data.split('\n'), headers={'Content-Type': 'text/plain'}
        ),
    ):
        yield
