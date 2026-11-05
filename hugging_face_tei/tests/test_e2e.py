import pytest

from datadog_checks.base.constants import ServiceCheck

from .common import EMBEDDING_METRICS


@pytest.mark.e2e
def test_e2e_service_check_ok(dd_agent_check, aggregator, instance):
    dd_agent_check(instance)
    aggregator.assert_service_check('hugging_face_tei.openmetrics.health', ServiceCheck.OK)


@pytest.mark.e2e
def test_e2e_assert_metrics(dd_agent_check, aggregator, instance):
    dd_agent_check(instance, rate=True)

    for metric in EMBEDDING_METRICS:
        aggregator.assert_metric(metric, at_least=1)

    aggregator.assert_all_metrics_covered()
