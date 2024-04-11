import os

import mock
import pytest

# import subprocess
# import requests
# from datadog_checks.dev import docker_run, get_here
from datadog_checks.dev import get_here

# from .support import CONFTEST, ENDPOINT
from .support import ENDPOINT

CHECK = 'redis_enterprise'
CWD = get_here()
DOCKER_DIR = os.path.join(CWD, 'docker')
SETUP = os.path.join(CWD, 'setup.sh')


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(DOCKER_DIR, 'docker-compose.yaml')

    # This does 3 things:
    #
    # 1. Spins up the services defined in the compose file
    # 2. Waits for the url to be available before running the tests
    # 3. Tears down the services when the tests are finished

    print(f'>>> spinning up docker: {compose_file}')
    # with docker_run(compose_file, endpoints=[CONFTEST]):
    #     response = requests.get(ENDPOINT, verify=False)
    #     # we have to run 'setup.sh' first - it might take a while...
    #     if response.status_code != 200:
    #         print('>>> running set up')
    #         subprocess.run([SETUP])
    #     instances = {'instances': [{'openmetrics_endpoint': ENDPOINT}, {'tls_verify': 'false'}]}
    #
    #     yield instances
    instances = {'instances': [{'openmetrics_endpoint': ENDPOINT}, {'tls_verify': 'false'}]}

    yield instances


@pytest.fixture(scope='session')
def instance():
    return {'openmetrics_endpoint': ENDPOINT, 'tags': ['instance'], 'tls_verify': 'false'}


@pytest.fixture()
def mock_http_response():
    f_name = os.path.join(os.path.dirname(__file__), 'data', 'metrics.txt')
    with open(f_name, 'r') as f:
        text_data = f.read()
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: text_data.split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield
