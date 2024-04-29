import ssl
from copy import deepcopy
from typing import Any, Callable, Dict  # noqa: F401

import pytest

from datadog_checks.redis_cloud.check import RedisCloudCheck

from .support import CHECK, DEFAULT_METRICS, EPHEMERAL, ERSATZ_INSTANCE, INSTANCE, METRICS_MAP

ssl._create_default_https_context = ssl._create_unverified_context


@pytest.mark.unit
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    instance = deepcopy(ERSATZ_INSTANCE)
    instance.update({'tls_verify': 'false'})
    check = RedisCloudCheck('redis_cloud', {}, [instance])

    dd_run_check(check)
    aggregator.assert_service_check('rdsc.can_connect', RedisCloudCheck.CRITICAL)


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
            print(f'metric: {m}')
            if m in EPHEMERAL:
                continue
            aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('rdsc.more_groups', count=1)


@pytest.mark.unit
def test_instance_invalid_group_check(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(INSTANCE)
    instance['metric_groups'] = ['redis.bogus', 'redis.raft']

    check = RedisCloudCheck(CHECK, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check('rdsc.group_bogus', count=0)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(ERSATZ_INSTANCE)
    instance.pop('openmetrics_endpoint')

    check = RedisCloudCheck(CHECK, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check('rdsc.node_imaginary', count=0)
