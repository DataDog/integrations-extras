
import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield

@pytest.fixture
def instance():
    return {
        'url': 'https://ps1.stonebranchdev.cloud/resources/metrics',
        'username': 'observability',
        'password': 'deadman26'
    }