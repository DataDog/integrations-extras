import ssl
import itertools
from typing import Any, Callable, Dict  # noqa: F401

from copy import deepcopy

import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.redis_enterprise.check import RedisEnterpriseCheck

from .support import CHECK, DEFAULT_METRICS, ADDITIONAL_METRICS, INSTANCE, ERSATZ_INSTANCE, EPHEMERAL, METRICS_MAP

ssl._create_default_https_context = ssl._create_unverified_context


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_instance_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    check = RedisEnterpriseCheck('redis_enterprise', {}, [instance])
    dd_run_check(check)

    metrics_list = []
    for g in DEFAULT_METRICS:
        metrics_list.extend(METRICS_MAP[g])
    for m in metrics_list:
        if m in EPHEMERAL:
            continue
        aggregator.assert_metric(m)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
def test_default_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    check = RedisEnterpriseCheck('redis_enterprise', {}, [instance])
    dd_run_check(check)

    metrics_list = []
    for g in DEFAULT_METRICS:
        metrics_list.extend(METRICS_MAP[g])
    for m in metrics_list:
        if m in EPHEMERAL:
            continue
        aggregator.assert_metric(m)

    # aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None

    instance = deepcopy(ERSATZ_INSTANCE)
    instance.update({'tls_verify': 'false'})
    check = RedisEnterpriseCheck('redis_enterprise', {}, [instance])

    dd_run_check(check)
    aggregator.assert_service_check('rdse.can_connect', RedisEnterpriseCheck.CRITICAL)


@pytest.mark.unit
def test_instance_additional_check(aggregator, dd_run_check, mock_http_response):
    # add additional metric groups for validation
    additional_metric_groups = [
        'RDSE.LISTENER',
    ]
    instance = deepcopy(INSTANCE)
    instance['metric_groups'] = additional_metric_groups

    check = RedisEnterpriseCheck(CHECK, {}, [instance])

    dd_run_check(check)

    metrics = DEFAULT_METRICS + additional_metric_groups
    for g in metrics:
        for m in METRICS_MAP[g]:
            if m in EPHEMERAL:
                continue
            # print(f'metric: {m}')
            aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('rdse.more_groups', count=1)


# @pytest.mark.unit
# def test_instance_full_additional_check(aggregator, dd_run_check, mock_http_response):
#     instance = deepcopy(INSTANCE)
#     # add all additional metric groups for validation
#     instance['metric_groups'] = ADDITIONAL_METRICS
#
#     check = RedisEnterpriseCheck(CHECK, {}, [instance])
#
#     dd_run_check(check)
#
#     groups_to_check = ADDITIONAL_METRICS
#
#     for g in groups_to_check:
#         for m in METRICS_MAP[g]:
#             aggregator.assert_metric(m)
#
#     aggregator.assert_all_metrics_covered()
#     aggregator.assert_service_check('rdse.openmetrics.health', count=1)


@pytest.mark.unit
def test_instance_invalid_group_check(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(INSTANCE)
    instance['metric_groups'] = ['redis.bogus', 'redis.raft']

    check = RedisEnterpriseCheck(CHECK, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check('rdse.group_bogus', count=0)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(ERSATZ_INSTANCE)
    instance.pop('openmetrics_endpoint')

    check = RedisEnterpriseCheck(CHECK, {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(check)

    aggregator.assert_service_check('rdse.node_imaginary', count=0)


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check(aggregator, dd_run_check):

    instances = INSTANCE
    instances.update({'tls_verify': 'false'})

    check = RedisEnterpriseCheck(CHECK, {}, [instances])
    dd_run_check(check)

    metrics_list = []
    for g in DEFAULT_METRICS:
        metrics_list.extend(METRICS_MAP[g])
    for m in metrics_list:
        if m in EPHEMERAL:
            continue
        aggregator.assert_metric(m)

    aggregator.assert_all_metrics_covered()
