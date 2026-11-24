import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.xinference import XinferenceCheck

from .common import SUPERVISOR_METRICS, WORKER_METRICS


@pytest.mark.integration
def test_check_metrics(dd_run_check, aggregator, dd_environment):
    for instance in dd_environment['instances']:
        check = XinferenceCheck('xinference', {}, [instance])
        dd_run_check(check)

    for metric_name in SUPERVISOR_METRICS + WORKER_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)
    aggregator.assert_service_check('xinference.openmetrics.health', ServiceCheck.OK)
