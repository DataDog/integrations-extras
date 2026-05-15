import base64
import json
import time
from unittest.mock import MagicMock, patch

import pytest
from datadog_checks.base import ConfigurationError
from datadog_checks.eden import EdenCheck


def _patch_http(check, mock_http):
    return patch.object(EdenCheck, "http", new=mock_http)


@pytest.mark.unit
def test_config_requires_url():
    check = EdenCheck("eden", {}, [{}])
    with pytest.raises(ConfigurationError):
        check.check({})


@pytest.mark.unit
def test_config_requires_robot_credentials():
    check = EdenCheck("eden", {}, [{}])
    with pytest.raises(ConfigurationError):
        check.check({"url": "https://api.eden.example.com"})
    with pytest.raises(ConfigurationError):
        check.check({"url": "https://api.eden.example.com", "org_id": "eden"})
    with pytest.raises(ConfigurationError):
        check.check(
            {
                "url": "https://api.eden.example.com",
                "org_id": "eden",
                "robot_username": "datadog-agent",
            }
        )


@pytest.mark.unit
def test_get_token_logs_in_with_robot_credentials(instance):
    check = EdenCheck("eden", {}, [instance])
    token = _jwt(exp=int(time.time()) + 900)
    response = MagicMock()
    response.json.return_value = {"token": token}
    response.raise_for_status.return_value = None
    http = MagicMock()
    http.post.return_value = response

    with _patch_http(check, http):
        result = check._get_token(
            {
                "url": "https://api.eden.example.com",
                "org_id": "eden",
                "robot_username": "datadog-agent",
                "robot_api_key": "secret",
            }
        )

    assert result == token
    args, kwargs = http.post.call_args
    assert args[0] == "https://api.eden.example.com/api/v1/auth/robots/login"
    assert kwargs["json"] == {"username": "datadog-agent", "api_key": "secret"}
    assert kwargs["extra_headers"]["X-Org-Id"] == "eden"


@pytest.mark.unit
def test_get_token_uses_org_uuid_when_provided(instance):
    check = EdenCheck("eden", {}, [instance])
    token = _jwt(exp=int(time.time()) + 900)
    response = MagicMock()
    response.json.return_value = {"token": token}
    response.raise_for_status.return_value = None
    http = MagicMock()
    http.post.return_value = response

    with _patch_http(check, http):
        check._get_token(
            {
                "url": "https://api.eden.example.com",
                "org_uuid": "org-uuid",
                "robot_username": "datadog-agent",
                "robot_api_key": "secret",
            }
        )

    args, kwargs = http.post.call_args
    assert args[0] == "https://api.eden.example.com/api/v1/auth/robots/login"
    assert kwargs["extra_headers"]["X-Org-Uuid"] == "org-uuid"
    assert "X-Org-Id" not in kwargs["extra_headers"]


@pytest.mark.unit
def test_get_token_reuses_cached_token(instance):
    check = EdenCheck("eden", {}, [instance])
    token = _jwt(exp=int(time.time()) + 900)
    http = MagicMock()
    login_instance = {
        "url": "https://api.eden.example.com",
        "org_id": "eden",
        "robot_username": "datadog-agent",
        "robot_api_key": "secret",
    }
    check._auth_cache[check._auth_cache_key(login_instance)] = {"token": token, "expires_at": int(time.time()) + 900}

    with _patch_http(check, http):
        assert check._get_token(login_instance) == token
    http.post.assert_not_called()


@pytest.mark.unit
def test_emit_rows_dispatches_by_metric_kind(aggregator, instance):
    check = EdenCheck("eden", {}, [instance])
    rows = [
        {
            "group": "proxy",
            "metric_name": "requests_total",
            "metric_kind": "sum",
            "value": 42,
            "service_name": "eden_service",
            "node_uuid": "node-1",
            "labels": {"endpoint_uuid": "endpoint-1"},
        },
        {
            "group": "proxy",
            "metric_name": "active_connections",
            "metric_kind": "gauge",
            "value": 7,
            "service_name": "eden_service",
            "node_uuid": "node-1",
            "labels": {},
        },
        {
            "group": "proxy",
            "metric_name": "request_duration_seconds",
            "metric_kind": "histogram",
            "count": 10,
            "sum": 1.5,
            "service_name": "eden_service",
            "node_uuid": "node-1",
            "labels": {},
        },
    ]

    check._emit_rows(rows, ["deployment:test"])

    aggregator.assert_metric(
        "eden.proxy.requests_total",
        value=42,
        tags=[
            "deployment:test",
            "eden_group:proxy",
            "eden_service:eden_service",
            "eden_node_uuid:node-1",
            "endpoint_uuid:endpoint-1",
        ],
    )
    aggregator.assert_metric("eden.proxy.active_connections", value=7)
    # No bucket data -> .count, .sum, .avg fallback
    aggregator.assert_metric("eden.proxy.request_duration_seconds.count", value=10)
    aggregator.assert_metric("eden.proxy.request_duration_seconds.sum", value=1.5)
    aggregator.assert_metric("eden.proxy.request_duration_seconds.avg", value=0.15)


@pytest.mark.unit
def test_emit_rows_submits_histogram_buckets_otel_shape(aggregator, instance):
    """Eden's fast-telemetry exporter ships N bounds and N+1 counts (with an overflow bucket)."""
    check = EdenCheck("eden", {}, [instance])
    check.submit_histogram_bucket = MagicMock()

    rows = [
        {
            "group": "proxy",
            "scope": "proxy",
            "metric_name": "proxy_request_duration_microseconds",
            "metric_kind": "histogram",
            "count": 7,
            "sum": 1234.0,
            "bucket_bounds": [10.0, 100.0, 1000.0],  # 3 bounds
            "bucket_counts": [3, 2, 1, 1],  # 4 counts (overflow at end)
            "labels": {},
        }
    ]
    check._emit_rows(rows, [])

    aggregator.assert_metric("eden.proxy.request_duration_microseconds.count", value=7)
    aggregator.assert_metric("eden.proxy.request_duration_microseconds.sum", value=1234.0)
    aggregator.assert_metric("eden.proxy.request_duration_microseconds.avg", count=0)

    calls = check.submit_histogram_bucket.call_args_list
    # 4 buckets, all non-zero
    assert len(calls) == 4
    assert [c.args[1] for c in calls] == [3, 2, 1, 1]
    assert [c.args[2] for c in calls] == [float("-inf"), 10.0, 100.0, 1000.0]
    assert [c.args[3] for c in calls] == [10.0, 100.0, 1000.0, float("inf")]


@pytest.mark.unit
def test_emit_rows_skips_zero_count_buckets(aggregator, instance):
    check = EdenCheck("eden", {}, [instance])
    check.submit_histogram_bucket = MagicMock()

    rows = [
        {
            "group": "proxy",
            "scope": "proxy",
            "metric_name": "proxy_request_duration_microseconds",
            "metric_kind": "histogram",
            "count": 1,
            "sum": 50.0,
            "bucket_bounds": [10.0, 100.0],
            "bucket_counts": [0, 1, 0],
            "labels": {},
        }
    ]
    check._emit_rows(rows, [])

    # Only the middle bucket has data; the empty ones should be skipped to keep cardinality down
    calls = check.submit_histogram_bucket.call_args_list
    assert len(calls) == 1
    assert calls[0].args[1] == 1
    assert calls[0].args[2] == 10.0
    assert calls[0].args[3] == 100.0


@pytest.mark.unit
def test_emit_rows_handles_exponential_histogram(aggregator, instance):
    """Eden's fast-telemetry exponential histograms ship empty bounds and rely on
    `scale` + `positive_offset` labels to derive bucket bounds."""
    check = EdenCheck("eden", {}, [instance])
    check.submit_histogram_bucket = MagicMock()

    rows = [
        {
            "group": "proxy",
            "scope": "proxy",
            "metric_name": "proxy_request_duration_microseconds",
            "metric_kind": "exponential_histogram",
            "count": 1023,
            "sum": 21896.0,
            "bucket_bounds": [],
            "bucket_counts": [17, 963, 21, 11, 9, 1, 1],
            # scale=0 -> base=2; offset=3 -> first bucket upper = 2^4 = 16
            "labels": {"scale": "0", "positive_offset": "3", "zero_count": "0"},
        }
    ]
    check._emit_rows(rows, [])

    aggregator.assert_metric("eden.proxy.request_duration_microseconds.count", value=1023)
    aggregator.assert_metric("eden.proxy.request_duration_microseconds.sum", value=21896.0)
    aggregator.assert_metric("eden.proxy.request_duration_microseconds.avg", count=0)

    calls = check.submit_histogram_bucket.call_args_list
    assert len(calls) == 7
    assert [c.args[1] for c in calls] == [17, 963, 21, 11, 9, 1, 1]
    assert [c.args[2] for c in calls] == [float("-inf"), 16.0, 32.0, 64.0, 128.0, 256.0, 512.0]
    assert [c.args[3] for c in calls] == [16.0, 32.0, 64.0, 128.0, 256.0, 512.0, 1024.0]


@pytest.mark.unit
def test_emit_rows_handles_equal_length_buckets(aggregator, instance):
    """Some exporters (and our older test fixtures) ship equal-length bound/count arrays."""
    check = EdenCheck("eden", {}, [instance])
    check.submit_histogram_bucket = MagicMock()

    rows = [
        {
            "group": "proxy",
            "scope": "proxy",
            "metric_name": "proxy_request_duration_microseconds",
            "metric_kind": "histogram",
            "count": 6,
            "sum": 1234.0,
            "bucket_bounds": [10.0, 100.0, 1000.0],
            "bucket_counts": [3, 2, 1],
            "labels": {},
        }
    ]
    check._emit_rows(rows, [])

    calls = check.submit_histogram_bucket.call_args_list
    assert [c.args[1] for c in calls] == [3, 2, 1]
    assert [c.args[2] for c in calls] == [float("-inf"), 10.0, 100.0]
    assert [c.args[3] for c in calls] == [10.0, 100.0, 1000.0]


@pytest.mark.unit
def test_emit_rows_preserves_qualified_metric_names(aggregator, instance):
    check = EdenCheck("eden", {}, [instance])

    check._emit_rows(
        [
            {
                "group": "proxy",
                "scope": "proxy",
                "metric_name": "proxy_lane_pool_waiters",
                "metric_kind": "sum",
                "value": 3,
                "labels": {},
            }
        ],
        [],
    )

    aggregator.assert_metric("eden.proxy.lane_pool_waiters", value=3)


@pytest.mark.unit
def test_metric_name_matches_dogstatsd(instance):
    check = EdenCheck("eden", {}, [instance])

    # Top-level groups: scope == group, metric_name = "<group>_<rest>" -> "<group>.<rest>"
    assert (
        check._metric_name({"group": "analytics", "scope": "analytics", "metric_name": "analytics_active_endpoints"})
        == "eden.analytics.active_endpoints"
    )
    assert (
        check._metric_name({"group": "eden", "scope": "eden", "metric_name": "eden_request_count"})
        == "eden.request_count"
    )
    assert (
        check._metric_name({"group": "proxy", "scope": "proxy", "metric_name": "proxy_lane_pool_waiters"})
        == "eden.proxy.lane_pool_waiters"
    )

    # Endpoint subgroup: scope == "eden.endpoint", metric_name = "eden.endpoint_<rest>" -> "eden.endpoint.<rest>"
    assert (
        check._metric_name(
            {"group": "endpoint", "scope": "eden.endpoint", "metric_name": "eden.endpoint_total_requests"}
        )
        == "eden.endpoint.total_requests"
    )
    assert (
        check._metric_name(
            {"group": "endpoint", "scope": "eden.endpoint", "metric_name": "eden.endpoint_active_requests"}
        )
        == "eden.endpoint.active_requests"
    )


@pytest.mark.unit
def test_check_emits_service_check_critical_on_http_error(aggregator, instance):
    check = EdenCheck("eden", {}, [instance])
    token = _jwt(exp=int(time.time()) + 900)
    check._auth_cache[check._auth_cache_key(instance)] = {"token": token, "expires_at": int(time.time()) + 900}
    http = MagicMock()
    http.get.side_effect = RuntimeError("boom")
    check._load_cursor = MagicMock(return_value=None)

    with _patch_http(check, http):
        check.check(instance)

    aggregator.assert_service_check("eden.api.can_connect", EdenCheck.CRITICAL)


@pytest.mark.unit
def test_check_polls_export_api_and_emits_ok(aggregator, instance):
    check = EdenCheck("eden", {}, [instance])
    token = _jwt(exp=int(time.time()) + 900)
    check._auth_cache[check._auth_cache_key(instance)] = {"token": token, "expires_at": int(time.time()) + 900}
    response = MagicMock()
    response.json.return_value = {
        "rows": [
            {
                "group": "proxy",
                "metric_name": "requests_total",
                "metric_kind": "sum",
                "value": 1,
                "labels": {},
            }
        ]
    }
    response.status_code = 200
    response.raise_for_status.return_value = None
    http = MagicMock()
    http.get.return_value = response
    check._load_cursor = MagicMock(return_value=None)
    check._save_cursor = MagicMock()

    with _patch_http(check, http):
        check.check(instance)

    aggregator.assert_service_check("eden.api.can_connect", EdenCheck.OK)
    args, kwargs = http.get.call_args
    assert args[0] == "https://api.eden.example.com/api/v1/analytics/telemetry"
    assert kwargs["params"]["signal"] == "metrics"
    assert kwargs["extra_headers"]["Authorization"] == f"Bearer {token}"


@pytest.mark.unit
def test_check_paginates_until_short_page(aggregator, instance):
    instance["metric_groups"] = ["proxy"]
    instance["limit"] = 2
    check = EdenCheck("eden", {}, [instance])

    full_page = MagicMock()
    full_page.status_code = 200
    full_page.raise_for_status.return_value = None
    full_page.json.return_value = {
        "rows": [
            {
                "group": "proxy",
                "scope": "proxy",
                "metric_name": "proxy_a",
                "metric_kind": "gauge",
                "value": 1,
                "labels": {},
            },
            {
                "group": "proxy",
                "scope": "proxy",
                "metric_name": "proxy_b",
                "metric_kind": "gauge",
                "value": 2,
                "labels": {},
            },
        ]
    }
    short_page = MagicMock()
    short_page.status_code = 200
    short_page.raise_for_status.return_value = None
    short_page.json.return_value = {
        "rows": [
            {
                "group": "proxy",
                "scope": "proxy",
                "metric_name": "proxy_c",
                "metric_kind": "gauge",
                "value": 3,
                "labels": {},
            },
        ]
    }
    pages = iter([full_page, short_page])
    token = _jwt(exp=int(time.time()) + 900)
    check._auth_cache[check._auth_cache_key(instance)] = {"token": token, "expires_at": int(time.time()) + 900}
    http = MagicMock()
    http.get.side_effect = lambda *_, **__: next(pages)
    check._load_cursor = MagicMock(return_value=None)
    check._save_cursor = MagicMock()

    with _patch_http(check, http):
        check.check(instance)

    assert http.get.call_count == 2
    assert http.get.call_args_list[0].kwargs["params"]["offset"] == "0"
    assert http.get.call_args_list[1].kwargs["params"]["offset"] == "2"
    aggregator.assert_metric("eden.proxy.a", value=1)
    aggregator.assert_metric("eden.proxy.b", value=2)
    aggregator.assert_metric("eden.proxy.c", value=3)


@pytest.mark.unit
def test_check_refreshes_login_token_on_unauthorized(aggregator):
    check = EdenCheck("eden", {}, [{}])
    old_token = _jwt(exp=int(time.time()) + 900)
    new_token = _jwt(exp=int(time.time()) + 900)
    instance = {
        "url": "https://api.eden.example.com",
        "org_id": "eden",
        "robot_username": "datadog-agent",
        "robot_api_key": "secret",
    }
    check._auth_cache[check._auth_cache_key(instance)] = {"token": old_token, "expires_at": int(time.time()) + 900}

    unauthorized = MagicMock()
    unauthorized.status_code = 401
    ok = MagicMock()
    ok.status_code = 200
    ok.json.return_value = {"rows": []}
    ok.raise_for_status.return_value = None
    login_response = MagicMock()
    login_response.json.return_value = {"token": new_token}
    login_response.raise_for_status.return_value = None
    http = MagicMock()
    responses = iter([unauthorized])

    def _get(*_, **__):
        return next(responses, ok)

    http.get.side_effect = _get
    http.post.return_value = login_response
    check._load_cursor = MagicMock(return_value=None)
    check._save_cursor = MagicMock()

    with _patch_http(check, http):
        check.check(instance)

    aggregator.assert_service_check("eden.api.can_connect", EdenCheck.OK)
    assert http.get.call_args_list[0].kwargs["extra_headers"]["Authorization"] == f"Bearer {old_token}"
    assert http.get.call_args_list[1].kwargs["extra_headers"]["Authorization"] == f"Bearer {new_token}"


def _jwt(exp):
    header = _b64({"alg": "HS256", "typ": "JWT"})
    payload = _b64({"exp": exp})
    return f"{header}.{payload}.signature"


def _b64(payload):
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
    return encoded.rstrip("=")
