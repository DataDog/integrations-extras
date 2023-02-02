import pytest
from mock import MagicMock

from datadog_checks.base import ConfigurationError
from datadog_checks.cloudsmith import CloudsmithCheck
from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.unit
def test_empty_instance(aggregator, instance_empty):
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [instance_empty])


@pytest.mark.unit
def test_api_key_none(aggregator, instance_api_key_none):
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [instance_api_key_none])


@pytest.mark.unit
def test_org_none(aggregator, instance_org_none):
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [instance_org_none])


@pytest.mark.unit
def test_uri_none(aggregator, instance_url_none):
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [instance_url_none])


def test_check(
    aggregator,
    instance_good,
    usage_resp_good,
    entitlements_test_json,
    audit_log_resp_good,
):

    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_usage_info = MagicMock(return_value=usage_resp_good)
    check.get_entitlement_info = MagicMock(return_value=entitlements_test_json)
    check.get_audit_log_info = MagicMock(return_value=audit_log_resp_good)

    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.OK)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.OK)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 0.0, count=1)
    aggregator.assert_metric("cloudsmith.storage_used", 0.914, count=1)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", 37802418, count=1)
    aggregator.assert_metric("cloudsmith.token_count", 119, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", 240, count=1)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_check_bad_json(aggregator, instance_good, not_found_json):

    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_api_json = MagicMock(return_value=not_found_json)
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.UNKNOWN)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.UNKNOWN)
    aggregator.assert_metric("cloudsmith.bandwidth_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_count", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", -1, count=1)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_check_bad_usage(aggregator, instance_good, usage_resp_warning, usage_resp_critical, entitlements_test_json):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    # Check for usage warning
    check.get_usage_info = MagicMock(return_value=usage_resp_warning)
    check.get_entitlement_info = MagicMock(return_value=entitlements_test_json)
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.WARNING)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.WARNING)
    aggregator.assert_metric("cloudsmith.storage_used", 80.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 80.0, count=1)

    # Check for usage critical
    check.get_usage_info = MagicMock(return_value=usage_resp_critical)
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.CRITICAL)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.CRITICAL)
    aggregator.assert_metric("cloudsmith.storage_used", 100.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 100.0, count=1)


def test_check_badly_formatted_json(aggregator, instance_good, entitlements_test_bad_json, usage_resp_bad_json):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    # Check for results if json usage doesn't have the expected keys
    check.get_usage_info = MagicMock(return_value=usage_resp_bad_json)
    check.get_entitlement_info = MagicMock(return_value=entitlements_test_bad_json)
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.UNKNOWN)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.UNKNOWN)
    aggregator.assert_metric("cloudsmith.storage_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_count", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", -1, count=1)
