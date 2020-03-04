import os
import time

import pytest

from datadog_checks.dev import docker_run, get_here

HOST1 = 'localhost:8888/pass'
HOST2 = 'localhost:8888/pass'

URL1 = 'http://localhost:8888/pass/admin/api.php'
URL2 = 'http://localhost:8888/fail/admin/api.php'
INSTANCE1 = {'host': HOST1}
INSTANCE2 = {'host': HOST2}


@pytest.fixture(scope='session')
def dd_environment_pass():
    compose_file = os.path.join(get_here(), 'docker-compose.yaml')

    with docker_run(compose_file, endpoints=[URL1]):
        time.sleep(10)
        yield instance_pass


@pytest.fixture(scope='session')
def dd_environment_fail():
    compose_file = os.path.join(get_here(), 'docker-compose.yaml')

    with docker_run(compose_file, endpoints=[URL1]):
        time.sleep(10)
        yield instance_fail


@pytest.fixture
def instance_pass():
    return INSTANCE1.copy()


@pytest.fixture
def instance_fail():
    return INSTANCE2.copy()
