from datadog_checks.aqua import AquaCheck


def test_check(aggregator, instance):
    check = AquaCheck('aqua', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
