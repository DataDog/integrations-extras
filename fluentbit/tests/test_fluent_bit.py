import pytest

from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.fluentbit import FluentBitCheck

METRICS = [
    'fluentbit.input.records.count',
    'fluentbit.input.bytes.count',
    'fluentbit.filter.add_records.count',
    'fluentbit.filter.drop_records.count',
    'fluentbit.output.proc_records.count',
    'fluentbit.output.proc_bytes.count',
    'fluentbit.output.errors.count',
    'fluentbit.output.retries.count',
    'fluentbit.output.retries_failed.count',
    'fluentbit.output.retried_records.count',
    'fluentbit.output.dropped_records.count',
    'fluentbit.build_info',
]


def test_check(dd_run_check, aggregator, instance, mock_data):
    check = FluentBitCheck('fluent_bit', {}, [instance])
    dd_run_check(check)

    for m in METRICS:
        aggregator.assert_metric(m)

    tags = [f'endpoint:{instance["metrics_endpoint"]}']

    aggregator.assert_metric('fluentbit.input.records.count', count=2)
    aggregator.assert_metric('fluentbit.input.bytes.count', count=2)
    aggregator.assert_metric('fluentbit.output.proc_records.count', count=1, value=64, tags=tags + ['name:stdout.0'])
    aggregator.assert_metric('fluentbit.output.proc_bytes.count', count=1, value=3104)
    aggregator.assert_metric('fluentbit.build_info', tags=tags + ['version:1.9.1', 'edition:Community'])

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_check_integration(dd_run_check, aggregator, instance):
    check = FluentBitCheck('fluent_bit', {}, [instance])
    dd_run_check(check)

    for m in METRICS:
        aggregator.assert_metric(m)
