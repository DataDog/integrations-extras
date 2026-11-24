import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.hugging_face_tei import HuggingFaceTeiCheck

from .common import EMBEDDING_METRICS


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check_metrics(dd_run_check, aggregator, instance):
    check = HuggingFaceTeiCheck('hugging_face_tei', {}, [instance])
    dd_run_check(check)

    for metric_name in EMBEDDING_METRICS:
        aggregator.assert_metric(metric_name, at_least=1)

    aggregator.assert_service_check('hugging_face_tei.openmetrics.health', ServiceCheck.OK)
