import logging

import pytest

from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.tidb import TiDBCheck

from .conftest import required_instance
from .expected import EXPECTED_PD_METRICS, EXPECTED_TIDB_METRICS, EXPECTED_TIKV_METRICS

TEST_CHECK_NAME = "test_config_check"


# test transforming tidb check config to openmetrics check config


@pytest.mark.unit
def test_config():
    with pytest.raises((CheckException, ConfigurationError)):
        TiDBCheck(TEST_CHECK_NAME, {}, [{}])

    # this should not fail
    TiDBCheck(TEST_CHECK_NAME, {}, [required_instance])


@pytest.mark.unit
def test_transform():
    check = TiDBCheck(TEST_CHECK_NAME, {}, [required_instance])
    ensure_tidb = False
    ensure_tikv = False
    ensure_pd = False
    for i in check.instances:
        if i.get("prometheus_url") == "http://localhost:10080/metrics" and i.get("namespace") == "tidb":
            ensure_tidb = True
        if i.get("prometheus_url") == "http://localhost:20180/metrics" and i.get("namespace") == "tikv":
            ensure_tikv = True
        if i.get("prometheus_url") == "http://localhost:2379/metrics" and i.get("namespace") == "pd":
            ensure_pd = True
    assert ensure_tidb and ensure_tikv and ensure_pd, "transforming config failed."


@pytest.mark.unit
def test_customized_metrics(customized_metric_instance):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [customized_metric_instance])
    target = None
    for i in check.instances:
        if i.get("namespace") == "tidb" and i.get("prometheus_url") == "http://localhost:10080/metrics":
            target = i
            break
    assert (
        target.get("metrics")[0].get("tidb_tikvclient_rawkv_cmd_seconds") == "tikvclient_rawkv_cmd_seconds"
    ), "customized metric failed."


# test metric mapping for each component


@pytest.mark.unit
def test_tidb_metrics(aggregator, tidb_instance, mock_tidb_metrics):
    _test_metrics(aggregator, tidb_instance, EXPECTED_TIDB_METRICS)


@pytest.mark.unit
def test_pd_metrics(aggregator, pd_instance, mock_pd_metrics):
    _test_metrics(aggregator, pd_instance, EXPECTED_PD_METRICS)


@pytest.mark.unit
def test_tikv_metrics(aggregator, tikv_instance, mock_tikv_metrics):
    _test_metrics(aggregator, tikv_instance, EXPECTED_TIKV_METRICS)


def _test_metrics(aggregator, instance, expected_metrics):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [required_instance])
    check.check(instance)

    logging.debug(expected_metrics)

    for metric in expected_metrics:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check(check.__NAMESPACE__ + '.' + instance['namespace'] + '.prometheus.health', count=1)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_metric_type=False)
