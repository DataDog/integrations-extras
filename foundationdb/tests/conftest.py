
import json
import time
import os
import pytest

from datadog_checks.dev import WaitFor, docker_run, run_command

from .common import E2E_INIT_CONFIG

INSTANCE = {'use_sudo': False}
CONFIG = {'init_config': E2E_INIT_CONFIG, 'instances': [INSTANCE]}
HERE = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope='session')
def dd_environment():
    compose_file = os.path.join(HERE, 'docker', 'docker-compose.yaml')
    with docker_run(compose_file=compose_file, conditions=[WaitFor(create_database)]):
        yield CONFIG

@pytest.fixture
def instance():
    return INSTANCE

def create_database():
    base_status = run_command('docker exec fdb-0 fdbcli --exec "status json"', capture=True, check=True)
    status = json.loads(base_status.stdout)
    if not status.get('client').get('database_status').get('available'):
        run_command('docker exec fdb-0 fdbcli --exec "configure new single memory"', capture=True, check=True)
    i = 0
    is_healthy = False
    has_latency_stats = False
    # Wait for 1 minute for the database to become available for testing
    while i < 60 and not (is_healthy and has_latency_stats):
        time.sleep(1)
        base_status = run_command('docker exec fdb-0 fdbcli --exec "status json"', capture=True, check=True)
        status = json.loads(base_status.stdout)
        is_healthy = status.get('cluster').get('data').get('state').get('name') == 'healthy'
        has_latency_stats = False
        for _, process in status.get('cluster').get('processes').items():
            for role in process.get('roles'):
                if "commit_latency_statistics" in role:
                    has_latency_stats = True
        i += 1
