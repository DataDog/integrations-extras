from datadog_checks.contrastsecurity import ContrastsecurityCheck


def test_check(aggregator, instance):
    check = ContrastsecurityCheck('contrastsecurity', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
