import os

import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.ravendb import RavendbCheck

from .common import METRICS as EXPECTED_PROMETHEUS_METRICS

pytestmark = [pytest.mark.usefixtures("dd_environment"), pytest.mark.e2e]
REQUIRED_ENV = ["RAVEN_License"]


def _missing_env():
    return [k for k in REQUIRED_ENV if not os.getenv(k)]


def test_e2e_ravendb_service_check_ok(dd_run_check, aggregator, check):
    missing = _missing_env()
    if missing:
        pytest.skip(f"E2E disabled (missing env vars: {', '.join(missing)})")
    dd_run_check(check)

    aggregator.assert_service_check('ravendb.openmetrics.health', ServiceCheck.OK)


def test_e2e_ravendb_service_check_critical_on_connection_error(dd_run_check, aggregator):
    missing = _missing_env()
    if missing:
        pytest.skip(f"E2E disabled (missing env vars: {', '.join(missing)})")
    bad_check = RavendbCheck(
        'ravendb', {}, [{'prometheus_url': 'http://invalid-host:8080/admin/monitoring/v1/prometheus'}]
    )

    with pytest.raises(Exception):
        dd_run_check(bad_check)

    all_service_checks = aggregator._service_checks

    assert len(all_service_checks) == 0, f"Expected no service checks, but got: {all_service_checks}"


def test_e2e_ravendb_check_e2e_assert_metrics(dd_run_check, aggregator, check):
    missing = _missing_env()
    if missing:
        pytest.skip(f"E2E disabled (missing env vars: {', '.join(missing)})")
    dd_run_check(check)
    for metric_name in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric_name, at_least=0)

    aggregator.assert_all_metrics_covered()
