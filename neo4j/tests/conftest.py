import os

import pytest
import requests

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import WaitFor

DOCKER_DIR = os.path.join(get_here(), 'docker')
INSTANCE = {
    'host': get_docker_hostname(),
    'port': 2004,
    'neo4j_version': os.environ['NEO4J_VERSION'],
}


def ensure_prometheus_endpoint_is_accessable():
    instance = INSTANCE
    url = 'http://{}:{}/metrics'.format(instance.get('host'), instance.get('port'))
    response = requests.get(url)
    response.raise_for_status()


@pytest.fixture(scope='session')
def dd_environment():
    instance = INSTANCE
    envs = {'NEO4J_VERSION': os.environ['NEO4J_VERSION']}
    with docker_run(
        os.path.join(DOCKER_DIR, 'docker-compose.yaml'),
        env_vars=envs,
        log_patterns=['Remote interface available at'],
        conditions=[WaitFor(ensure_prometheus_endpoint_is_accessable)],
    ):
        yield instance


@pytest.fixture
def instance():
    return INSTANCE.copy()
