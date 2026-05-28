import os

import pytest

try:
    from datadog_checks.dev import docker_run, get_docker_hostname, get_here

    HERE = get_here()
    HOST = get_docker_hostname()
    MOCKOON_PORT = 3002
    HAS_DATADOG_DEV = True
except ImportError:
    HAS_DATADOG_DEV = False


@pytest.fixture(scope='session')
def dd_environment():
    if not HAS_DATADOG_DEV:
        yield
        return

    compose_file = os.path.join(HERE, "docker", "docker-compose.yml")
    with docker_run(
        compose_file,
        log_patterns=["Server started"],
    ):
        yield {
            "huntress_api_key": "hk_testpublickey",
            "huntress_secret_key": "hs_testsecretkey",
            "log_queries": [{"esql_query": "FROM logs"}],
            "huntress_base_url": f"http://{HOST}:{MOCKOON_PORT}",
            "enrich_with_org_tags": True,
            "org_cache_ttl_seconds": 3600,
            "min_collection_interval": 60,
            "max_pages_per_run": 10,
            "tags": ["source:huntress", "env:test"],
        }


@pytest.fixture
def instance():
    return {
        "huntress_api_key": "test_api_key",
        "huntress_secret_key": "test_secret_key",
        "log_queries": [{"esql_query": "FROM logs"}],
        "enrich_with_org_tags": False,
        "min_collection_interval": 900,
        "max_pages_per_run": 100,
    }
