import os

import pytest
import time

from datadog_checks.dev import docker_run

HERE = os.path.dirname(os.path.abspath(__file__))
docker_compose = os.path.join(HERE, 'docker-compose.yml')


@pytest.fixture(scope='session', autouse=False)
def spin_up_traefik():
    with docker_run(docker_compose):
        # Needed to give time to the container to be ready.
        time.sleep(5)
        yield
