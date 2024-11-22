import pytest
import os

from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = f'http://{get_docker_hostname()}:9598/metrics'
INSTANCE = {'openmetrics_endpoint': URL}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker/docker-compose.yaml')
    with docker_run(compose_file, endpoints=[URL]):
        yield INSTANCE


@pytest.fixture
def instance():
    return {'openmetrics_endpoint': 'http://127.0.0.1:9598/metrics'}
