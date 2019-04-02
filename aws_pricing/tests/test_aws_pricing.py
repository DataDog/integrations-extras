import pytest

from datadog_checks.aws_pricing import AwsPricingCheck
from datadog_checks.errors import CheckException


def test_check_ok(aggregator, pricing_client, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services(['AmazonEC2'])
    pricing_client_stubber.stub_get_products([
        {
            'service_code': 'AmazonEC2',
            'term_code': 'YQHNG5NBWUE3D67S.4NA7Y494T4',
            'rate_code': 'YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7',
            'unit': 'Hrs',
            'price': '123'
        }
    ])
    pricing_client_stubber.activate()

    # Mock instance configuration
    instance = {'AmazonEC2': 'YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7'}

    # Run check
    check = AwsPricingCheck('aws_pricing', {}, {})
    check.check(instance, pricing_client)

    # Validate results
    aggregator.assert_metric('aws.pricing.amazonec2', 123)
    aggregator.assert_service_check('aws_pricing.all_good', AwsPricingCheck.OK)


def test_check_warning(aggregator, pricing_client, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services(['AmazonEC2'])
    pricing_client_stubber.stub_get_products([])
    pricing_client_stubber.activate()

    # Mock instance configuration
    instance = {'AmazonEC2': 'YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7'}

    # Run check
    check = AwsPricingCheck('aws_pricing', {}, {})
    check.check(instance, pricing_client)

    # Validate results
    aggregator.assert_service_check('aws_pricing.all_good', AwsPricingCheck.WARNING)


def test_check_exception(aggregator, pricing_client, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services(['AmazonEC2'])
    pricing_client_stubber.activate()

    # Run check and validate exception
    check = AwsPricingCheck('aws_pricing', {}, {})
    with pytest.raises(CheckException):
        check.check({}, pricing_client)
