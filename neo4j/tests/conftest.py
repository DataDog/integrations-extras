import os

import pytest
import requests

from datadog_checks.dev.conditions import WaitFor
from datadog_checks.dev.docker import docker_run

from .common import NEO4J_MINIMAL_CONFIG

HERE = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(HERE, 'docker')


def init_user():
    instance = NEO4J_MINIMAL_CONFIG
    url = '{}:{}/user/{}/password'.format(instance['neo4j_url'], instance['port'], instance['user'])
    r = requests.post(url, json={'password': instance['password']}, auth=(instance['user'], 'neo4j'))
    r.raise_for_status()


@pytest.fixture(scope='session')
def dd_environment():
    instance = NEO4J_MINIMAL_CONFIG
    with docker_run(
        os.path.join(DOCKER_DIR, 'docker-compose.yaml'),
        log_patterns='Remote interface available at',
        conditions=[WaitFor(init_user)],
    ):
        yield instance
