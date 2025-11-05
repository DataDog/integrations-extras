import os

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.scamalytics import ScamalyticsCheck

# =====================================================================
#  UNIT TESTS
# =====================================================================


@pytest.mark.unit
def test_config_validation():
    """
    Validate configuration handling for the ScamalyticsCheck.
    Ensures ConfigurationError is raised when required fields are missing.
    """

    with pytest.raises(ConfigurationError):
        ScamalyticsCheck('scamalytics', {}, [{}])

    with pytest.raises(ConfigurationError):
        ScamalyticsCheck('scamalytics', {}, [{'scamalytics_api_key': 'dummy'}])

    valid_instance = {
        'scamalytics_api_key': 'test_key',
        'scamalytics_api_url': 'https://api11.scamalytics.com/tiprem/?ip=',
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
    check = ScamalyticsCheck(
        'scamalytics',
        {},
        [
            {
                'scamalytics_api_key': 'x',
                'scamalytics_api_url': 'https://api11.scamalytics.com/tiprem/?ip=',
                'customer_id': 'x',
                'dd_api_key': 'x',
                'dd_app_key': 'x',
            }
        ],
    )

    assert check._is_public_ip("8.8.8.8")
    assert not check._is_public_ip("192.168.1.5")


# =====================================================================
#  INTEGRATION TEST
# =====================================================================


@pytest.mark.integration
def test_scamalytics_api_end_to_end():
    """
    Real integration test verifying that Scamalytics API and Datadog endpoints
    are reachable and that the check() runs without unhandled exceptions.
    """

    dd_api_key = os.getenv("DD_API_KEY")
    dd_app_key = os.getenv("DD_APP_KEY")
    scam_key = os.getenv("SCAM_API_KEY")
    customer_id = os.getenv("SCAM_CUSTOMER_ID")
    scam_api_url = os.getenv("SCAM_API_URL", "https://api11.scamalytics.com/tiprem/?ip=")
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

    check = ScamalyticsCheck("scamalytics", {}, [instance])

    try:
        check.check(instance)
    except Exception as e:
        pytest.fail(f"Integration check raised unexpected error: {e}")

    assert True, "Scamalytics integration check completed successfully"
