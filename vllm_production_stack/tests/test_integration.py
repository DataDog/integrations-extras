import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.vllm_production_stack import VllmProductionStackCheck

from .common import EXPECTED_PROMETHEUS_METRICS


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check_metrics(dd_run_check, aggregator, instance):
    check = VllmProductionStackCheck('vllm_production_stack', {}, [instance])
    dd_run_check(check)

    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)
    aggregator.assert_service_check('vllm_production_stack.openmetrics.health', ServiceCheck.OK)
