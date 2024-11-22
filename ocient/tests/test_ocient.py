from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.ocient import OcientCheck
from pytest import mark


@mark.e2e
def test_check(dd_run_check, aggregator, instance):
    check = OcientCheck("ocient", {}, [instance])

    dd_run_check(check)

    metadata_metrics = list(get_metadata_metrics().keys())
    for metric in metadata_metrics:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
