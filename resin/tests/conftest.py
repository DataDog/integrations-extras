import os
import time

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.utils import load_jmx_config

from .common import HERE


@pytest.fixture(scope="session")
def dd_environment():
    with docker_run(os.path.join(HERE, 'docker', 'docker-compose.yml')):
        instance = load_jmx_config()
        time.sleep(15)  # TODO: use better strategy, e.g. waiting for specific logs
        yield instance, {'use_jmx': True}
