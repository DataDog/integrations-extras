import logging

import pytest

from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.tidb import TiDBCheck

from .conftest import required_instances, tidb_instance, pd_instance, tikv_instance
from .expected import EXPECTED_PD_METRICS, EXPECTED_TIDB_METRICS, EXPECTED_TIKV_METRICS

TEST_CHECK_NAME = "test_config_check"


# test transforming tidb check config to openmetrics check config


@pytest.mark.unit
def test_config():
    with pytest.raises((CheckException, ConfigurationError)):
        TiDBCheck(TEST_CHECK_NAME, {}, [{}])

    # this should not fail
    TiDBCheck(TEST_CHECK_NAME, {}, [required_instances])


@pytest.mark.unit
def test_transform():
    check = TiDBCheck(TEST_CHECK_NAME, {}, [required_instances])
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
def test_tidb_metrics(aggregator, mock_tidb_metrics):
    _test_metrics(aggregator, tidb_instance, EXPECTED_TIDB_METRICS)


@pytest.mark.unit
def test_pd_metrics(aggregator, mock_pd_metrics):
    _test_metrics(aggregator, pd_instance, EXPECTED_PD_METRICS)


@pytest.mark.unit
def test_tikv_metrics(aggregator, mock_tikv_metrics):
    _test_metrics(aggregator, tikv_instance, EXPECTED_TIKV_METRICS)


def _test_metrics(aggregator, instance, expected_metrics):
    # required_instance is only for initializing TiDBCheck object, not for the actual check process
    check = TiDBCheck(TEST_CHECK_NAME, {}, [required_instances])
    _check_and_assert(aggregator, instance, expected_metrics, check)


def _check_and_assert(agg, ins, expected, c):
    c.check(ins)

    logging.debug(expected)

    for metric in expected:
        agg.assert_metric(metric)

    agg.assert_all_metrics_covered()
    agg.assert_service_check(c.__NAMESPACE__ + '.' + ins['namespace'] + '.prometheus.health', count=1)
    agg.assert_metrics_using_metadata(get_metadata_metrics(), check_metric_type=False)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_cluster_metrics(aggregator, instance):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [required_instances])
    ensure_tidb = False
    ensure_tikv = False
    ensure_pd = False
    for instance in check.instances:
        # ensure correctness for 4 components (tidb, pd, tikv)
        if instance.get("namespace") == "tidb":
            _check_and_assert(aggregator, instance, EXPECTED_TIDB_METRICS, check)
            ensure_tidb = True
        elif instance.get("namespace") == "pd":
            _check_and_assert(aggregator, instance, EXPECTED_PD_METRICS, check)
            ensure_tikv = True
        elif instance.get("namespace") == "tikv":
            _check_and_assert(aggregator, instance, EXPECTED_TIKV_METRICS, check)
            ensure_pd = True
        else:
            pass
    assert ensure_tidb and ensure_tikv and ensure_pd, "each 4 components must be covered!"
