from datadog_checks.ping import PingCheck


def test_check(aggregator, instance):
    check = PingCheck('ping', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
