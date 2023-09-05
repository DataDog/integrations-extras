import os

from datadog_checks.amazon_msk.metrics import JMX_METRICS_MAP, JMX_METRICS_OVERRIDES
from datadog_checks.dev import get_docker_hostname, get_here
from datadog_checks.dev.utils import read_file

HERE = get_here()
PORT = 8080
HOST = get_docker_hostname()

COMPOSE_FILE = os.path.join(HERE, 'docker', 'docker-compose.yaml')

E2E_METADATA = {
    'post_install_commands': ['pip install /home/mock_boto3'],
    'docker_volumes': ['{}:/home/mock_boto3'.format(os.path.join(HERE, 'mock_boto3'))],
}

METRICS = [
]

def get_metrics_fixture_path(exporter_type):
    return os.path.join(HERE, 'docker', 'exporter_{}'.format(exporter_type), 'metrics.txt')


def read_api_fixture():
    return read_file(os.path.join(HERE, 'fixtures', 'list_nodes.json'))


def read_e2e_api_fixture():
    return read_file(os.path.join(HERE, 'mock_boto3', 'boto3', 'list_nodes.json'))
