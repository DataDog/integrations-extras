import os
import time

import pytest

from datadog_checks.dev import docker_run, get_here

HOST = 'localhost:8888/pass'
URL = 'http://localhost:8888/pass/admin/api.php'
INSTANCE = {'host': HOST, 'web_password': 'test'}


V6_HOST = 'localhost:8888'
V6_URL = 'http://localhost:8888/api/auth'
V6_INSTANCE = {'host': V6_HOST, 'v6_check': True, 'web_password': 'test'}


@pytest.fixture(scope='session')
def dd_environment_pass():
    compose_file = os.path.join(get_here(), 'docker-compose.yaml')

    with docker_run(compose_file, endpoints=[URL]):
        time.sleep(10)
        yield instance_pass


@pytest.fixture
def instance_pass():
    return INSTANCE.copy()


@pytest.fixture(scope='session')
def v6_dd_environment_pass():
    compose_file = os.path.join(get_here(), 'docker-compose.yaml')

    with docker_run(compose_file, endpoints=[V6_URL]):
        time.sleep(10)
        yield v6_instance_pass


@pytest.fixture
def v6_instance_pass():
    return V6_INSTANCE.copy()
