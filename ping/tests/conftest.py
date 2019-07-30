import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield instance


@pytest.fixture
def instance():
    return {}
