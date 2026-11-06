import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.vllm_production_stack import VllmProductionStackCheck

from .common import BAD_HOSTNAME_INSTANCE, EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = VllmProductionStackCheck('vllm_production_stack', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('vllm_production_stack.openmetrics.health', ServiceCheck.CRITICAL)


def test_check_mock_vllm_production_stack_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)

    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)
    aggregator.assert_service_check('vllm_production_stack.openmetrics.health', ServiceCheck.OK)


def test_labels(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)

    endpoint_tag = 'endpoint:' + check.instance['openmetrics_endpoint']
    aggregator.assert_metric(
        'vllm_production_stack.backend.healthy',
        value=1,
        metric_type=aggregator.GAUGE,
        tags=[endpoint_tag, 'backend:http://127.0.0.1:18101'],
    )
    aggregator.assert_metric(
        'vllm_production_stack.request.errors.count',
        value=3,
        tags=[endpoint_tag, 'backend:http://127.0.0.1:18102', 'model:stories', 'error_type:ClientConnectorError'],
    )
    aggregator.assert_metric_has_tag('vllm_production_stack.request.latency.count', 'status:error')
    aggregator.assert_metric_has_tag('vllm_production_stack.requests.incoming.count', 'model:stories')


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = VllmProductionStackCheck('vllm_production_stack', {}, [{}])
        dd_run_check(check)
