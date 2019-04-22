import pytest

from .common import HOST, PORT


@pytest.fixture
def instance():
    return {'url': 'http://{}:{}'.format(HOST, PORT), 'api_user': 'foo', 'password': 'bar', 'tags': ['foo:bar']}
