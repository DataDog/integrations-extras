from datadog_checks.aws_pricing import AwsPricingCheck


def test_check(aggregator, instance):
    check = AwsPricingCheck('aws_pricing', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
