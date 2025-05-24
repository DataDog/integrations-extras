import time

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
    members_resp,
    mocker,
):

    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.OK,
            "storage_used": 0.914,
            "storage_used_bytes": 914000000,
            "storage_used_gb": 0.914,
            "storage_plan_limit_gb": 100.0,
            "bandwidth_mark": CloudsmithCheck.OK,
            "bandwidth_used": 0.0,
            "bandwidth_used_bytes": 0,
            "bandwidth_used_gb": 0.0,
            "storage_plan_limit_bytes": 100000000000,
            "bandwidth_plan_limit_bytes": 100000000000,
            "bandwidth_plan_limit_gb": 100.0,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 119, "token_bandwidth_total": 37802418, "token_download_total": 240}
    )
    check.get_parsed_audit_log_info = MagicMock(
        return_value=[
            {
                "event_at": int(time.time()),
                "event": "test_event",
                "object": "test_object",
                "object_slug_perm": "slug_perm",
                "actor": "test_actor",
                "actor_kind": "user",
                "city": "test_city",
            }
        ]
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_license_policy_violation_info = MagicMock(return_value={"results": []})
    check.get_parsed_members_info = MagicMock(
        return_value=[
            {
                "is_active": True,
                "user": "testuser",
                "role": "admin",
                "has_two_factor": True,
                "last_login_at": int(time.time()),
            }
        ]
    )
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})

    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.OK)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.OK)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 0.0, count=1)
    aggregator.assert_metric("cloudsmith.storage_used", 0.914, count=1)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", 37802418, count=1)
    aggregator.assert_metric("cloudsmith.token_count", 119, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", 240, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_bytes", 100000000000, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_gb", 100.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_bytes", 0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_gb", 0.0, count=1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_bytes", 100000000000, count=1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_gb", 100.0, count=1)
    aggregator.assert_metric("cloudsmith.storage_used_bytes", 914000000, count=1)
    aggregator.assert_metric("cloudsmith.storage_used_gb", 0.914, count=1)
    aggregator.assert_metric(
        "cloudsmith.cloudsmith.member.active",
        1,
        tags=[
            "user:testuser",
            "role:admin",
            "2fa:True",
            "base_url:https://api.cloudsmith.io/v1",
            "cloudsmith_org:cloudsmith",
        ],
        count=1,
    )
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_check_bad_usage(aggregator, instance_good, usage_resp_warning, usage_resp_critical, entitlements_test_json):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_members_info = MagicMock(return_value=[])

    # Check for usage warning
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.WARNING,
            "storage_used": 80.0,
            "storage_used_bytes": 80000000000,
            "storage_used_gb": 80.0,
            "bandwidth_mark": CloudsmithCheck.WARNING,
            "bandwidth_used": 80.0,
            "bandwidth_used_bytes": 80000000000,
            "bandwidth_used_gb": 80.0,
            "storage_plan_limit_gb": 100.0,
            "storage_plan_limit_bytes": 100000000000,
            "bandwidth_plan_limit_bytes": 100000000000,
            "bandwidth_plan_limit_gb": 100.0,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 119, "token_bandwidth_total": 37802418, "token_download_total": 240}
    )
    check.get_license_policy_violation_info = MagicMock(return_value={"results": []})
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.WARNING)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.WARNING)
    aggregator.assert_metric("cloudsmith.storage_used", 80.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 80.0, count=1)

    # Check for usage critical
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.CRITICAL,
            "storage_used": 100.0,
            "storage_used_bytes": 100000000000,
            "storage_used_gb": 100.0,
            "bandwidth_mark": CloudsmithCheck.CRITICAL,
            "bandwidth_used": 100.0,
            "bandwidth_used_bytes": 100000000000,
            "bandwidth_used_gb": 100.0,
            "storage_plan_limit_gb": 100.0,
            "storage_plan_limit_bytes": 100000000000,
            "bandwidth_plan_limit_bytes": 100000000000,
            "bandwidth_plan_limit_gb": 100.0,
        }
    )
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.CRITICAL)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.CRITICAL)
    aggregator.assert_metric("cloudsmith.storage_used", 100.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 100.0, count=1)


def test_check_badly_formatted_json(aggregator, instance_good, entitlements_test_bad_json, usage_resp_bad_json):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_members_info = MagicMock(return_value=[])

    # Check for results if json usage doesn't have the expected keys
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.UNKNOWN,
            "storage_used": -1,
            "storage_used_bytes": -1,
            "storage_used_gb": -1,
            "bandwidth_mark": CloudsmithCheck.UNKNOWN,
            "bandwidth_used": -1,
            "bandwidth_used_bytes": -1,
            "bandwidth_used_gb": -1,
            "storage_plan_limit_gb": -1,
            "storage_plan_limit_bytes": -1,
            "bandwidth_plan_limit_bytes": -1,
            "bandwidth_plan_limit_gb": -1,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": -1, "token_bandwidth_total": -1, "token_download_total": -1}
    )
    check.get_license_policy_violation_info = MagicMock(return_value={"results": []})
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.UNKNOWN)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.UNKNOWN)
    aggregator.assert_metric("cloudsmith.storage_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_count", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_used_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_used_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_gb", -1, count=1)


def test_vulnerability_and_license_violations(
    aggregator,
    instance_good,
    usage_resp_good,
    entitlements_test_json,
    audit_log_resp_good,
    license_policy_violation_resp,
    license_policy_violation_resp_bad,
    mocker,
):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.UNKNOWN,
            "storage_used": 0.914,
            "storage_used_bytes": -1,
            "storage_used_gb": -1,
            "bandwidth_mark": CloudsmithCheck.UNKNOWN,
            "bandwidth_used": 0.0,
            "bandwidth_used_bytes": -1,
            "bandwidth_used_gb": -1,
            "storage_plan_limit_gb": -1,
            "storage_plan_limit_bytes": -1,
            "bandwidth_plan_limit_bytes": -1,
            "bandwidth_plan_limit_gb": -1,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 119, "token_bandwidth_total": 37802418, "token_download_total": 240}
    )
    check.get_parsed_audit_log_info = MagicMock(return_value=audit_log_resp_good)
    check.get_parsed_license_policy_violations_info = MagicMock(
        side_effect=[license_policy_violation_resp_bad, license_policy_violation_resp]
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_parsed_members_info = MagicMock(return_value=[])
    check.get_license_policy_violation_info = MagicMock(return_value={"results": []})
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})

    check.check(None)

    aggregator.assert_metric("cloudsmith.bandwidth_used", 0.0)
    aggregator.assert_metric("cloudsmith.storage_used", 0.914)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", 37802418)
    aggregator.assert_metric("cloudsmith.token_count", 119)
    aggregator.assert_metric("cloudsmith.token_download_total", 240)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_bytes", -1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_gb", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_bytes", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_gb", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_bytes", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_gb", -1)
    aggregator.assert_metric("cloudsmith.storage_used_bytes", -1)
    aggregator.assert_metric("cloudsmith.storage_used_gb", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_bytes", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_gb", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_gb", -1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_bytes", -1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_gb", -1)
    aggregator.assert_metric("cloudsmith.storage_used_gb", -1)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_member_metrics_and_events(
    aggregator,
    instance_good,
    usage_resp_good,
    entitlements_test_json,
    audit_log_resp_good,
    members_resp,
    mocker,
):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.UNKNOWN,
            "storage_used": -1,
            "storage_used_bytes": -1,
            "storage_used_gb": -1,
            "bandwidth_mark": CloudsmithCheck.UNKNOWN,
            "bandwidth_used": -1,
            "bandwidth_used_bytes": -1,
            "bandwidth_used_gb": -1,
            "storage_plan_limit_gb": -1,
            "storage_plan_limit_bytes": -1,
            "bandwidth_plan_limit_bytes": -1,
            "bandwidth_plan_limit_gb": -1,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 119, "token_bandwidth_total": 37802418, "token_download_total": 240}
    )
    check.get_parsed_audit_log_info = MagicMock(return_value=audit_log_resp_good)
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_license_policy_violation_info = MagicMock(return_value={"results": []})
    check.get_parsed_members_info = MagicMock(
        return_value=[{"is_active": True, "user": "testuser", "role": "admin", "has_two_factor": True}]
    )
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})

    check.check(None)

    for _member in members_resp["results"]:
        aggregator.assert_metric(
            "cloudsmith.cloudsmith.member.active",
            1,
            tags=[
                "user:testuser",
                "role:admin",
                "2fa:True",
                "base_url:https://api.cloudsmith.io/v1",
                "cloudsmith_org:cloudsmith",
            ],
        )
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", 37802418)
    aggregator.assert_metric("cloudsmith.token_count", 119)
    aggregator.assert_metric("cloudsmith.token_download_total", 240)

    # Additional metrics for member metrics test
    aggregator.assert_metric("cloudsmith.bandwidth_used", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_bytes", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_gb", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_bytes", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_gb", -1)
    aggregator.assert_metric("cloudsmith.storage_used", -1)
    aggregator.assert_metric("cloudsmith.storage_used_bytes", -1)
    aggregator.assert_metric("cloudsmith.storage_used_gb", -1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_bytes", -1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_gb", -1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
