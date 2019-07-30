import pytest


@pytest.fixture(scope='function')
def dd_environment(instance):
    yield instance


@pytest.fixture
def instance():
    instance = {
        'host': '127.0.0.1',
        'tags': ["ping1", "ping2"]
    }
    return instance


@pytest.fixture
def empty_instance():
    instance = {}
    return instance


@pytest.fixture
def incorrect_ip_instance():
    instance = {'host': '124.0.0.1'}
    return instance
