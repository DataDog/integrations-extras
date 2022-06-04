import os

import pytest

from datadog_checks.dev import docker_run

from . import common


@pytest.fixture(scope='session')
def dd_environment(instance):
    with docker_run(
        os.path.join(common.HERE, 'docker', 'docker-compose.yaml'),
        env_vars={'NEO4J_IMAGE': f'neo4j:{common.NEO4J_VERSION}-enterprise'},
        log_patterns=['Remote interface available at'],
        endpoints=[common.METRICS_URL],
    ):
        yield instance


@pytest.fixture(scope='session')
def instance():
    return {
        'openmetrics_endpoint': common.METRICS_URL,
        'neo4j_version': common.NEO4J_VERSION,
        'neo4j_dbs': ['neo4j', 'system'],
    }
