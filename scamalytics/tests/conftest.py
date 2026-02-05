import pytest


@pytest.fixture(scope="session", autouse=True)
def dd_environment():
    yield
