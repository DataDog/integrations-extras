import os
import json
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone

import pytest

from datadog_checks.base import ConfigurationError
# Import the actual classes to test
from datadog_checks.scamalytics.check import ScamalyticsCheck, ScamalyticsLogStream


# =====================================================================
#  UTILITY FIXTURES / SETUP
# =====================================================================

@pytest.fixture
def mock_check(mocker):
    """Fixture to create a mock check instance with required components."""
    mock_check_instance = mocker.MagicMock(spec=ScamalyticsCheck)
    mock_check_instance.instance = {
        'scamalytics_api_key': 'test_scam_key',
        'scamalytics_api_url': 'http://scam-api.com/?ip=',
        'customer_id': 'test_customer',
        'dd_api_key': 'test_dd_key',
        'dd_app_key': 'test_dd_app',
        'dd_site': 'datadoghq.com',
        'skip_window_hours': 24,
    }
    # Mock persistent cache functions to return None by default
    mock_check_instance.read_persistent_cache.return_value = None
    mock_check_instance.write_persistent_cache.return_value = None
    mock_check_instance.log = mocker.MagicMock() # Mock the logger for checking messages
    return mock_check_instance


# =====================================================================
#  ORIGINAL UNIT TESTS
# =====================================================================


@pytest.mark.unit
def test_config_validation():
    """
    Validate configuration handling for the ScamalyticsCheck.
    Ensures ConfigurationError is raised when required fields are missing.
    """

    # Missing all keys
    with pytest.raises(ConfigurationError):
        ScamalyticsCheck('scamalytics', {}, [{}])

    # Missing some required keys
    with pytest.raises(ConfigurationError):
        ScamalyticsCheck('scamalytics', {}, [{'scamalytics_api_key': 'dummy'}])

    # Valid instance
    valid_instance = {
        'scamalytics_api_key': 'test_key',
        'scamalytics_api_url': 'https://api-ti-us.scamalytics.com/tiprem/?ip=',
        'customer_id': 'test_customer',
        'dd_api_key': 'test_dd_key',
        'dd_app_key': 'test_dd_app',
    }

    check = ScamalyticsCheck('scamalytics', {}, [valid_instance])
    assert check.instance == valid_instance


@pytest.mark.unit
def test_is_public_ip():
    """
    Verify internal logic for IP classification works correctly.
    """

    # Public IPs
    assert ScamalyticsLogStream._is_public_ip("8.8.8.8") is True
    assert ScamalyticsLogStream._is_public_ip("1.1.1.1") is True

    # Private IPs
    assert ScamalyticsLogStream._is_public_ip("192.168.1.5") is False
    assert ScamalyticsLogStream._is_public_ip("10.0.0.1") is False
    assert ScamalyticsLogStream._is_public_ip("172.16.0.5") is False
    assert ScamalyticsLogStream._is_public_ip("127.0.0.1") is False
    assert ScamalyticsLogStream._is_public_ip("169.254.5.10") is False


# =====================================================================
#  NEW UNIT TESTS FOR COVERAGE
# =====================================================================

@pytest.mark.unit
@patch('datadog_checks.scamalytics.check.requests.post')
def test_records_dd_fetch_failure(mock_post, mock_check):
    """
    Test the exception handling when the Datadog logs search API fails.
    (Covers lines 104-105 in check.py)
    """
    # 1. Setup: Simulate a connection error when fetching logs
    mock_post.side_effect = requests.exceptions.ConnectionError("DD Logs connection failed")

    # 2. Arrange: Initialize stream
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")

    # 3. Act: Run the records generator
    records = list(stream.records())

    # 4. Assert: No records should be yielded, and error should be logged.
    assert len(records) == 0
    mock_check.log.error.assert_called_with(
        "SCAMALYTICS: error fetching logs: %s", mock_post.side_effect
    )

@pytest.mark.unit
@patch('datadog_checks.scamalytics.check.requests.post')
@patch('datadog_checks.scamalytics.check.requests.get')
def test_records_deduplication_and_remote_skip(mock_scam_get, mock_dd_post, mock_check):
    """
    Test all three skip/deduplication paths:
    1. Persistent cache (local)
    2. Remote check (DD logs search)
    3. Session cache (in-memory)
    (Covers lines 152-167 in check.py)
    """
    ip_to_process = "8.8.8.8"
    ip_local_skip = "1.1.1.1"
    ip_remote_skip = "2.2.2.2"
    ip_session_skip = "2.2.2.2" # Same IP as remote skip, processed later in the same run

    # --- Setup 1: Mock Datadog Log Fetch (Input Logs) ---
    mock_dd_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": [
                # Log 1: Will be processed
                {"attributes": {"timestamp": "2025-10-15T10:00:00Z", "message": f"IP {ip_to_process}"}, "type": "log"},
                # Log 2: Will be skipped by local persistent cache
                {"attributes": {"timestamp": "2025-10-15T10:00:00Z", "message": f"IP {ip_local_skip}"}, "type": "log"},
                # Log 3: Will be skipped by remote DD search
                {"attributes": {"timestamp": "2025-10-15T10:00:00Z", "message": f"IP {ip_remote_skip}"}, "type": "log"},
                # Log 4: Will be skipped by session cache (after Log 3 is processed)
                {"attributes": {"timestamp": "2025-10-15T10:00:00Z", "message": f"IP {ip_session_skip}"}, "type": "log"},
            ]
        },
        raise_for_status=lambda: None,
    )

    # --- Setup 2: Mock Local Persistent Cache ---
    yesterday = (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_check.read_persistent_cache.return_value = json.dumps({ip_local_skip: yesterday})

    # --- Setup 3: Mock DD Search for Remote Check ---
    def mock_dd_search(*args, **kwargs):
        payload = kwargs.get('json')
        if f'@attributes.scamalytics.ip:{ip_remote_skip}' in payload.get('filter', {}).get('query', ''):
            # Simulate finding an existing Scamalytics log for the remote IP
            return MagicMock(
                status_code=200,
                json=lambda: {"data": [{"type": "log"}]}, # Found
                raise_for_status=lambda: None,
            )
        # Handle the initial log fetch request
        return mock_dd_post.return_value

    mock_dd_post.side_effect = mock_dd_search

    # --- Setup 4: Mock Scamalytics API Success ---
    mock_scam_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"scamalytics": {"ip": ip_to_process, "score": 90}},
        raise_for_status=lambda: None,
    )

    # 5. Act: Run the records generator
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")
    records = list(stream.records())

    # 6. Assert: Only one record (ip_to_process) should be yielded
    assert len(records) == 1
    
    # Assert logs for skips
    mock_check.log.info.assert_any_call(
        "SCAMALYTICS: SKIP %s (persistent cache <%sh)", ip_local_skip, 24
    )
    mock_check.log.info.assert_any_call(
        "SCAMALYTICS: SKIP %s (remote logs <%sh)", ip_remote_skip, 24
    )
    mock_check.log.debug.assert_any_call(
        "SCAMALYTICS: SKIP %s (session cache <%sh)", ip_session_skip, 24
    )
    
@pytest.mark.unit
@patch('datadog_checks.scamalytics.check.requests.post')
@patch('datadog_checks.scamalytics.check.requests.get')
def test_records_scamalytics_api_failure(mock_scam_get, mock_dd_post, mock_check):
    """
    Test the exception handling when the Scamalytics API call fails (HTTP error, timeout, etc.).
    (Covers lines 189-191 in check.py)
    """
    test_ip = "9.9.9.9"

    # --- Setup 1: Mock Datadog Log Fetch (Input Logs) ---
    mock_dd_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": [
                {"attributes": {"timestamp": "2025-10-15T10:00:00Z", "message": f"Log with IP {test_ip}"}, "type": "log"}
            ]
        },
        raise_for_status=lambda: None,
    )

    # --- Setup 2: Mock Scamalytics API Failure ---
    mock_scam_get.side_effect = requests.exceptions.HTTPError("Scamalytics 500 Server Error")

    # 3. Act: Run the records generator
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")
    records = list(stream.records())

    # 4. Assert: No records should be yielded, and error should be logged.
    assert len(records) == 0
    mock_check.log.error.assert_called_with(
        "SCAMALYTICS: Scamalytics API error for %s: %s", test_ip, mock_scam_get.side_effect
    )


@pytest.mark.unit
def test_load_save_cache_error_handling(mock_check):
    """
    Test error paths in cache loading and saving functions.
    (Covers lines 236-237 and 247-248 in check.py)
    """
    
    # --- Test _load_recent_cache error handling (load cache on init) ---
    mock_check.read_persistent_cache.side_effect = Exception("File read error")
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")
    
    # Assert the cache is empty despite the failure
    assert stream.recent_cache == {}
    mock_check.log.warning.assert_any_call(
        "SCAMALYTICS: failed to load persistent cache: %s", mock_check.read_persistent_cache.side_effect
    )
    
    # --- Test _save_recent_cache error handling ---
    mock_check.write_persistent_cache.side_effect = Exception("File write error")
    # Reset the read side_effect
    mock_check.read_persistent_cache.side_effect = None
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")

    # Call a method that triggers save
    stream._update_local_cache("3.3.3.3")
    
    mock_check.log.warning.assert_any_call(
        "SCAMALYTICS: failed to save persistent cache: %s", mock_check.write_persistent_cache.side_effect
    )


@pytest.mark.unit
def test_processed_recently_local_error_handling(mock_check):
    """
    Test the error path in _processed_recently_local when timestamp parsing fails.
    (Covers lines 267-268 in check.py)
    """
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")
    
    # Insert an unparsable timestamp into the cache
    stream.recent_cache["4.4.4.4"] = "NOT_A_VALID_TIMESTAMP"
    
    # Should return False (fail open) on parse error
    assert stream._processed_recently_local("4.4.4.4") is False

@pytest.mark.unit
@patch('datadog_checks.scamalytics.check.requests.post')
def test_was_recently_processed_remote_error_handling(mock_post, mock_check):
    """
    Test the error path in _was_recently_processed_remote when the remote API call fails.
    (Covers lines 303-304 in check.py)
    """
    test_ip = "123.123.123.123"
    stream = ScamalyticsLogStream(check=mock_check, name="scamalytics_stream")
    
    # Mock the remote check API call to fail
    mock_post.side_effect = requests.exceptions.Timeout("Remote check timeout")
    
    # Should return False (fail open) on error
    result = stream._was_recently_processed_remote(test_ip)
    
    assert result is False
    mock_check.log.warning.assert_called_with(
        "SCAMALYTICS: remote recent-check failed for %s: %s", test_ip, mock_post.side_effect
    )


# =====================================================================
#  INTEGRATION TEST
# =====================================================================


@pytest.mark.integration
def test_scamalytics_api_end_to_end():
    """
    Integration test verifying that Scamalytics crawler streams work end-to-end.
    It runs the ScamalyticsLogStream and ensures records can be produced
    without unhandled exceptions.
    """

    dd_api_key = os.getenv("DD_API_KEY")
    dd_app_key = os.getenv("DD_APP_KEY")
    scam_key = os.getenv("SCAM_API_KEY")
    customer_id = os.getenv("SCAM_CUSTOMER_ID")
    scam_api_url = "https://api-ti-us.scamalytics.com/tiprem/?ip="
    dd_site = os.getenv("DD_SITE", "datadoghq.com")

    if not all([dd_api_key, dd_app_key, scam_key, customer_id]):
        pytest.skip("Integration credentials not set (DD_API_KEY, SCAM_API_KEY, etc.)")

    instance = {
        "dd_api_key": dd_api_key,
        "dd_app_key": dd_app_key,
        "dd_site": dd_site,
        "scamalytics_api_key": scam_key,
        "scamalytics_api_url": scam_api_url,
        "customer_id": customer_id,
    }

    # Initialize the check and get its crawler stream
    check = ScamalyticsCheck("scamalytics", {}, [instance])
    streams = check.get_log_streams()
    assert streams, "No log streams returned by ScamalyticsCheck"

    stream = streams[0]

    try:
        records = list(stream.records())
    except Exception as e:
        pytest.fail(f"Integration crawler raised unexpected error: {e}")

    assert isinstance(records, list)
    assert all(hasattr(r, "data") for r in records)