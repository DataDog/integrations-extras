import pytest
from botocore.exceptions import ClientError

from datadog_checks.aws_pricing import AwsPricingCheck
from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.unit
def test_check_no_filters(aggregator, instance_good, mock_client):
    check = AwsPricingCheck("aws_pricing", {}, [instance_good])

    caller, _ = mock_client
    caller.assert_called_once_with("pricing", region_name="us-east-1")

    check.check(None)
    aggregator.assert_service_check("aws.pricing.status", AwsPricingCheck.OK)

    # Should send 2 metrics with no filters
    aggregator.assert_metric("aws.pricing.amazonec2", 5655.0, count=2)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_no_services_warning(aggregator, instance_no_services, mock_client):
    check = AwsPricingCheck("aws_pricing", {}, [instance_no_services])

    caller, _ = mock_client
    caller.assert_called_once_with("pricing", region_name="us-east-1")

    check.check(None)
    aggregator.assert_service_check("aws.pricing.status", AwsPricingCheck.WARNING)

    # Should send 0 metrics with no services
    aggregator.assert_metric("aws.pricing.amazonec2", count=0)


@pytest.mark.unit
def test_client_error(aggregator, instance_good, mock_client):
    check = AwsPricingCheck("aws_pricing", {}, [instance_good])

    caller, client = mock_client
    caller.assert_called_once_with("pricing", region_name="us-east-1")

    client.get_products.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}}, "get_products"
    )

    check.check(None)
    aggregator.assert_service_check("aws.pricing.status", AwsPricingCheck.CRITICAL)
