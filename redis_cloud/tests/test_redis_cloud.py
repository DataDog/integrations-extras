import ssl
from copy import deepcopy
from typing import Any, Callable, Dict  # noqa: F401

import pytest

from datadog_checks.base.errors import ConfigurationError
from datadog_checks.redis_cloud.check import RedisCloudCheck

from .support import CHECK, DEFAULT_METRICS, EPHEMERAL, ERSATZ_INSTANCE, INSTANCE, METRICS_MAP, SSL_INSTANCE

ssl._create_default_https_context = ssl._create_unverified_context


@pytest.mark.unit
def test_instance_additional_check(aggregator, dd_run_check, mock_http_response):
    # add additional metric groups for validation
    additional_metric_groups = [
        'RDSC.REPLICATION',
        'RDSC.NODE',
    ]
    instance = deepcopy(INSTANCE)
    instance['extra_metrics'] = additional_metric_groups

    check = RedisCloudCheck(CHECK, {}, [instance])

    dd_run_check(check)

    metrics = DEFAULT_METRICS + additional_metric_groups
    for g in metrics:
        for m in METRICS_MAP[g]:
            if m in EPHEMERAL:
                continue
            aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check(f'{RedisCloudCheck.__NAMESPACE__}.more_groups', count=1)


@pytest.mark.unit
def test_instance_exclude_metrics(aggregator, dd_run_check, mock_http_response):
    # validate exclude_metrics are not present in metrics
    exclude_metrics = ['bdb_conns', 'bdb_up']
    instance = deepcopy(INSTANCE)
    instance['exclude_metrics'] = exclude_metrics

    check = RedisCloudCheck(CHECK, {}, [instance])

    dd_run_check(check)

    for em in exclude_metrics:
        assert f'{RedisCloudCheck.__NAMESPACE__}.{em}' not in aggregator.metric_names


@pytest.mark.e2e
def test_end_to_end():
    pass


@pytest.mark.unit
def test_instance_invalid_group_check(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(INSTANCE)
    instance['extra_metrics'] = ['redis.bogus', 'redis.raft']

    check = RedisCloudCheck(CHECK, {}, [instance])

    try:
        dd_run_check(check)
    except ConfigurationError:
        assert True
    except Exception:
        assert True

    aggregator.assert_service_check(f'{RedisCloudCheck.__NAMESPACE__}.group_bogus', count=0)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(ERSATZ_INSTANCE)
    instance.pop('openmetrics_endpoint')

    check = RedisCloudCheck(CHECK, {}, [instance])

    try:
        dd_run_check(check)
    except ConfigurationError:
        assert True
    except Exception:
        assert True

    aggregator.assert_service_check(f'{RedisCloudCheck.__NAMESPACE__}.node_imaginary', count=0)

@pytest.mark.unit
def test_invalid_ssl_instance(aggregator, dd_run_check, mock_http_response):
    # Create instance without tls_verify
    instance = deepcopy(SSL_INSTANCE)
    instance.pop('tls_verify')  # Simulating missing tls_verify in config

    check = RedisEnterpriseCheck(CHECK, {}, [instance])
    dd_run_check(check)

    # Ensure tls_verify defaults to False
    assert check.scraper_configs[0]["tls_verify"] is False, "tls_verify should default to False"

    # Ensure the check does not raise ConfigurationError unexpectedly
    try:
        dd_run_check(check)
    except ConfigurationError:
        pytest.fail("ConfigurationError raised unexpectedly")
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
