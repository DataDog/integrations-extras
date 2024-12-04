import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.spicedb import SpicedbCheck
from datadog_checks.dev.utils import assert_service_checks, get_metadata_metrics

from .util import get_expected_non_histogram_metrics, get_expected_histogram_metrics

# NOTE: this is the same as annotating all of the test functions in this file with the dd_environment fixture.
pytestmark = [pytest.mark.usefixtures("dd_environment")]


def test_metrics(aggregator, instance, dd_run_check):
    check = SpicedbCheck("spicedb", {}, [instance])
    dd_run_check(check)

    for metric in get_expected_non_histogram_metrics():
        aggregator.assert_metric(f"spicedb.{metric}", at_least=0)

    for metric in get_expected_histogram_metrics():
        aggregator.assert_metric(f"spicedb.{metric}", at_least=0)

    aggregator.assert_service_check("spicedb.openmetrics.health", ServiceCheck.OK)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)

    assert_service_checks(aggregator)
