from datadog_checks.dev import get_docker_hostname

HOST = get_docker_hostname()
PORT = '8082'
METRICS_URL = f'http://{HOST}:{PORT}/metrics'
