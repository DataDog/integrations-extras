from datadog_checks.unbound import UnboundCheck


def test_check(aggregator, instance):
    check = UnboundCheck('unbound', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
