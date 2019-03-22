import os
import pytest

from datadog_checks.dev.docker import docker_run, get_docker_hostname

from .common import HOST, DOCKER_DIR, registry_file_path


@pytest.fixture(scope='session')
def dd_environment():
    instance = {
        'stats_endpoint': 'http://{}:5066/stats'.format(HOST),
        'registry_file_path': registry_file_path('empty')
    }
    with docker_run(
        os.path.join(DOCKER_DIR, 'docker-compose.yaml'),
        endpoints='http://{}:5066'.format(HOST)
    ):
        yield instance
