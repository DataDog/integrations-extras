import os

import pytest

from datadog_checks.dev import docker_run

from . import common


@pytest.fixture(scope="session", params=["neo4j4", "neo4j5"])
def dd_environment(request):
    with docker_run(
        os.path.join(common.HERE, "docker", request.param, "docker-compose.yaml"),
        log_patterns=["Remote interface available at"],
        endpoints=[common.METRICS_URL],
    ):
        yield


@pytest.fixture(scope="session")
def instance():
    return {
        "openmetrics_endpoint": common.METRICS_URL,
        "neo4j_version": common.NEO4J_IMAGE,
        "neo4j_dbs": ["neo4j", "system"],
    }
