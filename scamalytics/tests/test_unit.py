from datetime import datetime, timedelta, timezone
from unittest.mock import ANY, MagicMock, patch

import pytest

from datadog_checks.base import ConfigurationError

# Ensure this import matches your directory structure
from datadog_checks.scamalytics.check import (
    ScamalyticsCheck,
    ScamalyticsLogStream,
    parse_iso8601_timestamp,
)

# --- Fixtures (Setup) ---


@pytest.fixture
def instance_config():
    """Standard valid configuration."""
    return {
        "scamalytics_api_key": "test_scam_key",
        "scamalytics_api_url": "https://api.test.com/",
        "customer_id": "test_cust_id",
        "dd_api_key": "test_dd_key",
        "dd_app_key": "test_dd_app",
        "skip_window_hours": 24,
        "dd_site": "datadoghq.com",
    }


@pytest.fixture
def check_mock(instance_config):
    """Mocks the parent Check class to avoid loading real Agent config."""
    check = MagicMock(spec=ScamalyticsCheck)
    check.instance = instance_config
    check.log = MagicMock()
    # Mock persistent cache methods (Agent internals)
    check.read_persistent_cache.return_value = "{}"
    check.write_persistent_cache.return_value = None
    return check


@pytest.fixture
def stream(check_mock):
    """Creates a stream instance with the mocked check."""
    # FIX: Pass arguments explicitly using keywords to match your updated class
    return ScamalyticsLogStream(check=check_mock, name="test_stream")


# --- 1. Helper Function Tests ---


def test_parse_iso8601_timestamp():
    # Test Standard Z
    dt = parse_iso8601_timestamp("2023-01-01T12:00:00Z")
    assert dt.tzinfo == timezone.utc
    assert dt.hour == 12

    # Test Offset
    dt = parse_iso8601_timestamp("2023-01-01T12:00:00+00:00")
    assert dt.tzinfo == timezone.utc

    # Test Naive Fallback
    dt = parse_iso8601_timestamp("2023-01-01T12:00:00.000")
    assert dt.tzinfo == timezone.utc

    # Test None
    assert parse_iso8601_timestamp(None) is None


@pytest.mark.parametrize(
    "ip, is_public",
    [
        ("8.8.8.8", True),  # Google (Public)
        ("1.1.1.1", True),  # Cloudflare (Public)
        ("10.0.0.1", False),  # Private Class A
        ("192.168.0.1", False),  # Private Class C
        ("172.16.0.1", False),  # Private Class B (Start)
        ("172.31.255.255", False),  # Private Class B (End)
        ("127.0.0.1", False),  # Loopback
        ("169.254.1.1", False),  # Link-Local
    ],
)
def test_is_public_ip(ip, is_public):
    assert ScamalyticsLogStream._is_public_ip(ip) is is_public


# --- 2. Configuration Tests ---


def test_config_validation_success(instance_config):
    check = ScamalyticsCheck("test", {}, [instance_config])
    assert check.instance == instance_config


def test_config_validation_failure(instance_config):
    # Remove a required key
    del instance_config["scamalytics_api_key"]

    with pytest.raises(ConfigurationError) as excinfo:
        ScamalyticsCheck("test", {}, [instance_config])
    assert "Missing required configuration key" in str(excinfo.value)


def test_records_happy_path_new_ip(stream):
    """
    Scenario:
    1. Datadog Logs return 1 log with a public IP (8.8.8.8).
    2. Remote Check returns EMPTY (Ensures we DO NOT skip the API call).
    3. Scamalytics API is called.
    4. Record is yielded.
    """
    # 1. Main Log Search Response (Found the IP)
    dd_logs_found = {
        "data": [{"attributes": {"timestamp": "2023-01-01T12:00:00Z", "message": "Connection from 8.8.8.8"}}]
    }

    # 2. Remote Deduplication Check Response (NOT Found - safe to process)
    # This ensures the code proceeds to line 162
    dd_remote_empty = {"data": []}

    scam_resp = {"ip": "8.8.8.8", "score": 100, "risk": "high"}

    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        # Use side_effect to handle the two distinct Datadog calls
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: dd_logs_found),  # Call 1: Fetch Logs
            MagicMock(status_code=200, json=lambda: dd_remote_empty),  # Call 2: Remote Check
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = scam_resp

        # Run
        records = list(stream.records(cursor=None))

        # Assertions
        assert len(records) == 1
        assert records[0].data["attributes"]["score"] == 100

        # Verify the API block actually ran
        mock_get.assert_called_once()
        assert "8.8.8.8" in stream.recent_cache


def test_records_skips_private_ips(stream):
    """Scenario: Log contains 192.168.1.1. Should be ignored entirely."""
    dd_logs = {"data": [{"attributes": {"timestamp": "2023-01-01T12:00:00Z", "message": "Internal 192.168.1.1"}}]}

    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = dd_logs

        records = list(stream.records())

        assert len(records) == 0
        mock_get.assert_not_called()  # No Scamalytics call


def test_records_skips_cached_ips(stream):
    """Scenario: IP 1.1.1.1 is in persistent cache (processed recently)."""
    # Pre-populate cache with 'now'
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stream.recent_cache = {"1.1.1.1": now_str}

    dd_logs = {"data": [{"attributes": {"timestamp": now_str, "message": "User 1.1.1.1"}}]}

    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = dd_logs

        records = list(stream.records())

        assert len(records) == 0
        mock_get.assert_not_called()
        stream.check.log.info.assert_any_call("SCAMALYTICS: SKIP %s (persistent cache <%sh)", "1.1.1.1", 24)


def test_records_remote_fallback(stream):
    """
    Scenario: IP 2.2.2.2 is NOT in local cache, but IS found in remote Datadog logs
    (meaning another agent instance processed it).
    """
    target_ip = "2.2.2.2"

    # First call: Main log fetch returns the IP
    main_logs = {"data": [{"attributes": {"timestamp": "2023-01-01T12:00:00Z", "message": target_ip}}]}

    # Second call: Remote check returns a result (it was found)
    remote_check_logs = {"data": [{"id": "found_it"}]}

    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        # side_effect allows different returns for consecutive calls
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: main_logs),
            MagicMock(status_code=200, json=lambda: remote_check_logs),
        ]

        records = list(stream.records())

        assert len(records) == 0
        mock_get.assert_not_called()  # No Scamalytics call
        assert target_ip in stream.recent_cache  # Should populate local cache now


# --- 4. Error Handling Tests ---


def test_dd_api_error_handling(stream):
    """Scenario: Datadog API is down."""
    with patch("requests.post", side_effect=Exception("Network Down")):
        records = list(stream.records())
        assert len(records) == 0
        stream.check.log.error.assert_called_with("SCAMALYTICS: error fetching logs: %s", ANY)


# --- 5. Cache Lifecycle Tests ---


def test_prune_expired_cache(stream):
    """Scenario: Cache contains old and new entries. Old should be deleted."""
    now = datetime.now(timezone.utc)

    # 25 hours ago (Expired)
    old_ts = (now - timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # 1 hour ago (Valid)
    new_ts = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    stream.recent_cache = {
        "old_ip": old_ts,
        "new_ip": new_ts,
        "bad_ts_ip": "invalid-timestamp",  # Should be treated as expired/removed
    }

    stream._prune_expired_cache()

    assert "old_ip" not in stream.recent_cache
    assert "bad_ts_ip" not in stream.recent_cache
    assert "new_ip" in stream.recent_cache


def test_load_persistent_cache_corrupt(check_mock):
    """Scenario: Agent returns garbage JSON for the cache file."""
    check_mock.read_persistent_cache.return_value = "{ broken json"

    # FIX APPLIED HERE: Initialize using explicit keyword arguments
    stream = ScamalyticsLogStream(check=check_mock, name="test")

    assert stream.recent_cache == {}  # Should default to empty dict
    check_mock.log.warning.assert_called()


def test_cursor_handling_with_overlap(stream):
    """Scenario: Stream starts with a cursor, ensuring we request overlapping time."""
    cursor_ts = "2023-01-01T12:00:00Z"
    cursor = {"timestamp": cursor_ts}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"data": []}

        list(stream.records(cursor=cursor))

        # Verify the 'from' param in the API call includes the overlap subtraction
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        from_param = payload['filter']['from']

        # 12:00:00 - 2 seconds = 11:59:58
        assert "11:59:58" in from_param
