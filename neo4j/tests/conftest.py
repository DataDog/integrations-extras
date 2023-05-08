import os

import pytest

from datadog_checks.dev import docker_run

from . import common


@pytest.fixture(scope='session')
def dd_environment(instance):
    NEO4J_IMAGE = 'neo4j:4.4.18-enterprise'
    with docker_run(
        os.path.join(common.HERE, 'docker', 'docker-compose_v4.yaml'),
        env_vars={'NEO4J_IMAGE': f'{NEO4J_IMAGE}'},
        log_patterns=['Remote interface available at'],
        endpoints=[common.METRICS_URL],
    ):
        yield instance


@pytest.fixture(scope='session')
def dd_environment_v5(instance_neo4j5):
    NEO4J_IMAGE = 'neo4j:enterprise'
    with docker_run(
        os.path.join(common.HERE, 'docker', 'docker-compose_v5.yaml'),
        env_vars={'NEO4J_IMAGE': f'{NEO4J_IMAGE}'},
        log_patterns=['Remote interface available at'],
        endpoints=[common.METRICS_URL],
    ):
        yield instance_neo4j5


@pytest.fixture(scope='session')
def instance():
    return {
        'openmetrics_endpoint': common.METRICS_URL,
        'neo4j_version': common.NEO4J_VERSION,
        'neo4j_dbs': ['neo4j', 'system'],
    }


@pytest.fixture(scope='session')
def instance_neo4j5():
    return {
        'openmetrics_endpoint': common.METRICS_URL,
        'neo4j_version': common.NEO4J_VERSION,
        'neo4j_dbs': ['neo4j', 'system'],
    }
