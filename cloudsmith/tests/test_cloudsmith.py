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
            "storage_configured_bytes": 100000000000,
            "storage_configured_gb": 100.0,
            "bandwidth_configured_bytes": 100000000000,
            "bandwidth_configured_gb": 100.0,
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
    aggregator.assert_metric("cloudsmith.storage_configured_bytes", 100000000000, count=1)
    aggregator.assert_metric("cloudsmith.storage_configured_gb", 100.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_configured_bytes", 100000000000, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_configured_gb", 100.0, count=1)
    aggregator.assert_metric(
        "cloudsmith.member.active",
        1,
        tags=[
            "user:testuser",
            "role:admin",
            "2fa:True",
            "base_url:https://api.cloudsmith.io/v1",
            "cloudsmith_org:cloudsmith",
            "source:cloudsmith",
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
            "storage_configured_bytes": 100000000000,
            "storage_configured_gb": 100.0,
            "bandwidth_configured_bytes": 100000000000,
            "bandwidth_configured_gb": 100.0,
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
            "storage_configured_bytes": 100000000000,
            "storage_configured_gb": 100.0,
            "bandwidth_configured_bytes": 100000000000,
            "bandwidth_configured_gb": 100.0,
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
            "storage_configured_bytes": -1,
            "storage_configured_gb": -1,
            "bandwidth_configured_bytes": -1,
            "bandwidth_configured_gb": -1,
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
            "storage_configured_bytes": -1,
            "storage_configured_gb": -1,
            "bandwidth_configured_bytes": -1,
            "bandwidth_configured_gb": -1,
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
    aggregator.assert_metric("cloudsmith.storage_configured_bytes")
    aggregator.assert_metric("cloudsmith.storage_configured_gb")
    aggregator.assert_metric("cloudsmith.bandwidth_configured_bytes")
    aggregator.assert_metric("cloudsmith.bandwidth_configured_gb")
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
            "storage_configured_bytes": -1,
            "storage_configured_gb": -1,
            "bandwidth_configured_bytes": -1,
            "bandwidth_configured_gb": -1,
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
    # Assert the newly added metrics for configured storage and bandwidth
    aggregator.assert_metric("cloudsmith.storage_configured_bytes", -1)
    aggregator.assert_metric("cloudsmith.storage_configured_gb", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_configured_bytes", -1)
    aggregator.assert_metric("cloudsmith.bandwidth_configured_gb", -1)
    # Explicitly assert the four missing metrics to ensure coverage
    aggregator.assert_metric("cloudsmith.storage_configured_bytes")
    aggregator.assert_metric("cloudsmith.bandwidth_configured_bytes")
    aggregator.assert_metric("cloudsmith.storage_configured_gb")
    aggregator.assert_metric("cloudsmith.bandwidth_configured_gb")
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
    mocker.patch("datadog_checks.base.utils.http.requests.Session.get", side_effect=Timeout("timeout"))
    with pytest.raises(Timeout):
        check.get_api_json("https://api.cloudsmith.io/v1/timeout")

    # HTTPError
    mocker.patch(
        "datadog_checks.base.utils.http.requests.Session.get",
        side_effect=HTTPError("url", 500, "Internal Error", {}, None),
    )
    with pytest.raises(HTTPError):
        check.get_api_json("https://api.cloudsmith.io/v1/http-error")

    # InvalidURL
    mocker.patch("datadog_checks.base.utils.http.requests.Session.get", side_effect=InvalidURL("bad url"))
    with pytest.raises(InvalidURL):
        check.get_api_json("https://api.cloudsmith.io/v1/invalid")

    # JSONDecodeError
    class MockBadResponse:
        status_code = 200

        def json(self):
            raise json.JSONDecodeError("Expecting value", "doc", 0)

    mocker.patch("datadog_checks.base.utils.http.requests.Session.get", return_value=MockBadResponse())
    with pytest.raises(json.JSONDecodeError):
        check.get_api_json("https://api.cloudsmith.io/v1/bad-json")


# Additional test for 401 handling and fallback behavior in get_api_json()
def test_api_json_401_and_fallbacks(instance_good, mocker):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    class Mock401Response:
        def __init__(self):
            self.status_code = 401

        def json(self):
            return {}

    # Patch .http.get to return a mock 401 response for 'audit-log'
    mocker.patch("datadog_checks.base.utils.http.requests.Session.get", return_value=Mock401Response())

    # Should return None and trigger fallback
    audit_result = check.get_audit_log_info()
    assert isinstance(audit_result, list)
    assert audit_result[0]["event"] == "action.login"

    # Also test for 'vulnerabilities'
    result = check.get_vulnerabilities_info()
    assert isinstance(result, list)
    assert result[0]["package"]["name"] == "python"


# --- Additional direct unit tests for public methods ---


def test_get_full_path(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    path = check.get_full_path("/test/")
    assert path.replace("\\", "/").endswith("/test/cloudsmith")


def test_convert_time(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    ts = check.convert_time("2023-01-01T00:00:00.000000Z")
    assert isinstance(ts, int)
    assert ts > 0


def test_get_parsed_audit_log_info(instance_good, mocker):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    mocker.patch.object(
        check,
        'get_audit_log_info',
        return_value=[
            {
                "actor": "a",
                "actor_kind": "user",
                "actor_location": {"city": "x"},
                "event": "login",
                "event_at": "2023-01-01T00:00:00.000000Z",
                "object": "obj",
                "object_slug_perm": "slug",
            }
        ],
    )
    parsed = check.get_parsed_audit_log_info()
    assert isinstance(parsed, list)
    assert parsed[0]["actor"] == "a"
    assert parsed[0]["city"] == "x"
    assert isinstance(parsed[0]["event_at"], int)


def test_filter_vulnerabilities(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    results = [
        {"max_severity": "High"},
        {"max_severity": "Low"},
        {"max_severity": "Critical"},
    ]
    filtered = check.filter_vulnerabilities(results, ["Critical", "High"])
    assert len(filtered) == 2
    severities = {item["max_severity"] for item in filtered}
    assert "High" in severities
    assert "Critical" in severities


def test_realtime_bandwidth_metrics(aggregator, instance_good, usage_resp_good, entitlements_test_json):
    # Enable realtime bandwidth
    check = CloudsmithCheck('cloudsmith', {}, [dict(instance_good, enable_realtime_bandwidth=True)])

    # Mock parsed usage/entitlements (check() uses parsed versions)
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.OK,
            "storage_used": 10.0,
            "bandwidth_mark": CloudsmithCheck.OK,
            "bandwidth_used": 5.0,
            "storage_used_bytes": 1000,
            "storage_plan_limit_bytes": 2000,
            "bandwidth_used_bytes": 3000,
            "bandwidth_plan_limit_bytes": 4000,
            "storage_used_gb": 1.0,
            "storage_plan_limit_gb": 2.0,
            "bandwidth_used_gb": 3.0,
            "bandwidth_plan_limit_gb": 4.0,
            "storage_configured_bytes": 2000,
            "bandwidth_configured_bytes": 4000,
            "storage_configured_gb": 2.0,
            "bandwidth_configured_gb": 4.0,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 1, "token_bandwidth_total": 2, "token_download_total": 3}
    )
    # Provide required auxiliary method mocks to avoid network calls
    now_evt = int(time.time())
    check.get_parsed_audit_log_info = MagicMock(
        return_value=[
            {
                "actor": "a",
                "actor_kind": "user",
                "city": "x",
                "event": "login",
                "event_at": now_evt,
                "object": "obj",
                "object_slug_perm": "slug",
            }
        ]
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_license_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_members_info = MagicMock(
        return_value=[
            {
                "is_active": True,
                "user": "user1",
                "role": "admin",
                "has_two_factor": True,
                "last_login_method": "saml",
                "last_login_at": now_evt,
            }
        ]
    )

    realtime_resp = {
        "results": [
            {
                "dimensions": {"aggregate": "BYTES_DOWNLOADED_SUM", "unit": "bytes"},
                "timestamps": ["2025-10-29T18:34:00Z", "2025-10-29T18:35:00Z"],
                "values": [1000, 1600],
            }
        ]
    }
    check.get_realtime_bandwidth_info = MagicMock(return_value=realtime_resp)

    check.check(None)

    aggregator.assert_metric("cloudsmith.bandwidth_bytes_interval", 1600.0, count=1)


def test_realtime_bandwidth_metrics_insufficient_points(
    aggregator, instance_good, usage_resp_good, entitlements_test_json
):
    check = CloudsmithCheck('cloudsmith', {}, [dict(instance_good, enable_realtime_bandwidth=True)])
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.OK,
            "storage_used": 10.0,
            "bandwidth_mark": CloudsmithCheck.OK,
            "bandwidth_used": 5.0,
            "storage_used_bytes": 1000,
            "storage_plan_limit_bytes": 2000,
            "bandwidth_used_bytes": 3000,
            "bandwidth_plan_limit_bytes": 4000,
            "storage_used_gb": 1.0,
            "storage_plan_limit_gb": 2.0,
            "bandwidth_used_gb": 3.0,
            "bandwidth_plan_limit_gb": 4.0,
            "storage_configured_bytes": 2000,
            "bandwidth_configured_bytes": 4000,
            "storage_configured_gb": 2.0,
            "bandwidth_configured_gb": 4.0,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 1, "token_bandwidth_total": 2, "token_download_total": 3}
    )
    now_evt = int(time.time())
    check.get_parsed_audit_log_info = MagicMock(
        return_value=[
            {
                "actor": "a",
                "actor_kind": "user",
                "city": "x",
                "event": "login",
                "event_at": now_evt,
                "object": "obj",
                "object_slug_perm": "slug",
            }
        ]
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_license_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_members_info = MagicMock(
        return_value=[
            {
                "is_active": True,
                "user": "user1",
                "role": "admin",
                "has_two_factor": True,
                "last_login_method": "saml",
                "last_login_at": now_evt,
            }
        ]
    )
    realtime_resp = {
        "results": [
            {
                "dimensions": {"aggregate": "BYTES_DOWNLOADED_SUM", "unit": "bytes"},
                "timestamps": ["2025-10-29T18:34:00Z"],
                "values": [1000],
            }
        ]
    }
    check.get_realtime_bandwidth_info = MagicMock(return_value=realtime_resp)

    check.check(None)

    # Ensure realtime metric not emitted
    assert "cloudsmith.bandwidth_bytes_interval" not in aggregator._metrics
