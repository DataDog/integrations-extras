import os

from datadog_checks.dev import get_docker_hostname, get_here
from datadog_checks.dev.http import MockResponse

PORT = 2019
HERE = get_here()
HOST = get_docker_hostname()
METRICS_URL = f"http://{HOST}:{PORT}/metrics"
INSTANCE = {
    "openmetrics_endpoint": METRICS_URL,
}
MOCKED_INSTANCE = {
    "openmetrics_endpoint": "http://caddy:2019/metrics",
}


def mock_http_responses(url, **_params):
    mapping = {
        'http://caddy:2019/metrics': 'metrics.txt',
    }

    metrics_file = mapping.get(url)

    if not metrics_file:
        raise Exception(f"url `{url}` not registered")

    with open(os.path.join(HERE, 'fixtures', metrics_file)) as f:
        return MockResponse(content=f.read())
