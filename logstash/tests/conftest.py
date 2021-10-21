import os

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckEndpoints

from .common import HERE, URL


@pytest.fixture(scope='session', params=["logstash5", "logstash6", "logstash7"])
def dd_environment(request):
    with docker_run(
        compose_file=os.path.join(HERE, "docker", request.param, "docker-compose.yml"),
        conditions=[CheckEndpoints(URL, wait=20)],
    ):
        yield
