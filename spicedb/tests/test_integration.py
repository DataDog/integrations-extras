import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.cockroachdb import CockroachdbCheck
from datadog_checks.dev.utils import assert_service_checks, get_metadata_metrics

# NOTE: this is the same as annotating all of the test functions in this file with the dd_environment fixture.
pytestmark = [pytest.mark.usefixtures("dd_environment")]


def test_metrics(aggregator, instance, dd_run_check):
    check = CockroachdbCheck("spicedb", {}, [instance])
    dd_run_check(check)

    expected_metrics = []

    for metric in expected_metrics:
        aggregator.assert_metric(f"spicedb.{metric}", at_least=0)

    aggregator.assert_service_check("spicedb.openmetrics.health", ServiceCheck.OK)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), check_submission_type=True)

    assert_service_checks(aggregator)