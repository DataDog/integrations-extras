import pytest

# Don't forget to import your integration!
from datadog_checks.fluent_bit import FluentBitCheck
from datadog_checks.base import ConfigurationError


@pytest.mark.unit
def test_empty_config():
    instance = {}
    c = FluentBitCheck('fluent-bit',{},[instance])

    # empty instance, should fail
    with pytest.raises(ConfigurationError):
        c.check(instance)


@pytest.mark.unit
def test_config():
    instance = {'prometheus_url': 'http://%%host%%:2020/api/v1/metrics/prometheus'}
    c = FluentBitCheck('fluent-bit',{},[instance])

    # only the url, this should not fail
    c.check(instance)



# Testing known metric value using docker - valid response
@pytest.mark.integrations
@pytest.mark.usefixtures('dd_environment_pass')
def test_good_response(aggregator, instance_pass):
    c = FluentBitCheck('fluent-bit', {}, [instance_pass])

    c.check(instance_pass)

    METRICS = {
        "fluentbit.filter.add_record": 0,
        "fluentbit.filter.drop_record": 0,
        "fluentbit.input.bytes": 0,
        "fluentbit.input.record": 0,
        "fluentbit.output.errors": 0,
        "fluentbit.output.proc_bytes": 0,
        "fluentbit.output.proc_records": 0,
        "fluentbit.output.retries_failed": 0,
        "fluentbit.output.retries": 0,
    }
    for metric, value in METRICS.items():
        aggregator.assert_metric(name=metric, value=value)

    aggregator.assert_all_metrics_covered()
