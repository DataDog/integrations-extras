import pytest


INSTANCE = {
    "min_collection_interval": 15,
    "tags": ["region:local"],
}


@pytest.fixture(scope="session")
def dd_environment():
    yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()
