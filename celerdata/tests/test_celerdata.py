import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.celerdata import CelerdataCheck

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("dd_environment")]


def test_celerdata_be(aggregator, dd_run_check, be_instance):
    check = CelerdataCheck("celerdata", {}, [be_instance])
    dd_run_check(check)

    aggregator.assert_service_check("celerdata.openmetrics.health", ServiceCheck.OK)
    aggregator.assert_metric("celerdata.be.active_scan_context_count", value=0)
