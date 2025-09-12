import os
import ssl
from copy import deepcopy
from typing import Any, Callable, Dict  # noqa: F401

import pytest

from datadog_checks.base.errors import ConfigurationError

# from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.redis_enterprise_prometheus.check import RedisEnterprisePrometheusCheck

from .support import CHECK, DEFAULT_METRICS, EPHEMERAL, ERSATZ_INSTANCE, INSTANCE, METRICS_MAP

ssl._create_default_https_context = ssl._create_unverified_context


@pytest.mark.unit
def test_instance_additional_check(aggregator, dd_run_check, mock_http_response):
    # Load test data
    f_name = os.path.join(os.path.dirname(__file__), "data", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()

    # Mock the HTTP response
    mock_http_response(text_data, status_code=200, headers={"Content-Type": "text/plain"})

    # add additional metric groups for validation
    additional_metric_groups = ["REDIS2.DISK", "REDIS2.REPLICATION", "REDIS2.SEARCH"]
    instance = deepcopy(INSTANCE)
    instance["extra_metrics"] = additional_metric_groups

    check = RedisEnterprisePrometheusCheck(CHECK, {}, [instance])

    dd_run_check(check)

    metrics = DEFAULT_METRICS + additional_metric_groups
    for g in metrics:
        for m in METRICS_MAP[g]:
            if m in EPHEMERAL[0]:
                continue
            aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check(f"{RedisEnterprisePrometheusCheck.__NAMESPACE__}.more_groups", count=1)


@pytest.mark.unit
def test_instance_all_additional_check(aggregator, dd_run_check, mock_http_response):
    # Load test data
    f_name = os.path.join(os.path.dirname(__file__), "data", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()

    # Mock the HTTP response
    mock_http_response(text_data, status_code=200, headers={"Content-Type": "text/plain"})

    # add additional metric groups for validation
    additional_metric_groups = [
        "REDIS2.REPLICATION",
        "REDIS2.LDAP",
        "REDIS2.NETWORK",
        "REDIS2.MEMORY",
        "REDIS2.X509",
        "REDIS2.DISK",
        "REDIS2.FILESYSTEM",
        "REDIS2.PROCESS",
        "REDIS2.PRESSURE",
        "REDIS2.SEARCH",
    ]

    instance = deepcopy(INSTANCE)
    instance["extra_metrics"] = additional_metric_groups

    check = RedisEnterprisePrometheusCheck(CHECK, {}, [instance])

    dd_run_check(check)

    metrics = DEFAULT_METRICS + additional_metric_groups
    for g in metrics:
        for m in METRICS_MAP[g]:
            if m in EPHEMERAL[0]:
                continue
            aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check(f"{RedisEnterprisePrometheusCheck.__NAMESPACE__}.more_groups", count=1)


@pytest.mark.unit
def test_instance_exclude_metrics(aggregator, dd_run_check, mock_http_response):
    # Load test data
    f_name = os.path.join(os.path.dirname(__file__), "data", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()

    # Mock the HTTP response
    mock_http_response(text_data, status_code=200, headers={"Content-Type": "text/plain"})

    # validate exclude_metrics are not present in metrics
    exclude_metrics = ["endpoint_client_connections", "redis_server_up"]
    instance = deepcopy(INSTANCE)
    instance["exclude_metrics"] = exclude_metrics

    check = RedisEnterprisePrometheusCheck(CHECK, {}, [instance])

    dd_run_check(check)

    for em in exclude_metrics:
        assert f"{RedisEnterprisePrometheusCheck.__NAMESPACE__}.{em}" not in aggregator.metric_names


@pytest.mark.e2e
def test_end_to_end():
    pass


@pytest.mark.unit
def test_instance_invalid_group_check(aggregator, dd_run_check, mock_http_response):
    # Load test data
    f_name = os.path.join(os.path.dirname(__file__), "data", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()

    # Mock the HTTP response
    mock_http_response(text_data, status_code=200, headers={"Content-Type": "text/plain"})

    instance = deepcopy(INSTANCE)
    instance["metric_groups"] = ["redis.bogus", "redis.raft"]

    check = RedisEnterprisePrometheusCheck(CHECK, {}, [instance])

    try:
        dd_run_check(check)
    except ConfigurationError:
        assert True

    aggregator.assert_service_check(f"{RedisEnterprisePrometheusCheck.__NAMESPACE__}.more_groups", count=0)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    # Load test data
    f_name = os.path.join(os.path.dirname(__file__), "data", "metrics.txt")
    with open(f_name, "r") as f:
        text_data = f.read()

    # Mock the HTTP response
    mock_http_response(text_data, status_code=200, headers={"Content-Type": "text/plain"})

    instance = deepcopy(ERSATZ_INSTANCE)
    instance.pop("openmetrics_endpoint")

    check = RedisEnterprisePrometheusCheck(CHECK, {}, [instance])

    try:
        dd_run_check(check)
    except ConfigurationError:
        assert True
    except Exception:
        assert True

    aggregator.assert_service_check(f"{RedisEnterprisePrometheusCheck.__NAMESPACE__}.node_imaginary", count=0)
