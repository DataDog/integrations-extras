import os

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.scamalytics.check import ScamalyticsCheck, ScamalyticsLogStream

# =====================================================================
#  UNIT TESTS
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
