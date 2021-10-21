import os

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckDockerLogs
from datadog_checks.dev.utils import load_jmx_config

from .common import HERE


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(HERE, 'docker', 'docker-compose.yml')
    with docker_run(compose_file, conditions=[CheckDockerLogs(compose_file, 'Resin/4.0.62 started -server')]):
        instance = load_jmx_config()
        yield instance, {'use_jmx': True}
