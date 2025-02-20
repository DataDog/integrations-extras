import os

import mock
import pytest

from .support import ENDPOINT

CHECK = 'redis_cloud'


@pytest.fixture(scope='session')
def dd_environment():
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
    print(os.path.join(os.path.dirname(__file__), 'data', 'metrics.txt'))
    with mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: text_data.split("\n"),
            headers={'Content-Type': "text/plain"},
        ),
    ):
        yield
