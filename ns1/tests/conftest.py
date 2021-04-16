import pytest

CONFIG = {
    'api_endpoint': 'https://my.nsone.net',
    # The api authentication key.
    'api_key': 'svgRdvxF6XpWtqXGBJi7',
    'metrics': {'qps': [{"test.com": None}], 'usage': [{"test.com": None}], 'pulsar': None, 'ddi': None},
}


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return CONFIG


@pytest.fixture
def instance_empty():
    return {}
