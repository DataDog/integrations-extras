import pytest
import requests

from datadog_checks.dev import WaitFor, docker_run

from . import common


def ping_traefik():
    response = requests.get('{}://{}:{}/health'.format(common.SCHEME, common.HOST, common.PORT))
    response.raise_for_status()

    # Trigger a 404
    requests.get('http://{}:800'.format(common.HOST))


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(common.DOCKER_COMPOSE_FILE, conditions=[WaitFor(ping_traefik)]):
        yield common.INSTANCE


@pytest.fixture
def instance():
    return common.INSTANCE


@pytest.fixture
def instance_bad():
    return common.INSTANCE_BAD


@pytest.fixture
def instance_invalid():
    return common.INSTANCE_INVALID
