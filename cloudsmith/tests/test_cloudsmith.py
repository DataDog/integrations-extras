import pytest
from mock import MagicMock

from datadog_checks.base import ConfigurationError
from datadog_checks.cloudsmith import CloudsmithCheck
from datadog_checks.dev.utils import get_metadata_metrics

EXPECTED_VALUES = (("cloudsmith.vulnerability_count", 1),)


@pytest.mark.unit
def test_empty_instance(aggregator, instance_empty):
    check = CloudsmithCheck('cloudsmith', {}, [instance_empty])

    with pytest.raises(ConfigurationError):
        check.check(instance_empty)


@pytest.mark.unit
def test_api_key_none(aggregator, instance_api_key_none):
    check = CloudsmithCheck('cloudsmith', {}, [instance_api_key_none])

    with pytest.raises(ConfigurationError):
        check.check(instance_api_key_none)


@pytest.mark.unit
def test_org_none(aggregator, instance_org_none):
    check = CloudsmithCheck('cloudsmith', {}, [instance_org_none])

    with pytest.raises(ConfigurationError):
        check.check(instance_org_none)


@pytest.mark.unit
def test_uri_none(aggregator, instance_url_none):
    check = CloudsmithCheck('cloudsmith', {}, [instance_url_none])

    with pytest.raises(ConfigurationError):
        check.check(instance_url_none)


def test_check(aggregator, vulnerability_test_json, instance_good, usage_resp_good):

    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_vulnerability_info = MagicMock(return_value=vulnerability_test_json)
    check.get_usage_info = MagicMock(return_value=usage_resp_good)
    check.service_check = MagicMock()

    check.check(instance_good)
    check.service_check.assert_called_with(
        'cloudsmith.storage', CloudsmithCheck.OK, message="Percentage storaged used: 0.914%"
    )

    aggregator.assert_metric("cloudsmith.vulnerability_count", count=1)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_check_bad_usage(aggregator, vulnerability_test_json, instance_good, usage_resp_warning, usage_resp_critical):

    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_vulnerability_info = MagicMock(return_value=vulnerability_test_json)
    check.service_check = MagicMock()

    # Check for usage warning
    check.get_usage_info = MagicMock(return_value=usage_resp_warning)
    check.check(instance_good)
    check.service_check.assert_called_with(
        'cloudsmith.storage', CloudsmithCheck.WARNING, message="Percentage storaged used: 80%"
    )

    # Check for usage critical
    check.get_usage_info = MagicMock(return_value=usage_resp_critical)
    check.check(instance_good)
    check.service_check.assert_called_with(
        'cloudsmith.storage', CloudsmithCheck.CRITICAL, message="Percentage storaged used: 100%"
    )
