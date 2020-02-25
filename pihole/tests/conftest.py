import os
import pytest
import time


from datadog_checks.dev import docker_run, get_here

HOST = 'localhost'  # pihole docker containers bind to localhost for its functionality
URL = 'http://localhost/admin/api.php'
INSTANCE = {'host': HOST}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker-compose.yaml')

    with docker_run(compose_file, endpoints=[URL]):
        time.sleep(10)  # see readme.md in this directory
        yield instance


@pytest.fixture
def instance():
    return INSTANCE.copy()
