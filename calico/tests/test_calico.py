from typing import Any, Dict

from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.calico import CalicoCheck
from datadog_checks.dev.utils import get_metadata_metrics


def test_check(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = CalicoCheck('calico', {}, [instance])
    check.check(instance)
    aggregator.assert_metric("calico.felix_active_local_endpoints", metric_type=0)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
