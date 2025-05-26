import json
import time
from urllib.error import HTTPError

import pytest
from mock import MagicMock
from requests.exceptions import InvalidURL, Timeout

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
        "cloudsmith.member.active",
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
    # Assert new metrics added for members and policy violations
    for metric in [
        "cloudsmith.license_policy_violation.count",
        "cloudsmith.vulnerability_policy_violation.count",
        "cloudsmith.member.has_2fa.count",
        "cloudsmith.member.saml.count",
        "cloudsmith.member.password.count",
        "cloudsmith.member.owner.count",
        "cloudsmith.member.manager.count",
        "cloudsmith.member.admin.count",
        "cloudsmith.member.readonly.count",
    ]:
        aggregator.assert_metric(metric)
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
    # Assert new metrics added for members and policy violations
    for metric in [
        "cloudsmith.license_policy_violation.count",
        "cloudsmith.vulnerability_policy_violation.count",
        "cloudsmith.member.has_2fa.count",
        "cloudsmith.member.saml.count",
        "cloudsmith.member.password.count",
        "cloudsmith.member.owner.count",
        "cloudsmith.member.manager.count",
        "cloudsmith.member.admin.count",
        "cloudsmith.member.readonly.count",
    ]:
        aggregator.assert_metric(metric)
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
            "cloudsmith.member.active",
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

    # Assert new metrics added for members and policy violations
    for metric in [
        "cloudsmith.license_policy_violation.count",
        "cloudsmith.vulnerability_policy_violation.count",
        "cloudsmith.member.has_2fa.count",
        "cloudsmith.member.saml.count",
        "cloudsmith.member.password.count",
        "cloudsmith.member.owner.count",
        "cloudsmith.member.manager.count",
        "cloudsmith.member.admin.count",
        "cloudsmith.member.readonly.count",
    ]:
        aggregator.assert_metric(metric)
    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_get_parsed_usage_info_missing_keys(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_usage_info = MagicMock(return_value={})  # Simulate missing 'usage' key
    result = check.get_parsed_usage_info()
    assert result["storage_used"] == -1
    assert result["bandwidth_used"] == -1
    assert result["storage_used_bytes"] == -1
    assert result["bandwidth_used_bytes"] == -1


def test_get_parsed_license_policy_violation_info_structure(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_license_policy_violation_info = MagicMock(
        return_value={
            "results": [
                {
                    "package": {"name": "pkg"},
                    "policy": {"name": "GPL"},
                    "reasons": ["GPL-2.0", "GPL-3.0"],
                    "event_at": "2023-01-01T00:00:00.000000Z",
                }
            ]
        }
    )
    parsed = check.get_parsed_license_policy_violation_info()
    assert parsed[0]["policy"] == "GPL"
    assert "GPL-2.0" in parsed[0]["reason"]


def test_filter_vulnerabilities_multiple_severities(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    data = [
        {"max_severity": "Critical"},
        {"max_severity": "Medium"},
        {"max_severity": "Low"},
    ]
    result = check.filter_vulnerabilities(data, ["Critical", "Medium"])
    assert len(result) == 2
    assert result[0]["max_severity"] == "Critical"
    assert result[1]["max_severity"] == "Medium"


def test_get_api_json_exceptions(instance_good, mocker):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    # Timeout
    mocker.patch("datadog_checks.base.utils.http.requests.get", side_effect=Timeout("timeout"))
    with pytest.raises(Timeout):
        check.get_api_json("https://api.cloudsmith.io/v1/timeout")

    # HTTPError
    mocker.patch(
        "datadog_checks.base.utils.http.requests.get", side_effect=HTTPError("url", 500, "Internal Error", {}, None)
    )
    with pytest.raises(HTTPError):
        check.get_api_json("https://api.cloudsmith.io/v1/http-error")

    # InvalidURL
    mocker.patch("datadog_checks.base.utils.http.requests.get", side_effect=InvalidURL("bad url"))
    with pytest.raises(InvalidURL):
        check.get_api_json("https://api.cloudsmith.io/v1/invalid")

    # JSONDecodeError
    class MockBadResponse:
        status_code = 200

        def json(self):
            raise json.JSONDecodeError("Expecting value", "doc", 0)

    mocker.patch("datadog_checks.base.utils.http.requests.get", return_value=MockBadResponse())
    with pytest.raises(json.JSONDecodeError):
        check.get_api_json("https://api.cloudsmith.io/v1/bad-json")
