import pytest

from .common import MOCK_INSTANCE


@pytest.fixture(scope='session')
def dd_environment():
    instances = {'instances': [MOCK_INSTANCE]}

    yield instances


@pytest.fixture
def instance():
    return MOCK_INSTANCE.copy()
