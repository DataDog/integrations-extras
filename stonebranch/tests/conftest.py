
import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield

@pytest.fixture
def instance():
    return {
        'url': 'http://localhost:8080/uc',
        'username': 'test_user',
        'password': 'test_password'
    }