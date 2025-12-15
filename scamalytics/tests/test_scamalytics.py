import pytest
import json
from unittest.mock import MagicMock
from datetime import datetime, timezone

from datadog_checks.base import ConfigurationError
# Import the actual classes to test
from datadog_checks.scamalytics.check import ScamalyticsCheck

# =====================================================================
#  UTILITY FIXTURES / SETUP
# =====================================================================

@pytest.fixture
def instance_config():
    """Returns a valid configuration dictionary."""
    return {
        'scamalytics_api_key': 'test_scam_key',
        'scamalytics_api_url': 'https://api.scamalytics.com/',
        'customer_id': 'test_customer',
        'dd_api_key': 'test_dd_key',
        'dd_app_key': 'test_dd_app',
        'dd_site': 'datadoghq.com',
        'skip_window_hours': 24,
    }

@pytest.fixture
def check(instance_config):
    """
    Creates a REAL instance of ScamalyticsCheck.
    We mock the methods that interact with the Agent (cache/log) 
    so we can test the python logic in isolation.
    """
    check = ScamalyticsCheck('scamalytics', {}, [instance_config])
    
    # Mock the internal logger to avoid clutter and verify logs
    check.log = MagicMock()
    
    # Mock persistent cache methods (Agent features)
    check.read_persistent_cache = MagicMock(return_value=None)
    check.write_persistent_cache = MagicMock()
    
    return check

# =====================================================================
#  CONFIGURATION & UTILS
# =====================================================================

@pytest.mark.unit
def test_config_validation():
    """Test that missing configuration raises ConfigurationError."""
    with pytest.raises(ConfigurationError):
        ScamalyticsCheck('scamalytics', {}, [{}])

@pytest.mark.unit
def test_timestamp_utils():
    """Test the static timestamp parsing logic (coverage for helper function)."""
    from datadog_checks.scamalytics.check import parse_iso8601_timestamp
    
    # Case 1: None input
    assert parse_iso8601_timestamp(None) is None
    
    # Case 2: Z suffix (UTC)
    dt = parse_iso8601_timestamp("2023-01-01T12:00:00Z")
    assert dt.tzinfo == timezone.utc
    assert dt.hour == 12
    
    # Case 3: Naive input (force UTC)
    dt_naive = parse_iso8601_timestamp("2023-01-01T12:00:00")
    assert dt_naive.tzinfo == timezone.utc

# =====================================================================
#  MAIN LOGIC TESTS (HAPPY PATH)
# =====================================================================

@pytest.mark.unit
def test_happy_path_flow(check, requests_mock):
    """
    Test the full flow:
    1. Fetch logs from DD (returns 1 public IP).
    2. Check local cache (empty).
    3. Check remote logs (empty).
    4. Call Scamalytics API (success).
    5. Yield enriched log.
    """
    # 1. Mock Datadog Logs API (Initial Search)
    requests_mock.post(
        "https://api.datadoghq.com/api/v2/logs/events/search",
        json={
            "data": [{
                "attributes": {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "message": "User login from 8.8.8.8" 
                }
            }]
        }
    )
    
    # 2. Mock Scamalytics API (Enrichment)
    requests_mock.get(
        "https://api.scamalytics.com/8.8.8.8",
        json={"ip": "8.8.8.8", "score": 10, "risk": "low"},
        status_code=200
    )
    
    # Initialize the stream and run
    stream = check.get_log_streams()[0]
    results = list(stream.records(cursor=None))
    
    # Assertions
    assert len(results) == 1
    assert results[0].data['attributes']['score'] == 10
    assert "8.8.8.8" in results[0].data['message']
    
    # Verify we tried to write to persistent cache
    check.write_persistent_cache.assert_called()

# =====================================================================
#  ERROR HANDLING & EDGE CASES (THE "MISSING" COVERAGE)
# =====================================================================

@pytest.mark.unit
def test_private_ip_filtering(check, requests_mock):
    """Ensure private IPs (192.168.x.x) are filtered out silently."""
    requests_mock.post(
        "https://api.datadoghq.com/api/v2/logs/events/search",
        json={
            "data": [{
                "attributes": {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "message": "Internal request 192.168.1.50" 
                }
            }]
        }
    )
    
    stream = check.get_log_streams()[0]
    results = list(stream.records(cursor=None))
    
    # Should yield nothing
    assert len(results) == 0

@pytest.mark.unit
def test_scamalytics_api_failure(check, requests_mock):
    """Ensure we handle Scamalytics API 500 errors gracefully."""
    # 1. DD returns valid IP
    requests_mock.post(
        "https://api.datadoghq.com/api/v2/logs/events/search",
        json={"data": [{"attributes": {"timestamp": "2025-01-01T12:00:00Z", "message": "1.1.1.1"}}]}
    )
    
    # 2. Scamalytics returns 500
    requests_mock.get("https://api.scamalytics.com/1.1.1.1", status_code=500)
    
    stream = check.get_log_streams()[0]
    results = list(stream.records(cursor=None))
    
    # Should skip this IP and log error
    assert len(results) == 0
    check.log.error.assert_called_with("SCAMALYTICS: Scamalytics API error for %s: %s", "1.1.1.1", pytest.any_arg())

@pytest.mark.unit
def test_datadog_logs_api_failure(check, requests_mock):
    """Ensure we handle Datadog Logs API 500 errors."""
    requests_mock.post("https://api.datadoghq.com/api/v2/logs/events/search", status_code=500)
    
    stream = check.get_log_streams()[0]
    results = list(stream.records(cursor=None))
    
    # Should return safely with 0 results
    assert len(results) == 0
    check.log.error.assert_called_with("SCAMALYTICS: error fetching logs: %s", pytest.any_arg())

@pytest.mark.unit
def test_cache_persistence_failure(check):
    """Ensure disk I/O errors don't crash the check."""
    # Force read/write to raise exceptions
    check.read_persistent_cache.side_effect = Exception("Disk Corrupt")
    check.write_persistent_cache.side_effect = Exception("Disk Full")
    
    stream = check.get_log_streams()[0] # Triggers read
    stream._save_recent_cache()         # Triggers write
    
    # Verify warnings were logged
    check.log.warning.assert_any_call("SCAMALYTICS: failed to load persistent cache: %s", pytest.any_arg())
    check.log.warning.assert_any_call("SCAMALYTICS: failed to save persistent cache: %s", pytest.any_arg())

# =====================================================================
#  REMOTE DEDUPLICATION LOGIC
# =====================================================================

@pytest.mark.unit
def test_remote_fallback_found_skips_ip(check, requests_mock):
    """If IP is found in recent remote logs, we should SKIP it."""
    # 1. DD Logs returns new IP
    requests_mock.post(
        "https://api.datadoghq.com/api/v2/logs/events/search",
        [{
            "json": {"data": [{"attributes": {"timestamp": "2025-01-01T12:00:00Z", "message": "2.2.2.2"}}]}
        },
        # 2. Remote Look-up (the dedup check) returns "Found"
        {
            "json": {"data": [{"id": "previous_log"}]}
        }]
    )
    
    stream = check.get_log_streams()[0]
    results = list(stream.records(cursor=None))
    
    # Should be empty because we skipped it
    assert len(results) == 0
    check.log.info.assert_any_call("SCAMALYTICS: SKIP %s (remote logs <%sh)", "2.2.2.2", 24)

@pytest.mark.unit
def test_remote_fallback_failure_fails_open(check, requests_mock):
    """If Remote Look-up fails (network error), we should PROCESS the IP (Fail Open)."""
    # 1. DD Logs returns new IP
    requests_mock.post(
        "https://api.datadoghq.com/api/v2/logs/events/search",
        [{
            "json": {"data": [{"attributes": {"timestamp": "2025-01-01T12:00:00Z", "message": "3.3.3.3"}}]}
        },
        # 2. Remote Look-up FAILS (500)
        {
            "status_code": 500
        }]
    )
    
    # 3. Scamalytics API succeeds (because we proceeded anyway)
    requests_mock.get("https://api.scamalytics.com/3.3.3.3", json={"score": 5})

    stream = check.get_log_streams()[0]
    results = list(stream.records(cursor=None))
    
    # Should contain the result
    assert len(results) == 1
    check.log.warning.assert_any_call("SCAMALYTICS: remote recent-check failed for %s: %s", "3.3.3.3", pytest.any_arg())