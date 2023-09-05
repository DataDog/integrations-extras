import os

from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()
PORT = 8080
HOST = get_docker_hostname()

COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')


def get_metrics_fixture_path(exporter_type):
    return os.path.join(HERE, 'docker', 'exporter_{}'.format(exporter_type), 'metrics.txt')
