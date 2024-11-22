import pytest

from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.ocient import OcientCheck


@pytest.mark.e2e
def test_check(dd_run_check, aggregator, instance):
    check = OcientCheck('ocient', {}, [instance])

    dd_run_check(check)

    metadata_metrics = [k for k in get_metadata_metrics()]
    for metric in metadata_metrics:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())