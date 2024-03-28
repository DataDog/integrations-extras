import os

import pytest

from datadog_checks.dev import docker_run

from . import common


@pytest.fixture(scope='session')
def dd_environment(request):
    with docker_run(
        os.path.join(common.HERE, 'docker', 'docker-compose.yaml'),
        log_patterns=['run start_be.sh'],
        endpoints=[common.FE_METRICS_URL, common.BE_METRICS_URL],
    ):
        yield


@pytest.fixture(scope='session')
def fe_instance():
    return {
        'openmetrics_endpoint': common.FE_METRICS_URL,
        'namespace': "celerdata",
    }


@pytest.fixture(scope='session')
def be_instance():
    return {
        'openmetrics_endpoint': common.BE_METRICS_URL,
        'namespace': "celerdata",
    }
