from datadog_checks.dev import get_docker_hostname

HOST = get_docker_hostname()
VECTOR_HTTP_PORT = '9598'
VECTOR_METRICS_URL = f'http://{HOST}:{VECTOR_HTTP_PORT}/metrics'
