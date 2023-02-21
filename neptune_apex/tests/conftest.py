import pytest

INSTANCE = {"address": "http://127.0.0.1"}


@pytest.fixture(scope="session")
def dd_environment():
    yield INSTANCE.copy()


@pytest.fixture
def instance():
    return INSTANCE.copy()
