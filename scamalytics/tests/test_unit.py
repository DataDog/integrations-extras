from typing import Any, Callable, Dict  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.scamalytics import ScamalyticsCheck
import pytest


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def instance() -> Dict[str, Any]:
    """
    Returns a valid minimal configuration for the ScamalyticsCheck.
    """
    return {
        'scamalytics_api_key': 'x',
        'scamalytics_api_url': 'https://api-ti-us.scamalytics.com/tiprem/?ip=',
        'customer_id': 'x',
        'dd_api_key': 'x',
        'dd_app_key': 'x',
    }


# -------------------------------
# Tests
# -------------------------------
def test_check(dd_run_check, aggregator, instance):
    """
    Test the ScamalyticsCheck with the provided instance.
    """
    check = ScamalyticsCheck('scamalytics', {}, [instance])
    dd_run_check(check)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
