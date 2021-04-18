from datadog_checks.base.errors import CheckException, ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics

from datadog_checks.tidb import TiDBCheck
from .common import *

TEST_CHECK_NAME = 'tidb_check_test'


@pytest.mark.unit
def test_config():
    with pytest.raises((CheckException, ConfigurationError)):
        TiDBCheck(TEST_CHECK_NAME, {}, [{}])

    # this should not fail
    TiDBCheck(TEST_CHECK_NAME, {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_tidb_metrics(aggregator, instance, mock_audit_metrics):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for metric_name, metric_type in EXPECTED_TIDB_METRICS.items():
        aggregator.assert_metric(metric_name, metric_type=metric_type)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


# @pytest.mark.unit
# def test_pd_metrics(aggregator, instance, mock_controller_metrics):
#     check = GatekeeperCheck('gatekeeper', {}, [MOCK_INSTANCE])
#     check.check(MOCK_INSTANCE)
#
#     for metric_name, metric_type in EXPECTED_CONTROLLER_METRICS.items():
#         aggregator.assert_metric(metric_name, metric_type=metric_type)
#
#     aggregator.assert_all_metrics_covered()
#     aggregator.assert_metrics_using_metadata(get_metadata_metrics())
#
#
# @pytest.mark.unit
# def test_tikv_metrics(aggregator, instance, mock_controller_metrics):
#     check = GatekeeperCheck('gatekeeper', {}, [MOCK_INSTANCE])
#     check.check(MOCK_INSTANCE)
#
#     for metric_name, metric_type in EXPECTED_CONTROLLER_METRICS.items():
#         aggregator.assert_metric(metric_name, metric_type=metric_type)
#
#     aggregator.assert_all_metrics_covered()
#     aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_check(aggregator, instance, mock_audit_metrics):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    for check_name in EXPECTED_CHECKS:
        aggregator.assert_service_check(
            check_name,
            status=TiDBCheck.OK,
            tags=[],
            count=1,
        )


@pytest.mark.unit
def test_openmetrics_error(aggregator, instance, error_instance):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [MOCK_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_INSTANCE)

        for check_name in EXPECTED_CHECKS:
            aggregator.assert_service_check(
                check_name,
                status=TiDBCheck.CRITICAL,
                tags=[],
                count=1,
            )
