import json
import time
from urllib.error import HTTPError

import pytest
from mock import MagicMock
from requests.exceptions import InvalidURL, Timeout

from datadog_checks.base import ConfigurationError
from datadog_checks.cloudsmith import CloudsmithCheck
from datadog_checks.dev.utils import get_metadata_metrics


def _mock_non_analytics(check):
    """Stub out all non-analytics collection methods so bandwidth tests run in isolation."""
    check.get_parsed_usage_info = MagicMock(
        return_value={
            "storage_mark": CloudsmithCheck.OK,
            "storage_used": 1.0,
            "bandwidth_mark": CloudsmithCheck.OK,
            "bandwidth_used": 1.0,
            "storage_used_bytes": 1,
            "storage_plan_limit_bytes": 2,
            "bandwidth_used_bytes": 1,
            "bandwidth_plan_limit_bytes": 2,
            "storage_used_gb": 1.0,
            "storage_plan_limit_gb": 2.0,
            "bandwidth_used_gb": 1.0,
            "bandwidth_plan_limit_gb": 2.0,
            "storage_configured_bytes": 2,
            "bandwidth_configured_bytes": 2,
            "storage_configured_gb": 2.0,
            "bandwidth_configured_gb": 2.0,
        }
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 1, "token_bandwidth_total": 2, "token_download_total": 3}
    )
    check.get_parsed_audit_log_info = MagicMock(
        return_value=[
            {
                "actor": "a",
                "actor_kind": "user",
                "city": "x",
                "event": "login",
                "event_at": int(time.time()),
                "object": "o",
                "object_slug_perm": "s",
            }
        ]
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_license_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_members_info = MagicMock(return_value=[])
    check.get_parsed_repositories_info = MagicMock(return_value=[])


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
    check.get_parsed_repositories_info = MagicMock(
        return_value=[
            {
                "repository": "prod",
                "repository_type": "private",
                "storage_region": "default",
                "visibility": "private",
                "storage_bytes": 226620351,
                "package_count": 42,
                "download_count": 7,
            }
        ]
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 119, "token_bandwidth_total": 37802418, "token_download_total": 240}
    )
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})

    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.OK)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.OK)
    aggregator.assert_metric("cloudsmith.bandwidth_used", 0.0, count=1)
    aggregator.assert_metric("cloudsmith.storage_used", 0.914, count=1)
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
    aggregator.assert_metric("cloudsmith.repository.storage_bytes", 226620351, count=1)
    aggregator.assert_metric("cloudsmith.repository.package_count", 42, count=1)
    aggregator.assert_metric("cloudsmith.repository.download_count", 7, count=1)
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
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", 37802418, count=1)
    aggregator.assert_metric("cloudsmith.token_count", 119, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", 240, count=1)
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


def test_check_bad_usage(aggregator, instance_good, usage_resp_warning, usage_resp_critical):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 119, "token_bandwidth_total": 37802418, "token_download_total": 240}
    )
    check.get_parsed_members_info = MagicMock(return_value=[])
    check.get_parsed_repositories_info = MagicMock(return_value=[])

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


def test_check_badly_formatted_json(aggregator, instance_good, usage_resp_bad_json):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": -1, "token_bandwidth_total": -1, "token_download_total": -1}
    )
    check.get_parsed_members_info = MagicMock(return_value=[])
    check.get_parsed_repositories_info = MagicMock(return_value=[])

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
    check.get_license_policy_violation_info = MagicMock(return_value={"results": []})
    check.get_vuln_policy_violation_info = MagicMock(return_value={"results": []})
    check.check(None)

    aggregator.assert_service_check('cloudsmith.storage', CloudsmithCheck.UNKNOWN)
    aggregator.assert_service_check('cloudsmith.bandwidth', CloudsmithCheck.UNKNOWN)
    aggregator.assert_metric("cloudsmith.storage_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_used_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_used_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_used_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.storage_plan_limit_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_bytes", -1, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth_plan_limit_gb", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_count", -1, count=1)
    aggregator.assert_metric("cloudsmith.token_download_total", -1, count=1)


def test_vulnerability_and_license_violations(
    aggregator,
    instance_good,
    usage_resp_good,
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
    check.get_parsed_repositories_info = MagicMock(return_value=[])
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
    check.get_parsed_repositories_info = MagicMock(return_value=[])
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
    aggregator.assert_metric("cloudsmith.token_bandwidth_total", 37802418)
    aggregator.assert_metric("cloudsmith.token_count", 119)
    aggregator.assert_metric("cloudsmith.token_download_total", 240)
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
        headers = {}

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


def test_get_repositories_info_pagination(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    def _mock_page(url):
        if "page=1" in url:
            check._pagination_page = 1
            check._pagination_page_total = 2
            return [
                {"slug": "repo-a", "size": 10},
                {"slug": "repo-b", "size": 20},
            ]
        check._pagination_page = 2
        check._pagination_page_total = 2
        return [{"slug": "repo-c", "size": 30}]

    check.get_api_json = MagicMock(side_effect=_mock_page)

    parsed = check.get_repositories_info()

    assert len(parsed["results"]) == 3
    assert [repo["slug"] for repo in parsed["results"]] == ["repo-a", "repo-b", "repo-c"]


def test_get_parsed_repositories_info(instance_good):
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])
    check.get_repositories_info = MagicMock(
        return_value={
            "results": [
                {
                    "slug": "python",
                    "repository_type_str": "Private",
                    "storage_region": "default",
                    "is_private": True,
                    "size": 226620351,
                    "package_count": 8,
                    "num_downloads": 5,
                }
            ]
        }
    )

    parsed = check.get_parsed_repositories_info()

    assert parsed[0]["repository"] == "python"
    assert parsed[0]["repository_type"] == "private"
    assert parsed[0]["visibility"] == "private"
    assert parsed[0]["storage_bytes"] == 226620351
    assert parsed[0]["package_count"] == 8


# --- Rate-limit (429) and resilience tests ---


def test_get_api_json_429_retry_success(instance_good, mocker, aggregator):
    """A 429 followed by a 200 should succeed after a short retry."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    class Mock429Response:
        status_code = 429
        headers = {
            "x-ratelimit-reset": str(time.time() + 2),
            "x-ratelimit-remaining": "0",
            "x-ratelimit-limit": "10800",
        }

    class Mock200Response:
        status_code = 200
        headers = {}

        def json(self):
            return {"ok": True}

    mocker.patch(
        "datadog_checks.base.utils.http.requests.Session.get",
        side_effect=[Mock429Response(), Mock200Response()],
    )
    mocker.patch("time.sleep")  # Don't actually sleep in tests

    result = check.get_api_json("https://api.cloudsmith.io/v1/test")
    assert result == {"ok": True}
    # Verify we slept once (for the retry)
    time.sleep.assert_called_once()


def test_get_api_json_429_exhausted_retries(instance_good, mocker, aggregator):
    """All retries exhausted on 429 should return None and set WARNING service check."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    class Mock429Response:
        status_code = 429
        headers = {"Retry-After": "1"}

    mocker.patch(
        "datadog_checks.base.utils.http.requests.Session.get",
        return_value=Mock429Response(),
    )
    mocker.patch("time.sleep")

    result = check.get_api_json("https://api.cloudsmith.io/v1/test")
    assert result is None
    aggregator.assert_service_check("cloudsmith.can_connect", CloudsmithCheck.WARNING)


def test_get_api_json_429_no_headers_uses_default_wait(instance_good, mocker, aggregator):
    """When 429 has no rate-limit headers, use a sensible default wait."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    class Mock429NoHeaders:
        status_code = 429
        headers = {}

    class Mock200Response:
        status_code = 200
        headers = {}

        def json(self):
            return {"ok": True}

    mocker.patch(
        "datadog_checks.base.utils.http.requests.Session.get",
        side_effect=[Mock429NoHeaders(), Mock200Response()],
    )
    mocker.patch("time.sleep")

    result = check.get_api_json("https://api.cloudsmith.io/v1/test")
    assert result == {"ok": True}
    # Default wait is 5 seconds when no headers present
    time.sleep.assert_called_once_with(5)


def test_get_api_json_429_reset_too_far_skips_retries(instance_good, mocker, aggregator):
    """If x-ratelimit-reset is far in the future (> RATE_LIMIT_MAX_WAIT),
    skip retries immediately instead of wasting time sleeping."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    class Mock429FarReset:
        status_code = 429
        headers = {
            # Reset 120s in the future — way beyond the 10s cap
            "x-ratelimit-reset": str(time.time() + 120),
            "x-ratelimit-remaining": "0",
            "x-ratelimit-limit": "10800",
        }

    mocker.patch(
        "datadog_checks.base.utils.http.requests.Session.get",
        return_value=Mock429FarReset(),
    )
    mocker.patch("time.sleep")

    result = check.get_api_json("https://api.cloudsmith.io/v1/test")
    assert result is None
    # Should NOT have slept at all — bail out immediately
    time.sleep.assert_not_called()
    aggregator.assert_service_check("cloudsmith.can_connect", CloudsmithCheck.WARNING)


def test_check_continues_on_usage_api_failure(aggregator, instance_good, mocker):
    """If get_parsed_usage_info raises, the rest of the check still runs."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

    check.get_parsed_usage_info = MagicMock(side_effect=Exception("usage API down"))
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 5, "token_bandwidth_total": 100, "token_download_total": 10}
    )
    check.get_parsed_audit_log_info = MagicMock(
        return_value=[
            {
                "actor": "a",
                "actor_kind": "user",
                "city": "x",
                "event": "login",
                "event_at": int(time.time()),
                "object": "obj",
                "object_slug_perm": "slug",
            }
        ]
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_license_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_members_info = MagicMock(return_value=[])
    check.get_parsed_repositories_info = MagicMock(return_value=[])

    # Should not raise
    check.check(None)

    # Usage defaults should be used (-1), but entitlement metrics should still be submitted
    aggregator.assert_metric("cloudsmith.storage_used", -1)
    aggregator.assert_metric("cloudsmith.token_count", 5)


def test_check_continues_on_members_api_failure(aggregator, instance_good, mocker):
    """If get_parsed_members_info raises, the check still submits other metrics."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_good])

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
    check.get_parsed_audit_log_info = MagicMock(
        return_value=[
            {
                "actor": "a",
                "actor_kind": "user",
                "city": "x",
                "event": "login",
                "event_at": int(time.time()),
                "object": "obj",
                "object_slug_perm": "slug",
            }
        ]
    )
    check.get_parsed_entitlement_info = MagicMock(
        return_value={"token_count": 5, "token_bandwidth_total": 100, "token_download_total": 10}
    )
    check.get_parsed_vulnerabilities_info = MagicMock(return_value=[])
    check.get_parsed_vuln_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_license_policy_violation_info = MagicMock(return_value=[])
    check.get_parsed_members_info = MagicMock(side_effect=Exception("members API down"))
    check.get_parsed_repositories_info = MagicMock(return_value=[])

    # Should not raise
    check.check(None)

    # Other metrics should still be submitted
    aggregator.assert_metric("cloudsmith.storage_used", 10.0)
    aggregator.assert_metric("cloudsmith.token_count", 5)
    aggregator.assert_service_check("cloudsmith.storage", CloudsmithCheck.OK)


# --- Bandwidth profile tests ---


def test_bandwidth_profile_submits_latest_data_point(aggregator, instance_with_profiles, analytics_response_bytes):
    """A profile with data should submit the latest data point as a gauge."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_bytes)

    check.check(None)

    # Should submit the LATEST data point (67890)
    aggregator.assert_metric(
        "cloudsmith.analytics.bytes_downloaded_sum",
        67890.0,
        tags=[
            "base_url:https://api.cloudsmith.io/v1",
            "cloudsmith_org:cloudsmith",
            "profile:prod-python",
            "repository:production",
            "package_format:python",
        ],
        count=1,
    )


def test_bandwidth_profile_empty_data_no_metric(aggregator, instance_with_profiles, analytics_response_empty):
    """When the API returns empty data, no metric should be submitted."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_empty)

    check.check(None)

    assert "cloudsmith.analytics.bytes_downloaded_sum" not in aggregator._metrics


def test_bandwidth_profile_dedup_skips_stale_data(aggregator, instance_with_profiles, analytics_response_bytes):
    """On second check with the same data, no metric should be re-submitted."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_bytes)

    # First check should submit
    check.check(None)
    aggregator.assert_metric("cloudsmith.analytics.bytes_downloaded_sum", 67890.0, count=1)

    # Reset aggregator and check again — same data, should not submit another point
    aggregator.reset()
    check.check(None)
    assert "cloudsmith.analytics.bytes_downloaded_sum" not in aggregator._metrics


def test_bandwidth_profile_drops_incomplete_bucket(aggregator, instance_with_profiles):
    """The last bucket whose interval window hasn't closed yet should be dropped,
    and the second-to-last (completed) bucket should be submitted instead."""
    from datetime import datetime, timedelta, timezone

    # Build timestamps where the LAST one is still within its 5-min interval
    now = datetime.now(timezone.utc)
    # Completed bucket: started 10 minutes ago (well past its 5-min window)
    completed_ts = (now - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Incomplete bucket: started 2 minutes ago (5-min window NOT yet closed)
    incomplete_ts = (now - timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")

    response_with_incomplete = {
        "results": [
            {
                "dimensions": {"aggregate": "BYTES_DOWNLOADED_SUM", "unit": "bytes"},
                "timestamps": [completed_ts, incomplete_ts],
                "values": [42000, 5],
            }
        ],
    }

    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=response_with_incomplete)

    check.check(None)

    # Should submit the completed bucket value (42000), NOT the incomplete one (5)
    aggregator.assert_metric("cloudsmith.analytics.bytes_downloaded_sum", 42000.0, count=1)


def test_bandwidth_profile_all_buckets_incomplete(aggregator, instance_with_profiles):
    """When all buckets are incomplete (only one bucket, still accumulating),
    no metric should be submitted."""
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)
    incomplete_ts = (now - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    response_only_incomplete = {
        "results": [
            {
                "dimensions": {"aggregate": "BYTES_DOWNLOADED_SUM", "unit": "bytes"},
                "timestamps": [incomplete_ts],
                "values": [3],
            }
        ],
    }

    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=response_only_incomplete)

    check.check(None)

    # Only bucket was incomplete — nothing settled yet, so nothing should be submitted.
    assert "cloudsmith.analytics.bytes_downloaded_sum" not in aggregator._metrics


def test_bandwidth_profile_api_returns_none(aggregator, instance_with_profiles):
    """When the API returns None (e.g., network error), no metric should be submitted."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=None)

    check.check(None)

    assert "cloudsmith.analytics.bytes_downloaded_sum" not in aggregator._metrics


def test_bandwidth_profile_request_count(aggregator, instance_multi_profiles, analytics_response_requests):
    """A request_count profile should submit the correct metric name."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_multi_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_requests)

    check.check(None)

    aggregator.assert_metric("cloudsmith.analytics.request_count", 99.0, count=1)


def test_bandwidth_profile_invalid_config_raises(instance_good):
    """Invalid profile config should raise ConfigurationError at init."""
    bad_instance = dict(
        instance_good,
        bandwidth_profiles=[
            {"name": "bad", "interval": "five_minutes", "aggregate": "bytes_downloaded_sum"},
        ],
    )
    with pytest.raises(ConfigurationError, match="per-profile 'interval' is no longer supported"):
        CloudsmithCheck('cloudsmith', {}, [bad_instance])


def test_bandwidth_profile_missing_name_raises(instance_good):
    """Profile missing required 'name' should raise ConfigurationError."""
    bad_instance = dict(
        instance_good,
        bandwidth_profiles=[
            {"interval": "five_minutes", "aggregate": "bytes_downloaded_sum"},
        ],
    )
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [bad_instance])


def test_bandwidth_profile_invalid_aggregate_raises(instance_good):
    """Profile with invalid aggregate should raise ConfigurationError."""
    bad_instance = dict(
        instance_good,
        bandwidth_profiles=[
            {"name": "bad", "aggregate": "invalid_agg"},
        ],
    )
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [bad_instance])


def test_bandwidth_profile_duplicate_name_raises(instance_good):
    """Two profiles with the same name should raise ConfigurationError."""
    bad_instance = dict(
        instance_good,
        bandwidth_profiles=[
            {"name": "dupe", "aggregate": "bytes_downloaded_sum"},
            {"name": "dupe", "aggregate": "request_count"},
        ],
    )
    with pytest.raises(ConfigurationError):
        CloudsmithCheck('cloudsmith', {}, [bad_instance])


def test_no_profiles_configured_no_analytics_metrics(aggregator, instance_good):
    """Without bandwidth_profiles and with realtime disabled, no analytics metrics should be submitted."""
    inst = dict(instance_good, enable_realtime_bandwidth=False)
    check = CloudsmithCheck('cloudsmith', {}, [inst])
    _mock_non_analytics(check)

    check.check(None)

    assert "cloudsmith.analytics.bytes_downloaded_sum" not in aggregator._metrics
    assert "cloudsmith.analytics.request_count" not in aggregator._metrics
    assert "cloudsmith.bandwidth.bytes_downloaded" not in aggregator._metrics
    assert "cloudsmith.bandwidth.request_count" not in aggregator._metrics


# --- Org-wide bandwidth tests ---


def test_org_bandwidth_submits_both_metrics(
    aggregator, instance_with_realtime, analytics_response_bytes, analytics_response_requests
):
    """With enable_realtime_bandwidth=True, both org-wide metrics should be submitted."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_realtime])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(side_effect=[analytics_response_bytes, analytics_response_requests])

    check.check(None)

    aggregator.assert_metric(
        "cloudsmith.bandwidth.bytes_downloaded",
        67890.0,
        tags=[
            "base_url:https://api.cloudsmith.io/v1",
            "cloudsmith_org:cloudsmith",
        ],
        count=1,
    )
    aggregator.assert_metric(
        "cloudsmith.bandwidth.request_count",
        99.0,
        tags=[
            "base_url:https://api.cloudsmith.io/v1",
            "cloudsmith_org:cloudsmith",
        ],
        count=1,
    )


def test_org_bandwidth_disabled(aggregator, instance_good):
    """With enable_realtime_bandwidth=False (or unset with profiles), no org bandwidth metrics."""
    inst = dict(instance_good, enable_realtime_bandwidth=False)
    check = CloudsmithCheck('cloudsmith', {}, [inst])
    _mock_non_analytics(check)

    check.check(None)

    assert "cloudsmith.bandwidth.bytes_downloaded" not in aggregator._metrics
    assert "cloudsmith.bandwidth.request_count" not in aggregator._metrics


def test_org_bandwidth_dedup(aggregator, instance_with_realtime, analytics_response_bytes, analytics_response_requests):
    """On second run with same data, org bandwidth should not re-submit stale points."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_realtime])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(side_effect=[analytics_response_bytes, analytics_response_requests])

    # First check submits real values
    check.check(None)
    aggregator.assert_metric("cloudsmith.bandwidth.bytes_downloaded", 67890.0, count=1)
    aggregator.assert_metric("cloudsmith.bandwidth.request_count", 99.0, count=1)

    # Second check with same data — should not submit stale points again
    aggregator.reset()
    check.get_api_json = MagicMock(side_effect=[analytics_response_bytes, analytics_response_requests])
    check.check(None)
    assert "cloudsmith.bandwidth.bytes_downloaded" not in aggregator._metrics
    assert "cloudsmith.bandwidth.request_count" not in aggregator._metrics


def test_org_bandwidth_invalid_interval_raises(instance_good):
    """An invalid bandwidth_interval should raise ConfigurationError."""
    bad_instance = dict(instance_good, bandwidth_interval="invalid_interval")
    with pytest.raises(ConfigurationError, match="bandwidth_interval must be one of"):
        CloudsmithCheck('cloudsmith', {}, [bad_instance])


def test_bandwidth_profile_filter_tags(aggregator, analytics_response_bytes):
    """Profile filter keys should be emitted as tags."""
    instance = {
        'url': 'https://api.cloudsmith.io/v1',
        'cloudsmith_api_key': 'aaa',
        'organization': 'cloudsmith',
        'enable_realtime_bandwidth': False,
        'bandwidth_interval': 'five_minutes',
        'bandwidth_profiles': [
            {
                'name': 'by-country',
                'aggregate': 'bytes_downloaded_sum',
                'country': ['US', 'GB'],
                'entitlement_token': ['tok-123'],
            },
        ],
    }
    check = CloudsmithCheck('cloudsmith', {}, [instance])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_bytes)

    check.check(None)

    aggregator.assert_metric(
        "cloudsmith.analytics.bytes_downloaded_sum",
        67890.0,
        tags=[
            "base_url:https://api.cloudsmith.io/v1",
            "cloudsmith_org:cloudsmith",
            "profile:by-country",
            "entitlement_token:tok-123",
            "country:US",
            "country:GB",
        ],
        count=1,
    )


def test_bandwidth_profile_poll_throttled_by_interval(aggregator, instance_with_profiles, analytics_response_bytes):
    """Second check run within the same interval should not call analytics API again."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_bytes)

    check.check(None)
    assert check.get_api_json.call_count == 1

    aggregator.reset()
    check.get_api_json = MagicMock(side_effect=AssertionError("API should not be called within throttle window"))
    check.check(None)
    assert "cloudsmith.analytics.bytes_downloaded_sum" not in aggregator._metrics


def test_bandwidth_profile_poll_resumes_after_interval(aggregator, instance_with_profiles, analytics_response_bytes):
    """Analytics polling should resume once the configured interval has elapsed."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_profiles])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(return_value=analytics_response_bytes)

    check.check(None)
    # Simulate interval passing without waiting in real time.
    check._analytics_last_poll["prod-python"] -= 300

    aggregator.reset()
    check.get_api_json = MagicMock(return_value=analytics_response_bytes)
    check.check(None)
    assert check.get_api_json.call_count == 1


def test_org_bandwidth_poll_throttled_by_interval(
    aggregator, instance_with_realtime, analytics_response_bytes, analytics_response_requests
):
    """Org-wide analytics should not be called again until the interval window elapses."""
    check = CloudsmithCheck('cloudsmith', {}, [instance_with_realtime])
    _mock_non_analytics(check)
    check.get_api_json = MagicMock(side_effect=[analytics_response_bytes, analytics_response_requests])

    check.check(None)
    assert check.get_api_json.call_count == 2

    aggregator.reset()
    check.get_api_json = MagicMock(side_effect=AssertionError("Org analytics API should be throttled"))
    check.check(None)
    assert "cloudsmith.bandwidth.bytes_downloaded" not in aggregator._metrics
    assert "cloudsmith.bandwidth.request_count" not in aggregator._metrics
