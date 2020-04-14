import pytest
from mock import Mock, patch

from datadog_checks.aws_pricing import AwsPricingCheck
from datadog_checks.base.errors import CheckException


def test_check_ok(aggregator, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services_response(['AmazonEC2'])
    pricing_client_stubber.stub_get_products_response(
        [
            {
                'service_code': 'AmazonEC2',
                'term_code': 'YQHNG5NBWUE3D67S.4NA7Y494T4',
                'rate_code': 'YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7',
                'unit': 'Hrs',
                'price': '123',
            }
        ]
    )

    # Mock instance configuration
    instance = {'region_name': 'us-east-1', 'AmazonEC2': ['YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7']}

    # Run check
    with pricing_client_stubber, patch('boto3.client', Mock(return_value=pricing_client_stubber.get_client())):
        check = AwsPricingCheck('aws_pricing', {})
        check.check(instance)

    # Validate results
    aggregator.assert_metric('aws.pricing.amazonec2', 123)
    aggregator.assert_all_metrics_covered()

    aggregator.assert_service_check('aws_pricing.status', AwsPricingCheck.OK)
    assert len(aggregator.service_checks('aws_pricing.status')) == 1, 'Too many service checks were emitted'


def test_check_warning(aggregator, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services_response(['AmazonEC2'])
    pricing_client_stubber.stub_get_products_response([])

    # Mock instance configuration
    instance = {'region_name': 'us-east-1', 'AmazonEC2': ['YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7']}

    # Run check
    with pricing_client_stubber, patch('boto3.client', Mock(return_value=pricing_client_stubber.get_client())):
        check = AwsPricingCheck('aws_pricing', {})
        check.check(instance)

    # Validate results
    missing_rate_codes = {'AmazonEC2': ['YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7']}
    message = 'Pricing data not found for these service rate codes: {}'.format(missing_rate_codes)
    aggregator.assert_service_check('aws_pricing.status', AwsPricingCheck.WARNING, message=message)
    assert len(aggregator.service_checks('aws_pricing.status')) == 1, 'Too many service checks were emitted'


def test_check_checkexception(aggregator, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services_response(['AmazonEC2'])

    # Run check and validate exception
    with pricing_client_stubber, patch('boto3.client', Mock(return_value=pricing_client_stubber.get_client())):
        check = AwsPricingCheck('aws_pricing', {})
        with pytest.raises(CheckException):
            check.check({})

    # Validate results
    aggregator.assert_service_check('aws_pricing.status', AwsPricingCheck.CRITICAL)
    assert len(aggregator.service_checks('aws_pricing.status')) == 1, 'Too many service checks were emitted'


def test_check_describe_services_clienterror(aggregator, pricing_client_stubber):
    # Mock client responses
    code = 'TEST_DESCRIBE_SERVICES_ERROR_CODE'
    message = 'TEST_DESCRIBE_SERVICES_ERROR_MESSAGE'
    pricing_client_stubber.stub_describe_services_error(code, message)

    # Mock instance configuration
    instance = {'region_name': 'us-east-1', 'AmazonEC2': ['YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7']}

    # Run check
    with pricing_client_stubber, patch('boto3.client', Mock(return_value=pricing_client_stubber.get_client())):
        with pytest.raises(CheckException):
            check = AwsPricingCheck('aws_pricing', {})
            check.check(instance)

    # Validate results
    message = 'An error occurred ({}) when calling the DescribeServices operation: {}'.format(code, message)
    aggregator.assert_service_check('aws_pricing.status', AwsPricingCheck.CRITICAL, message=message)
    assert len(aggregator.service_checks('aws_pricing.status')) == 1, 'Too many service checks were emitted'


def test_check_get_products_clienterror(aggregator, pricing_client_stubber):
    # Mock client responses
    pricing_client_stubber.stub_describe_services_response(['AmazonEC2'])
    code = 'TEST_GET_PRODUCTS_ERROR_CODE'
    message = 'TEST_GET_PRODUCTS_ERROR_MESSAGE'
    pricing_client_stubber.stub_get_products_error(code, message)

    # Mock instance configuration
    instance = {'region_name': 'us-east-1', 'AmazonEC2': ['YQHNG5NBWUE3D67S.4NA7Y494T4.6YS6EN2CT7']}

    # Run check
    with pricing_client_stubber, patch('boto3.client', Mock(return_value=pricing_client_stubber.get_client())):
        with pytest.raises(CheckException):
            check = AwsPricingCheck('aws_pricing', {})
            check.check(instance)

    # Validate results
    message = 'An error occurred ({}) when calling the GetProducts operation: {}'.format(code, message)
    aggregator.assert_service_check('aws_pricing.status', AwsPricingCheck.CRITICAL, message=message)
    assert len(aggregator.service_checks('aws_pricing.status')) == 1, 'Too many service checks were emitted'
