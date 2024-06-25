import ssl
from copy import deepcopy
from typing import Any, Callable, Dict  # noqa: F401

import pytest

from datadog_checks.base.errors import ConfigurationError
from datadog_checks.redis_cloud.check import RedisCloudCheck

from .support import CHECK, DEFAULT_METRICS, EPHEMERAL, ERSATZ_INSTANCE, INSTANCE, METRICS_MAP

ssl._create_default_https_context = ssl._create_unverified_context


@pytest.mark.unit
def test_instance_additional_check(aggregator, dd_run_check, mock_http_response):
    # add additional metric groups for validation
    additional_metric_groups = [
        'RDSC.LISTENER',
    ]
    instance = deepcopy(INSTANCE)
    instance['metric_groups'] = additional_metric_groups

    check = RedisCloudCheck(CHECK, {}, [instance])

    dd_run_check(check)

    metrics = DEFAULT_METRICS + additional_metric_groups
    for g in metrics:
        for m in METRICS_MAP[g]:
            if m in EPHEMERAL:
                continue
            # print(f'metric: {m}')
            aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('rdsc.more_groups', count=1)


@pytest.mark.unit
def test_instance_invalid_group_check(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(INSTANCE)
    instance['metric_groups'] = ['redis.bogus', 'redis.raft']

    check = RedisCloudCheck(CHECK, {}, [instance])

    try:
        dd_run_check(check)
    except ConfigurationError:
        assert True
    except Exception:
        assert True

    aggregator.assert_service_check('rdsc.group_bogus', count=0)


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

    aggregator.assert_service_check('rdsc.node_imaginary', count=0)
