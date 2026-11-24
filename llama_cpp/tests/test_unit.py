import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.llama_cpp import LlamaCppCheck

from .common import BAD_HOSTNAME_INSTANCE, EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.unit]


def test_connect_exception(dd_run_check, aggregator):
    with pytest.raises(Exception, match="Failed to resolve 'invalid-hostname'|Max retries exceeded"):
        check = LlamaCppCheck('llama_cpp', {}, [BAD_HOSTNAME_INSTANCE])
        dd_run_check(check)

    aggregator.assert_service_check('llama_cpp.openmetrics.health', ServiceCheck.CRITICAL)


def test_check_mock_llama_cpp_metrics(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)

    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_symmetric_inclusion=True)
    aggregator.assert_service_check('llama_cpp.openmetrics.health', ServiceCheck.OK)


def test_tokens_max_is_a_gauge(dd_run_check, aggregator, check, mock_prometheus_metrics):
    dd_run_check(check)

    aggregator.assert_metric('llama_cpp.tokens_max', value=57, metric_type=aggregator.GAUGE)
    aggregator.assert_metric('llama_cpp.prompt_tokens_per_second', value=454.057, metric_type=aggregator.GAUGE)


def test_empty_instance(dd_run_check):
    with pytest.raises(
        Exception,
        match='\nopenmetrics_endpoint\n  Field required',
    ):
        check = LlamaCppCheck('llama_cpp', {}, [{}])
        dd_run_check(check)
