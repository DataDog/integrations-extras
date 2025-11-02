import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.e2e
def test_metrics(dd_agent_check):
    aggregator = dd_agent_check(check_rate=True)

    aggregator.assert_metric("grafana.build_info")
    aggregator.assert_service_check('grafana.openmetrics.health', ServiceCheck.OK, at_least=1)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


# def test_metrics_with_extra(dd_agent_check, instance_with_extra_metrics):
#     aggregator = dd_agent_check(instance_with_extra_metrics)
#     aggregator.assert_metric('grafana.alerting.scheduler_behind_seconds')
#     aggregator.assert_metric('grafana.alerting.alertmanager_alerts')
#     aggregator.assert_metric('grafana.database.conn_idle')
#     aggregator.assert_service_check('grafana.openmetrics.health', ServiceCheck.OK, count=1)
#     assert_service_checks(aggregator)
#     for m in METRICS:
#         aggregator.assert_metric(m)
#     aggregator.assert_all_metrics_covered()
