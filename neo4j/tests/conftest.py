import os

import pytest

from datadog_checks.dev.docker import docker_run

from .common import NEO4J_AUTH, NEO4J_MINIMAL_CONFIG

HERE = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    instance = NEO4J_MINIMAL_CONFIG
    envs = {'NEO4J_VERSION': os.environ['NEO4J_VERSION'], 'NEO4J_AUTH': NEO4J_AUTH}
    with docker_run(
        os.path.join(DOCKER_DIR, 'docker-compose.yaml'),
        env_vars=envs,
        log_patterns=['Remote interface available at'],
    ):
        yield instance
