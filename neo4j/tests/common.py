import os

from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()
HOST = get_docker_hostname()
PORT = '2004'
METRICS_URL = f'http://{HOST}:{PORT}/metrics'
NEO4J_VERSION = os.getenv('NEO4J_VERSION')
