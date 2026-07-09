from unittest import mock

import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.external_secrets import ExternalSecretsCheck

from .common import EXPECTED_PROMETHEUS_METRICS, get_fixture_path


@pytest.mark.e2e
def test_e2e_service_check_ok(dd_agent_check, aggregator, instance, mock_prometheus_metrics):
    dd_agent_check(instance)
    aggregator.assert_service_check('external_secrets.openmetrics.health', ServiceCheck.OK)


@pytest.mark.e2e
def test_e2e_assert_metrics(dd_agent_check, aggregator, instance, mock_prometheus_metrics):
    dd_agent_check(instance)

    for metric in EXPECTED_PROMETHEUS_METRICS:
        aggregator.assert_metric(metric, at_least=0)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
