
import pytest

from datadog_checks.qdrant import QdrantCheck

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.base.constants import ServiceCheck
from tests.common import OM_METRICS


@pytest.mark.e2e
def test_emits_metrics(dd_run_check, aggregator, instance):
    check = QdrantCheck("qdrant", {}, [instance])
    dd_run_check(check)

    for metric in OM_METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check("qdrant.openmetrics.health", ServiceCheck.OK)
    aggregator.assert_service_check("qdrant.readyz.status", ServiceCheck.OK)
    aggregator.assert_service_check("qdrant.livez.status", ServiceCheck.OK)
