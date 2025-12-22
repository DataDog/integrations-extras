import pytest
import requests
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from datadog_checks.base import ConfigurationError
from datadog_checks.scamalytics import ScamalyticsCheck
from datadog_checks.scamalytics.check import ScamalyticsLogStream, parse_iso8601_timestamp


@pytest.fixture
def instance():
    return {
        "scamalytics_api_key": "test_key",
        "scamalytics_api_url": "https://api.scamalytics.com/",
        "customer_id": "test_cust_id",
        "dd_api_key": "dd_key",
        "dd_app_key": "dd_app",
    }


@pytest.fixture
def check(instance):
    return ScamalyticsCheck("scamalytics", {}, [instance])


@pytest.fixture
def stream(check):
    return ScamalyticsLogStream(check=check, name="scamalytics_stream")


def test_parse_iso8601_timestamp():
    dt = parse_iso8601_timestamp("2025-01-01T12:00:00Z")
    assert dt.year == 2025
    assert dt.tzinfo == timezone.utc

    dt2 = parse_iso8601_timestamp("2025-01-01T12:00:00+00:00")
    assert dt2 == dt

    assert parse_iso8601_timestamp(None) is None


@pytest.mark.parametrize("ip, expected", [
    ("8.8.8.8", True),
    ("1.1.1.1", True),
    ("10.0.0.1", False),
    ("192.168.0.1", False),
    ("172.16.0.1", False),
    ("172.31.255.255", False),
    ("127.0.0.1", False),
    ("169.254.1.1", False),
])
def test_is_public_ip(stream, ip, expected):
    assert stream._is_public_ip(ip) == expected


def test_config_validation_success(instance):
    check = ScamalyticsCheck("scamalytics", {}, [instance])
    assert check.instance["scamalytics_api_key"] == "test_key"


def test_config_validation_failure():
    instance = {"scamalytics_api_key": "missing_others"}
    with pytest.raises(ConfigurationError) as e:
        ScamalyticsCheck("scamalytics", {}, [instance])
    assert "Missing required configuration key" in str(e.value)


def test_records_happy_path_new_ip(stream):
    mock_logs = [
        {
            "attributes": {
                "timestamp": "2025-01-01T10:00:00Z",
                "message": "Connection from 8.8.8.8"
            }
        }
    ]
    mock_scam_data = {"score": 50, "risk": "medium"}

    with patch("requests.post") as mock_dd_post, \
         patch("requests.get") as mock_scam_get:
        
        resp_logs = MagicMock()
        resp_logs.json.return_value = {"data": mock_logs}

        resp_remote_check = MagicMock()
        resp_remote_check.json.return_value = {"data": []}

        mock_dd_post.side_effect = [resp_logs, resp_remote_check]

        mock_scam_resp = MagicMock()
        mock_scam_resp.json.return_value = mock_scam_data
        mock_scam_get.return_value = mock_scam_resp

        records = list(stream.records(cursor={"timestamp": "2025-01-01T09:00:00Z"}))

        assert len(records) == 1
        assert records[0].data["attributes"] == mock_scam_data
        assert records[0].data["message"] == "Scamalytics report for IP 8.8.8.8"
        assert "8.8.8.8" in stream.recent_cache


def test_records_skips_private_ips(stream):
    mock_logs = [
        {
            "attributes": {
                "timestamp": "2025-01-01T10:00:00Z",
                "message": "Connection from 192.168.1.1"
            }
        }
    ]

    with patch("requests.post") as mock_dd_post:
        mock_dd_resp = MagicMock()
        mock_dd_resp.json.return_value = {"data": mock_logs}
        mock_dd_post.return_value = mock_dd_resp

        records = list(stream.records(cursor={"timestamp": "2025-01-01T09:00:00Z"}))

        assert len(records) == 1
        assert records[0].data["attributes"].get("checkpoint") is True
        assert records[0].cursor["timestamp"] == "2025-01-01T10:00:00Z"


def test_records_skips_cached_ips(stream):
    stream.recent_cache["8.8.8.8"] = "2025-01-01T09:55:00Z"
    
    mock_logs = [
        {
            "attributes": {
                "timestamp": "2025-01-01T10:00:00Z",
                "message": "Connection from 8.8.8.8"
            }
        }
    ]

    with patch("requests.post") as mock_dd_post, \
         patch("requests.get") as mock_scam_get:
        
        mock_dd_resp = MagicMock()
        mock_dd_resp.json.return_value = {"data": mock_logs}
        mock_dd_post.return_value = mock_dd_resp

        records = list(stream.records(cursor={"timestamp": "2025-01-01T09:00:00Z"}))

        assert len(records) == 1
        assert records[0].data["attributes"].get("checkpoint") is True
        mock_scam_get.assert_not_called()


def test_records_remote_fallback(stream):
    ip = "1.2.3.4"
    mock_logs = [
        {
            "attributes": {
                "timestamp": "2025-01-01T10:00:00Z",
                "message": f"Connection from {ip}"
            }
        }
    ]

    with patch("requests.post") as mock_post, \
         patch("requests.get") as mock_get:
        
        resp_logs = MagicMock()
        resp_logs.json.return_value = {"data": mock_logs}

        resp_fallback = MagicMock()
        resp_fallback.json.return_value = {"data": [{"id": "found_prev_log"}]}

        mock_post.side_effect = [resp_logs, resp_fallback]

        records = list(stream.records(cursor={"timestamp": "2025-01-01T09:00:00Z"}))

        assert len(records) == 1
        assert records[0].data["attributes"].get("checkpoint") is True
        
        mock_get.assert_not_called()
        assert ip in stream.recent_cache


def test_dd_api_error_handling(stream):
    with patch("requests.post") as mock_post:
        mock_post.side_effect = Exception("API Down")
        records = list(stream.records(cursor=None))
        assert len(records) == 0


def test_prune_expired_cache(stream):
    now = datetime.now(timezone.utc)
    old_ts = (now - timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%SZ")
    fresh_ts = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    stream.recent_cache["old_ip"] = old_ts
    stream.recent_cache["fresh_ip"] = fresh_ts

    stream._prune_expired_cache()

    assert "old_ip" not in stream.recent_cache
    assert "fresh_ip" in stream.recent_cache


def test_load_persistent_cache_corrupt(check, stream):
    check.read_persistent_cache = MagicMock(return_value="{bad_json")
    stream._load_recent_cache()
    assert stream.recent_cache == {}


def test_cursor_handling_with_overlap(stream):
    cursor = {"timestamp": "2025-01-01T10:00:00Z"}
    
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"data": []}
        mock_post.return_value = mock_resp
        
        list(stream.records(cursor=cursor))
        
        _, kwargs = mock_post.call_args
        payload = kwargs['json']
        filter_from = payload['filter']['from']
        
        assert "09:59:58" in filter_from


def test_handling_http_status_errors(stream):
    with patch("requests.post") as mock_post:
        resp = MagicMock()
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Forbidden")
        mock_post.return_value = resp
        
        records = list(stream.records(cursor=None))
        assert len(records) == 0


def test_malformed_timestamp_in_log(stream):
    mock_logs = [
        {
            "attributes": {
                "message": "Bad log"
            }
        }
    ]
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"data": mock_logs}
        mock_post.return_value = mock_resp

        records = list(stream.records(cursor={"timestamp": "2025-01-01T09:00:00Z"}))
        assert len(records) == 0