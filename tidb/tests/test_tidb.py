import pytest
from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics

from datadog_checks.tidb import TiDBCheck
from .conftest import TEST_CHECK_NAME
from .expected import (
    EXPECTED_TIDB_METRICS,
    EXPECTED_PD_METRICS,
    EXPECTED_TIKV_METRICS,
    EXPECTED_CHECKS,
)


@pytest.mark.unit
def test_config(instance):
    with pytest.raises((CheckException, ConfigurationError)):
        TiDBCheck(TEST_CHECK_NAME, {}, [{}])

    # this should not fail
    TiDBCheck(TEST_CHECK_NAME, {}, [instance])


@pytest.mark.unit
def test_tidb_metrics(aggregator, instance, mock_tidb_metrics):
    _test_metrics(aggregator, instance, EXPECTED_TIDB_METRICS)


@pytest.mark.unit
def test_pd_metrics(aggregator, instance, mock_pd_metrics):
    _test_metrics(aggregator, instance, EXPECTED_PD_METRICS)


@pytest.mark.unit
def test_tikv_metrics(aggregator, instance, mock_tikv_metrics):
    _test_metrics(aggregator, instance, EXPECTED_TIKV_METRICS)


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [instance])
    with pytest.raises(Exception):
        check.check(instance)

        for check_name in EXPECTED_CHECKS:
            aggregator.assert_service_check(
                check_name,
                status=TiDBCheck.CRITICAL,
                tags=[],
                count=1,
            )


def _test_metrics(aggregator, instance, expected_metrics):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [instance])
    check.check(instance)

    for metric in expected_metrics:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('tidb_cluster.prometheus.health', count=1)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
