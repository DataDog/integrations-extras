import os

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.utils import load_jmx_config

from .common import HERE, HOST


@pytest.fixture(scope="session")
def dd_environment():
    with docker_run(os.path.join(HERE, 'docker', 'docker-compose.yml')):
        instance = load_jmx_config()
        #instance['instances'][0]['host'] = HOST
        yield instance, {'use_jmx': True}
