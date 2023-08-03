import os

import pytest

from datadog_checks.dev.http import MockResponse

from .common import MOCKED_MARIADB_SKYSQL_INSTANCE

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    token_path = os.path.join(HERE, 'fixtures', 'token.txt')
    with open(token_path, 'r') as t:
        data = t.read()
    return {
        'openmetrics_endpoint': MOCKED_MARIADB_SKYSQL_INSTANCE.get("mariadb_skysql_endpoint"),
        'extra_headers': {'Authorization': data},
    }


@pytest.fixture
def instance_invalid_endpoint():
    return {'openmetrics_endpoint': 'http://invalid_endpoint', 'extra_headers': {"Authorization": "Bearer none"}}


def mock_http_responses(url, **_params):
    mapping = {
        MOCKED_MARIADB_SKYSQL_INSTANCE.get("mariadb_skysql_endpoint"): 'mariadb_skysql_metrics.txt',
    }

    metrics_file = mapping.get(url)

    if not metrics_file:
        pytest.fail(f"url `{url}` not registered")

    with open(os.path.join(HERE, 'fixtures', metrics_file)) as f:
        print("Getting metrics content from {}".format(metrics_file))
        return MockResponse(content=f.read())
