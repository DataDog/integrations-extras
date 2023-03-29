import os
import time

import pytest

from datadog_checks.dev import docker_run, get_here

HOST = 'localhost:8888/pass'
TOKEN = 'abcdefghijklmnop'
URL = 'http://localhost:8888/pass/admin/api.php'
INSTANCE = {'host': HOST, 'token': TOKEN}


@pytest.fixture(scope='session')
def dd_environment_pass():
    compose_file = os.path.join(get_here(), 'docker-compose.yaml')

    with docker_run(compose_file, endpoints=[URL]):
        time.sleep(10)
        yield instance_pass


@pytest.fixture
def instance_pass():
    return INSTANCE.copy()
