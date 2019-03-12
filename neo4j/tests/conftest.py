import json
import os

import pytest
import requests

from datadog_checks.dev import docker_run
from .common import NEO4J_MINIMAL_CONFIG

HERE = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    instance = NEO4J_MINIMAL_CONFIG
    with docker_run(
        os.path.join(DOCKER_DIR, 'docker-compose.yaml'),
        log_patterns='Remote interface available at'
    ):
        headers_sent = {'Content-Type': 'application/json'}
        url = '{}:{}/user/{}/password'.format(instance['neo4j_url'], instance['port'], instance['user'])
        r = requests.post(
            url,
            data=json.dumps({'password': instance['password']}),
            auth=(instance['user'], 'neo4j'), headers=headers_sent)
        r.raise_for_status()
        yield instance
