import pytest

INSTANCE = {"tags": ["foo:bar"]}


@pytest.fixture(scope='session')
def dd_environment():
    yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()
