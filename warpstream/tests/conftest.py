# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
import pytest

from .common import URL, INSTANCE
from datadog_checks.dev import docker_run, get_docker_hostname, get_here

@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return INSTANCE.copy()

@pytest.fixture(scope='session')
def instance():
    return INSTANCE.copy()

@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file, endpoints=[f"{URL}/api/v1/status"]):
        yield INSTANCE
