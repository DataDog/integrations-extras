import os

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.scamalytics.check import ScamalyticsCheck, ScamalyticsLogStream

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
