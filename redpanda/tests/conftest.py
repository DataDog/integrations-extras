import os

import mock
import pytest

from datadog_checks.dev import docker_run, get_here

from .common import INSTANCE_URL

HERE = get_here()
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(DOCKER_DIR, 'docker-compose.yaml')

    with docker_run(compose_file, log_patterns=[r'Successfully started Redpanda!']):
        instances = {'instances': [{'openmetrics_endpoint': INSTANCE_URL}]}
        yield instances


@pytest.fixture(scope='session')
def db_instance():
    return {'openmetrics_endpoint': INSTANCE_URL, 'tags': ['instance_test']}


@pytest.fixture()
def mock_http_response():
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', 'redpanda_metrics.txt')
    with open(f_name, 'r') as f:
        text_data = f.read()
    with mock.patch(
        'requests.Session.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: text_data.split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield
