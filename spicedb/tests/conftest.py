import os
import pytest

from datadog_checks.dev import docker_run, get_here

from .util import HOST, PORT


@pytest.fixture(scope="session")
def dd_environment(instance):
    env_vars = {"SPICEDB_GRPC_PRESHARED_KEY": "some random key"}

    with docker_run(
        os.path.join(get_here(), "docker", "docker-compose.yml"),
        env_vars=env_vars,
        endpoints=instance["openmetrics_endpoint"],
        conditions=None,
    ):
        yield instance


@pytest.fixture
def instance(scope="session"):
    return {
        "openmetrics_endpoint": "http://{}:{}/metrics".format(HOST, PORT),
        "histogram_buckets_as_distributions": True,
        "tags": ["cluster:spicedb-cluster", "node:1"],
    }
