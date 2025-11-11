import copy
from pathlib import Path

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckEndpoints

INSTANCE = {'openmetrics_endpoint': 'http://localhost:3000/metrics'}
EXTRA_METRICS = [
    {'grafana_alerting_alertmanager_alerts': 'alerting.alertmanager_alerts'},
    {'grafana_database_conn_idle': 'database.conn_idle'},
]
INSTANCE_WITH_EXTRA_METRICS = {**INSTANCE, 'extra_metrics': EXTRA_METRICS}


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = str(Path(__file__).parent.absolute() / 'docker' / 'docker-compose.yaml')
    conditions = [
        CheckEndpoints(INSTANCE["openmetrics_endpoint"]),
    ]
    with docker_run(compose_file, conditions=conditions):
        yield {
            'instances': [INSTANCE],
        }


@pytest.fixture
def instance():
    return copy.deepcopy(INSTANCE)


@pytest.fixture
def instance_with_extra_metrics():
    return copy.deepcopy(INSTANCE_WITH_EXTRA_METRICS)
