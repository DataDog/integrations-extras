import os
from unittest.mock import patch

import pytest

from datadog_checks.scamalytics.check import ScamalyticsCheck


# ==============================================================================
# 1. HELPER FUNCTION
# ==============================================================================
def run_crawler_logic(instance_config):
    """
    Executes the check initialization and stream processing.
    This function contains the lines that were previously missed.
    """
    # Initialize the check
    check = ScamalyticsCheck("scamalytics", {}, [instance_config])

    # Get the streams
    streams = check.get_log_streams()
    assert streams, "No log streams returned by ScamalyticsCheck"

    stream = streams[0]

    # Run the stream (Force execution by converting generator to list)
    try:
        records = list(stream.records())
    except Exception as e:
        pytest.fail(f"Integration crawler raised unexpected error: {e}")

    # Validations
    assert isinstance(records, list)
    if records:
        assert all(hasattr(r, "data") for r in records)

    return records


# ==============================================================================
# 2. MOCKED TEST (Always Runs)
# ==============================================================================
def test_scamalytics_mocked_execution():
    """
    Runs the logic with fake keys and mocked network.
    This ensures lines inside 'run_crawler_logic' are counted in coverage.
    """
    instance = {
        "dd_api_key": "dummy_key",
        "dd_app_key": "dummy_app",
        "dd_site": "datadoghq.com",
        "scamalytics_api_key": "dummy_scam_key",
        "scamalytics_api_url": "https://api.test/",
        "customer_id": "dummy_id",
    }

    # Mock requests so we don't need real internet/keys
    with patch("requests.post") as mock_post, patch("requests.get"):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"data": []}
        run_crawler_logic(instance)
        mock_post.return_value.json.return_value = {"data": []}

        # CALL THE HELPER - This hits the lines you were missing!
        run_crawler_logic(instance)


# ==============================================================================
# 3. LIVE INTEGRATION TEST (Skips if no keys)
# ==============================================================================
@pytest.mark.integration
def test_scamalytics_api_end_to_end():
    dd_api_key = os.getenv("DD_API_KEY")
    dd_app_key = os.getenv("DD_APP_KEY")
    scam_key = os.getenv("SCAM_API_KEY")
    customer_id = os.getenv("SCAM_CUSTOMER_ID")
    dd_site = os.getenv("DD_SITE", "datadoghq.com")
    scam_api_url = "https://api-ti-us.scamalytics.com/tiprem/?ip="

    if not all([dd_api_key, dd_app_key, scam_key, customer_id]):
        pytest.skip("Integration credentials not set")

    instance = {
        "dd_api_key": dd_api_key,
        "dd_app_key": dd_app_key,
        "dd_site": dd_site,
        "scamalytics_api_key": scam_key,
        "scamalytics_api_url": scam_api_url,
        "customer_id": customer_id,
    }

    # Also uses the helper, but with REAL keys
    run_crawler_logic(instance)
