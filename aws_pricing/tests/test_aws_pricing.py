from datadog_checks.aws_pricing import AwsPricingCheck


def test_check_ok(aggregator, instance_ok):
    check = AwsPricingCheck('aws_pricing', {}, {})
    check.check(instance_ok)

    aggregator.assert_metric('aws.pricing.amazonec2')
    aggregator.assert_metric('aws.pricing.amazoncloudfront')
    aggregator.assert_service_check('aws_pricing.all_good', AwsPricingCheck.OK)


def test_check_warning(aggregator, instance_warning):
    check = AwsPricingCheck('aws_pricing', {}, {})
    check.check(instance_warning)

    aggregator.assert_metric('aws.pricing.amazoncloudfront')
    aggregator.assert_service_check('aws_pricing.all_good', AwsPricingCheck.WARNING)
