"""
Unit tests for the Huntress SIEM → Datadog Logs integration.
Covers all 17 scenarios from PRD §12.
"""
import json
import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from datadog_checks.huntress import HuntressCheck


FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def _load_fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


def _make_instance(**kwargs):
    base = {
        "huntress_api_key": "pub_key",
        "huntress_secret_key": "secret_key",
        "esql_query": "FROM logs",
        "enrich_with_org_tags": False,
        "tags": ["source:huntress", "env:test"],
    }
    base.update(kwargs)
    return base


def _make_check(**kwargs):
    inst = kwargs.pop("instance", None) or _make_instance(**kwargs)
    check = HuntressCheck("huntress", {}, [inst])
    check.log = MagicMock()
    # Use an in-memory dict to prevent persistent cache from bleeding between tests
    _cache = {}
    check.read_persistent_cache = lambda key: _cache.get(key)
    check.write_persistent_cache = lambda key, value: _cache.__setitem__(key, value)
    return check, inst


def _mock_response(status_code, body, headers=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = body
    resp.text = json.dumps(body)
    # Use a real dict so header parsing in _parse_rate_limit_headers works correctly.
    resp.headers = headers if headers is not None else {
        "x-huntress-api-call-limit": "60",
        "x-huntress-api-call-remaining": "55",
    }
    return resp


# ===========================================================================
# 1. Happy path — single page
# ===========================================================================

def test_happy_path_single_page():
    check, instance = _make_check()
    fixture = _load_fixture("siem_query_empty.json")
    fixture["logs"] = _load_fixture("siem_query_page1.json")["logs"][:1]

    with patch.object(check, "_request_with_retry", return_value=_mock_response(200, fixture)) as mock_req, \
         patch.object(check, "_send_logs_batch") as mock_send, \
         patch.object(check, "_save_checkpoint") as mock_save, \
         patch("time.time", side_effect=[1000.0, 1001.0]):

        check.check(instance)

    mock_send.assert_called_once()
    mock_save.assert_called_once()
    batch = mock_send.call_args[0][0]
    assert len(batch) == 1
    assert batch[0]["ddsource"] == "huntress"
    assert batch[0]["message"] == "An account was successfully logged on."


# ===========================================================================
# 2. Happy path — multi-page
# ===========================================================================

def test_happy_path_multi_page():
    check, instance = _make_check()
    page1 = _load_fixture("siem_query_page1.json")
    page2 = _load_fixture("siem_query_page2.json")

    responses = [
        _mock_response(200, page1),
        _mock_response(200, page2),
    ]

    with patch.object(check, "_request_with_retry", side_effect=responses), \
         patch.object(check, "_send_logs_batch") as mock_send, \
         patch.object(check, "_save_checkpoint") as mock_save, \
         patch("time.time", side_effect=[1000.0, 1002.0]):

        check.check(instance)

    assert mock_send.call_count == 2
    all_logs = mock_send.call_args_list[0][0][0] + mock_send.call_args_list[1][0][0]
    assert len(all_logs) == 3
    mock_save.assert_called_once()


# ===========================================================================
# 3. Auth failure (401)
# ===========================================================================

def test_auth_failure_401():
    check, instance = _make_check()

    with patch.object(check, "_request_with_retry",
                      side_effect=Exception("Huntress API 401 Unauthorized")), \
         patch.object(check, "_save_checkpoint") as mock_save, \
         patch.object(check, "count") as mock_count, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        with pytest.raises(Exception, match="401"):
            check.check(instance)

    mock_save.assert_not_called()


def test_auth_failure_401_raises_via_retry():
    """Verify _request_with_retry itself raises on 401."""
    check, instance = _make_check()
    resp = _mock_response(401, {"error": "unauthorized"})

    with patch("requests.request", return_value=resp), \
         patch.object(check, "count") as mock_count:
        with pytest.raises(Exception, match="401"):
            check._request_with_retry("POST", "https://api.huntress.io/v1/siem/query",
                                      {}, json_body={})

    mock_count.assert_called_with("huntress.siem.errors", 1, tags=["error_type:auth_failure"])


# ===========================================================================
# 4. Query timeout (408) — retried twice then aborts
# ===========================================================================

def test_query_timeout_408():
    check, instance = _make_check()
    resp_408 = _mock_response(408, {"error": "timeout"})

    with patch("requests.request", return_value=resp_408), \
         patch("time.sleep") as mock_sleep, \
         patch.object(check, "count") as mock_count:
        with pytest.raises(Exception, match="408"):
            check._request_with_retry("POST", "https://x/q", {}, json_body={})

    # Two retries → sleeps of 2s and 4s
    assert mock_sleep.call_count == 2
    sleep_args = [c[0][0] for c in mock_sleep.call_args_list]
    assert sleep_args == [2, 4]
    mock_count.assert_called_with("huntress.siem.errors", 1, tags=["error_type:timeout"])


# ===========================================================================
# 5. Rate limit (429) — sleeps 60s and retries
# ===========================================================================

def test_rate_limit_429_then_success():
    check, instance = _make_check()
    resp_429 = _mock_response(429, {"error": "rate_limited"})
    resp_200 = _mock_response(200, _load_fixture("siem_query_empty.json"))

    with patch("requests.request", side_effect=[resp_429, resp_200]), \
         patch("time.sleep") as mock_sleep:
        result = check._request_with_retry("POST", "https://x/q", {}, json_body={})

    mock_sleep.assert_called_once_with(60)
    assert result.status_code == 200


# ===========================================================================
# 6. Invalid ES|QL (422)
# ===========================================================================

def test_invalid_esql_422():
    check, instance = _make_check()
    resp_422 = _mock_response(422, {"error": "invalid query"})

    with patch("requests.request", return_value=resp_422), \
         patch.object(check, "count") as mock_count:
        with pytest.raises(Exception, match="422"):
            check._request_with_retry("POST", "https://x/q", {}, json_body={})

    mock_count.assert_called_with("huntress.siem.errors", 1, tags=["error_type:invalid_query"])


# ===========================================================================
# 7. Checkpoint persistence — second run uses previous range_end as range_start
# ===========================================================================

def test_checkpoint_persistence():
    check, instance = _make_check()
    saved_ts = "2026-05-27T13:00:00.000Z"
    instance_hash = check._instance_hash(instance)
    check.write_persistent_cache(
        check.CHECKPOINT_CACHE_KEY_PREFIX + instance_hash,
        json.dumps({"last_collected_at": saved_ts, "schema_version": 1}),
    )

    captured_bodies = []

    def capture_request(method, url, headers, json_body=None, params=None):
        if json_body:
            captured_bodies.append(json_body)
        return _mock_response(200, _load_fixture("siem_query_empty.json"))

    with patch.object(check, "_request_with_retry", side_effect=capture_request), \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)

    assert captured_bodies, "No SIEM query was made"
    # range_start should be 1ms after saved_ts
    assert captured_bodies[0]["range_start"] == "2026-05-27T13:00:00.001Z"


# ===========================================================================
# 8. No checkpoint (first run) — range_start defaults to now - interval
# ===========================================================================

def test_no_checkpoint_first_run():
    check, instance = _make_check(min_collection_interval=900)
    captured_bodies = []

    def capture_request(method, url, headers, json_body=None, params=None):
        if json_body:
            captured_bodies.append(json_body)
        return _mock_response(200, _load_fixture("siem_query_empty.json"))

    fixed_now = datetime(2026, 5, 27, 14, 0, 0, tzinfo=timezone.utc)
    with patch.object(check, "_request_with_retry", side_effect=capture_request), \
         patch("datadog_checks.huntress.huntress.datetime") as mock_dt, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        mock_dt.now.return_value = fixed_now
        mock_dt.fromisoformat = datetime.fromisoformat
        check.check(instance)

    assert captured_bodies
    body = captured_bodies[0]
    range_start = datetime.fromisoformat(body["range_start"].replace("Z", "+00:00"))
    range_end = datetime.fromisoformat(body["range_end"].replace("Z", "+00:00"))
    diff_seconds = (range_end - range_start).total_seconds()
    assert abs(diff_seconds - 900) < 2


# ===========================================================================
# 9. ES|QL validation — query not starting with FROM logs raises ConfigurationError
# ===========================================================================

def test_esql_validation_rejects_bad_query():
    check, instance = _make_check(esql_query="SELECT * FROM logs")
    with pytest.raises(Exception, match="FROM logs"):
        check.check(instance)


def test_esql_validation_accepts_from_logs():
    check, instance = _make_check(esql_query="FROM logs | KEEP @timestamp, message")
    with patch.object(check, "_request_with_retry",
                      return_value=_mock_response(200, _load_fixture("siem_query_empty.json"))), \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)  # should not raise


def test_esql_validation_case_insensitive():
    check, instance = _make_check(esql_query="from logs | limit 100")
    with patch.object(check, "_request_with_retry",
                      return_value=_mock_response(200, _load_fixture("siem_query_empty.json"))), \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)  # should not raise


# ===========================================================================
# 10. Log transformation — ECS fields correctly mapped to Datadog payload
# ===========================================================================

def test_log_transformation():
    check, instance = _make_check()
    raw = {
        "@timestamp": "2026-05-27T14:00:00.000Z",
        "log.original": "An account was successfully logged on.",
        "message": "fallback message",
        "event.provider": "Microsoft-Windows-Security-Auditing",
        "host.hostname": "DESKTOP-ABC123",
        "event.category": "authentication",
    }
    tags = ["source:huntress", "env:test", "huntress_account_id:42"]
    payload = check._transform_log(raw, tags, "huntress-siem")

    assert payload["message"] == "An account was successfully logged on."
    assert payload["ddsource"] == "huntress"
    assert payload["service"] == "huntress-siem"
    assert payload["ddtags"] == "source:huntress,env:test,huntress_account_id:42"
    assert payload["date"] == 1779890400000
    assert payload["event.provider"] == "Microsoft-Windows-Security-Auditing"
    assert payload["host.hostname"] == "DESKTOP-ABC123"
    assert "@timestamp" not in payload
    assert "log.original" not in payload


def test_log_transformation_fallback_message():
    check, instance = _make_check()
    raw = {"message": "fallback used", "@timestamp": "2026-05-27T14:00:00.000Z"}
    payload = check._transform_log(raw, [], "huntress-siem")
    assert payload["message"] == "fallback used"


def test_log_transformation_json_fallback():
    check, instance = _make_check()
    raw = {"event.category": "network", "@timestamp": "2026-05-27T14:00:00.000Z"}
    payload = check._transform_log(raw, [], "huntress-siem")
    assert "event.category" in payload["message"]


# ===========================================================================
# 11. Batching — >1,000 logs split into multiple batches
# ===========================================================================

def test_batching_over_1000_logs():
    check, instance = _make_check()

    large_log_list = [
        {
            "@timestamp": "2026-05-27T14:00:00.000Z",
            "message": f"log {i}",
        }
        for i in range(1500)
    ]
    fixture = {"logs": large_log_list, "pagination": {}}

    with patch.object(check, "_request_with_retry", return_value=_mock_response(200, fixture)), \
         patch.object(check, "_send_logs_batch") as mock_send, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)

    assert mock_send.call_count == 2
    first_batch = mock_send.call_args_list[0][0][0]
    second_batch = mock_send.call_args_list[1][0][0]
    assert len(first_batch) == 1000
    assert len(second_batch) == 500


# ===========================================================================
# 12. max_pages_per_run cap — stops after N pages; checkpoint does NOT advance
# ===========================================================================

def test_max_pages_per_run_cap():
    check, instance = _make_check(max_pages_per_run=1)
    page1 = _load_fixture("siem_query_page1.json")

    with patch.object(check, "_request_with_retry", return_value=_mock_response(200, page1)), \
         patch.object(check, "_save_checkpoint") as mock_save, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)

    mock_save.assert_not_called()


# ===========================================================================
# 13. Org enrichment — cache hit (no extra API calls)
# ===========================================================================

def test_org_enrichment_cache_hit():
    check, instance = _make_check(enrich_with_org_tags=True)
    instance_hash = check._instance_hash(instance)

    # Pre-populate cache (fresh)
    from datetime import datetime, timezone
    cache = {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "account_id": 42,
        "orgs": {
            "101": {"name": "Acme Inc.", "key": "acme", "account_id": 42},
        },
    }
    check.write_persistent_cache(check.ORG_CACHE_KEY_PREFIX + instance_hash, json.dumps(cache))

    page1 = _load_fixture("siem_query_page1.json")
    page1["pagination"] = {}

    api_calls = []

    def side_effect(method, url, headers, json_body=None, params=None):
        api_calls.append(url)
        return _mock_response(200, page1)

    with patch.object(check, "_request_with_retry", side_effect=side_effect), \
         patch.object(check, "_send_logs_batch") as mock_send, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)

    # Only the SIEM query should have been called — no org API calls
    assert all("/siem/query" in u for u in api_calls)

    # Verify org tags applied
    batch = mock_send.call_args_list[0][0][0]
    first_log_tags = batch[0]["ddtags"]
    assert "huntress_org_name:Acme Inc." in first_log_tags
    assert "huntress_org_key:acme" in first_log_tags
    assert "huntress_account_id:42" in first_log_tags


# ===========================================================================
# 14. Org enrichment — cache miss (fetches account + orgs)
# ===========================================================================

def test_org_enrichment_cache_miss():
    check, instance = _make_check(enrich_with_org_tags=True)

    account_resp = _mock_response(200, {"account": {"id": 42}})
    orgs_resp = _mock_response(200, {
        "organizations": [
            {"id": 101, "name": "Acme Inc.", "key": "acme"},
        ],
        "pagination": {},
    })
    siem_resp = _mock_response(200, {
        "logs": _load_fixture("siem_query_page1.json")["logs"][:1],
        "pagination": {},
    })

    call_urls = []

    def side_effect(method, url, headers, json_body=None, params=None):
        call_urls.append(url)
        if "/account" in url and "organization" not in url:
            return account_resp
        elif "organizations" in url:
            return orgs_resp
        else:
            return siem_resp

    with patch.object(check, "_request_with_retry", side_effect=side_effect), \
         patch.object(check, "_send_logs_batch") as mock_send, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)

    assert any("/account" in u for u in call_urls)
    assert any("organizations" in u for u in call_urls)

    batch = mock_send.call_args_list[0][0][0]
    assert "huntress_account_id:42" in batch[0]["ddtags"]


# ===========================================================================
# 15. Org enrichment — fetch failure → warning, logs collected without org tags
# ===========================================================================

def test_org_enrichment_fetch_failure():
    check, instance = _make_check(enrich_with_org_tags=True)
    siem_resp = _mock_response(200, {
        "logs": _load_fixture("siem_query_page1.json")["logs"][:1],
        "pagination": {},
    })

    def side_effect(method, url, headers, json_body=None, params=None):
        if "/account" in url and "organization" not in url:
            raise Exception("Network error fetching account")
        return siem_resp

    with patch.object(check, "_request_with_retry", side_effect=side_effect), \
         patch.object(check, "_send_logs_batch") as mock_send, \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)  # must not raise

    check.log.warning.assert_called()
    # Logs should still be sent
    mock_send.assert_called()
    batch = mock_send.call_args_list[0][0][0]
    # No org tags on logs
    assert "huntress_org_name" not in batch[0]["ddtags"]


# ===========================================================================
# 16. Org enrichment — no org match → only huntress_account_id tag
# ===========================================================================

def test_org_enrichment_no_org_match():
    check, instance = _make_check()
    org_cache = {
        "fetched_at": "2026-05-27T14:00:00.000Z",
        "account_id": 42,
        "orgs": {"101": {"name": "Acme Inc.", "key": "acme", "account_id": 42}},
    }
    raw_log = {"@timestamp": "2026-05-27T14:00:00.000Z", "message": "no org field"}
    tags = check._get_org_tags(raw_log, org_cache)

    assert "huntress_account_id:42" in tags
    assert not any("org_name" in t or "org_key" in t for t in tags)


# ===========================================================================
# 17. Multi-instance isolation — independent checkpoints and org caches
# ===========================================================================

def test_multi_instance_isolation():
    instance_a = _make_instance(
        huntress_api_key="key_a",
        huntress_secret_key="secret_a",
        esql_query="FROM logs",
    )
    instance_b = _make_instance(
        huntress_api_key="key_b",
        huntress_secret_key="secret_b",
        esql_query="FROM logs",
    )

    check_a = HuntressCheck("huntress", {}, [instance_a])
    check_a.log = MagicMock()
    _cache_a = {}
    check_a.read_persistent_cache = lambda key: _cache_a.get(key)
    check_a.write_persistent_cache = lambda key, value: _cache_a.__setitem__(key, value)

    check_b = HuntressCheck("huntress", {}, [instance_b])
    check_b.log = MagicMock()
    _cache_b = {}
    check_b.read_persistent_cache = lambda key: _cache_b.get(key)
    check_b.write_persistent_cache = lambda key, value: _cache_b.__setitem__(key, value)

    hash_a = check_a._instance_hash(instance_a)
    hash_b = check_b._instance_hash(instance_b)

    assert hash_a != hash_b

    # Checkpoints stored under different keys must return different values
    check_a._save_checkpoint(hash_a, "2026-05-27T14:00:00.000Z")
    check_b._save_checkpoint(hash_b, "2026-05-27T15:00:00.000Z")

    assert check_a._load_checkpoint(hash_a) == "2026-05-27T14:00:00.000Z"
    assert check_b._load_checkpoint(hash_b) == "2026-05-27T15:00:00.000Z"
    # Each check's cache is isolated — A cannot see B's checkpoint
    assert check_a._load_checkpoint(hash_b) is None


# ===========================================================================
# Bonus: _get_org_tags strategies
# ===========================================================================

def test_org_tags_by_id():
    check, _ = _make_check()
    org_cache = {
        "account_id": 42,
        "orgs": {"101": {"name": "Acme Inc.", "key": "acme", "account_id": 42}},
    }
    raw = {"organization.id": 101}
    tags = check._get_org_tags(raw, org_cache)
    assert "huntress_org_id:101" in tags
    assert "huntress_org_name:Acme Inc." in tags
    assert "huntress_org_key:acme" in tags
    assert "huntress_account_id:42" in tags


def test_org_tags_by_name_reverse_lookup():
    check, _ = _make_check()
    org_cache = {
        "account_id": 42,
        "orgs": {"101": {"name": "Acme Inc.", "key": "acme", "account_id": 42}},
    }
    raw = {"organization.name": "Acme Inc."}
    tags = check._get_org_tags(raw, org_cache)
    assert "huntress_org_name:Acme Inc." in tags
    assert "huntress_org_key:acme" in tags


def test_org_tags_nested_org_field():
    """organization field as a nested dict (e.g. from ECS nested structure)."""
    check, _ = _make_check()
    org_cache = {
        "account_id": 42,
        "orgs": {"101": {"name": "Acme Inc.", "key": "acme", "account_id": 42}},
    }
    raw = {"organization": {"id": 101, "name": "Acme Inc."}}
    tags = check._get_org_tags(raw, org_cache)
    assert "huntress_org_name:Acme Inc." in tags


# ===========================================================================
# Rate limit header parsing
# ===========================================================================

def test_rate_limit_headers_parsed_and_stored():
    """_parse_rate_limit_headers populates _last_api_call_* attributes."""
    check, _ = _make_check()
    check._last_api_call_limit = None
    check._last_api_call_remaining = None

    resp = _mock_response(200, {}, headers={
        "x-huntress-api-call-limit": "60",
        "x-huntress-api-call-remaining": "42",
    })
    check._parse_rate_limit_headers(resp)

    assert check._last_api_call_limit == 60
    assert check._last_api_call_remaining == 42


def test_rate_limit_warning_when_low():
    """Warning is logged when remaining drops below 10."""
    check, _ = _make_check()
    check._last_api_call_limit = None
    check._last_api_call_remaining = None

    resp = _mock_response(200, {}, headers={
        "x-huntress-api-call-limit": "60",
        "x-huntress-api-call-remaining": "3",
    })
    check._parse_rate_limit_headers(resp)

    check.log.warning.assert_called()
    assert check._last_api_call_remaining == 3


def test_rate_limit_headers_missing_gracefully():
    """Missing rate limit headers do not raise; attributes stay None."""
    check, _ = _make_check()
    check._last_api_call_limit = None
    check._last_api_call_remaining = None

    resp = _mock_response(200, {}, headers={"Content-Type": "application/json"})
    check._parse_rate_limit_headers(resp)

    assert check._last_api_call_limit is None
    assert check._last_api_call_remaining is None


def test_rate_limit_metrics_emitted_in_check():
    """huntress.siem.api_call_* gauges are emitted when headers were present."""
    check, instance = _make_check()
    fixture = _load_fixture("siem_query_empty.json")
    fixture["logs"] = []

    emitted_gauges = {}

    def capture_gauge(name, value, tags=None):
        emitted_gauges[name] = value

    real_request_with_retry = check._request_with_retry

    def fake_retry(method, url, headers, json_body=None, params=None):
        resp = _mock_response(200, fixture, headers={
            "x-huntress-api-call-limit": "60",
            "x-huntress-api-call-remaining": "48",
        })
        check._parse_rate_limit_headers(resp)
        return resp

    with patch.object(check, "_request_with_retry", side_effect=fake_retry), \
         patch.object(check, "gauge", side_effect=capture_gauge), \
         patch("time.time", side_effect=[1000.0, 1001.0]):
        check.check(instance)

    assert emitted_gauges.get("huntress.siem.api_call_limit") == 60
    assert emitted_gauges.get("huntress.siem.api_call_remaining") == 48
