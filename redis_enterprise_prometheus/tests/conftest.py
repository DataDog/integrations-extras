import pytest

from .support import ENDPOINT

CHECK = "redis_enterprise_prometheus"


@pytest.fixture(scope="session")
def dd_environment():
    instances = {"instances": [{"openmetrics_endpoint": ENDPOINT}, {"tls_verify": "false"}]}

    yield instances


@pytest.fixture(scope="session")
def instance():
    return {"openmetrics_endpoint": ENDPOINT, "tags": ["instance"], "tls_verify": "false"}
