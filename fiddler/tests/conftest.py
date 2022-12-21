import os
import pytest
from datadog_checks.dev import docker_run, get_docker_hostname, get_here

URL = 'http://{}:9000'.format(get_docker_hostname())
FIDDLER_API_KEY = 'eSZ7iyuywmODU0ftl1GvqzuxLNE8mxFWovBftInhqY4'
INSTANCE = {"urlF": "https://demo.fiddler.ai", "fiddler_api_key": FIDDLER_API_KEY, "organization": "demo", 'url': URL}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(get_here(), 'docker-compose.yml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished
    with docker_run(compose_file, endpoints=[URL]):
        yield instance


@pytest.fixture(scope='session')
def e2e_instance():
    return {
        "url": "https://demo.fiddler.ai",
        "fiddler_api_key": FIDDLER_API_KEY,
        "organization": "demo",
    }


@pytest.fixture
def instance():
    return INSTANCE.copy()
