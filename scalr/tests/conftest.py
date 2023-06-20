import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {"url": "http://acc_name.localhost", "access_token": "test"}
