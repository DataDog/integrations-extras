import pytest

from datadog_checks.mariadb_skysql import MariadbSkysqlCheck

from .common import MARIADB_SKYSQL_METRICS
from .conftest import mock_http_responses


@pytest.mark.unit
def test_check_mock_mariadb_skysql(dd_run_check, aggregator, instance, mocker):
    mocker.patch('requests.get', wraps=mock_http_responses)
    check = MariadbSkysqlCheck('skysql', {}, [instance])
    dd_run_check(check)
    print("Received the following metrics: ")
    print(" ".join(aggregator.metric_names))

    for metric in MARIADB_SKYSQL_METRICS:
        aggregator.assert_metric(metric, at_least=1)

    aggregator.assert_all_metrics_covered()
    # The below will fail until we update the metadata.csv
    # aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.integration
def test_invalid_endpoint(dd_run_check, aggregator, instance_invalid_endpoint):
    check = MariadbSkysqlCheck('skysql', {}, [instance_invalid_endpoint])
    with pytest.raises(Exception):
        dd_run_check(check)
    aggregator.assert_service_check('skysql.openmetrics.health', MariadbSkysqlCheck.CRITICAL, count=1)
