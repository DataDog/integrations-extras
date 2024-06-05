from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()
HOST = get_docker_hostname()
FE_HTTP_PORT = '8030'
FE_METRICS_URL = f'http://{HOST}:{FE_HTTP_PORT}/metrics'
BE_HTTP_PORT = '8040'
BE_METRICS_URL = f'http://{HOST}:{BE_HTTP_PORT}/metrics'
