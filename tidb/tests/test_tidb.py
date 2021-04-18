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
def test_metrics(aggregator):
    check = TiDBCheck(TEST_CHECK_NAME, {}, [MOCK_INSTANCE])
    check.check(MOCK_INSTANCE)

    expected_metrics = dict(EXPECTED_TIDB_METRICS)
    expected_metrics.update(EXPECTED_PD_METRICS)
    expected_metrics.update(EXPECTED_TIKV_METRICS)

    for metric_name, metric_type in expected_metrics.items():
        aggregator.assert_metric(metric_name, metric_type=metric_type)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_openmetrics_error(aggregator):
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
