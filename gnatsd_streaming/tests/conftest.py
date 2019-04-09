import os

import pytest

from datadog_checks.dev import TempDir, docker_run
from datadog_checks.dev.docker import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    with TempDir() as nats_dir:
        env_vars = {'TEMP_DIR': nats_dir}
        with docker_run(
            os.path.join(DOCKER_DIR, 'docker-compose.yml'), env_vars=env_vars, log_patterns='test.channel3'
        ):
            yield


@pytest.fixture
def instance():
    return {'host': 'http://{}'.format(HOST), 'port': 8222, 'pagination_limit': 1}
