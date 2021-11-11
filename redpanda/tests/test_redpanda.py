from copy import deepcopy

import pytest

from datadog_checks.redpanda import RedpandaCheck

from .common import (
    INSTANCE_ADDITIONAL_GROUPS,
    INSTANCE_ADDITIONAL_METRICS,
    INSTANCE_DEFAULT_GROUPS,
    INSTANCE_DEFAULT_METRICS,
    MOCK_REDPANDA_INSTANCE,
    get_metrics,
)


@pytest.mark.unit
def test_instance_default_check(aggregator, dd_run_check, mock_http_response):
    c = RedpandaCheck('redpanda', {}, [MOCK_REDPANDA_INSTANCE])

    dd_run_check(c)

    for m in INSTANCE_DEFAULT_METRICS:
        aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
def test_instance_additional_check(aggregator, dd_run_check, mock_http_response):
    # add additional metric groups for validation
    additional_metric_groups = ['redpanda.alien', 'redpanda.raft']

    instance = deepcopy(MOCK_REDPANDA_INSTANCE)
    instance['metric_groups'] = additional_metric_groups

    c = RedpandaCheck('redpanda', {}, [instance])

    dd_run_check(c)

    metrics_to_check = get_metrics(INSTANCE_DEFAULT_GROUPS + additional_metric_groups)

    for m in metrics_to_check:
        aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('redpanda.openmetrics.health', count=1)


@pytest.mark.unit
def test_instance_full_additional_check(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(MOCK_REDPANDA_INSTANCE)
    instance['metric_groups'] = INSTANCE_ADDITIONAL_GROUPS

    c = RedpandaCheck('redpanda', {}, [instance])

    dd_run_check(c)

    metrics_to_check = INSTANCE_DEFAULT_METRICS + INSTANCE_ADDITIONAL_METRICS

    for m in metrics_to_check:
        aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('redpanda.openmetrics.health', count=1)


@pytest.mark.unit
def test_instance_invalid_group_check(aggregator, dd_run_check, mock_http_response):
    additional_metric_groups = ['redpanda.bogus', 'redpanda.raft']

    instance = deepcopy(MOCK_REDPANDA_INSTANCE)
    instance['metric_groups'] = additional_metric_groups

    c = RedpandaCheck('redpanda', {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(c)

    aggregator.assert_service_check('redpanda.openmetrics.health', count=0)


@pytest.mark.unit
def test_invalid_instance(aggregator, dd_run_check, mock_http_response):
    instance = deepcopy(MOCK_REDPANDA_INSTANCE)
    instance.pop('openmetrics_endpoint')

    c = RedpandaCheck('redpanda', {}, [instance])

    with pytest.raises(Exception):
        dd_run_check(c)

    aggregator.assert_service_check('redpanda.openmetrics.health', count=0)


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check(aggregator, dd_run_check):
    check = RedpandaCheck('redpanda', {}, [MOCK_REDPANDA_INSTANCE])
    dd_run_check(check)

    for m in INSTANCE_DEFAULT_METRICS:
        aggregator.assert_metric(m)
    aggregator.assert_all_metrics_covered()
