import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "prometheus_url": "http://localhost:54127//metrics",
        "namespace": "calico",
        "metrics": ["felix_active_local_endpoints"],
    }
