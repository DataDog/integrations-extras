import json
import os

import pytest
from mock import patch
from tests.common import HERE

from datadog_checks.base import AgentCheck
from datadog_checks.unifi_console.check import UnifiConsoleCheck
from datadog_checks.unifi_console.errors import APIConnectionError
from datadog_checks.unifi_console.types import ControllerInfo, Count, Gauge, Rate


@pytest.mark.usefixtures("mock_api")
def test_metrics_submission(aggregator, dd_run_check, instance):
    """This test asserts that the same api content always produces the same metrics."""
    check = UnifiConsoleCheck("unifi", {}, [instance])
    dd_run_check(check)

    value_files = ["device_metrics_values.json", "client_metrics_values.json"]

    for file in value_files:
        fixture_file = os.path.join(HERE, "fixtures", file)
        with open(fixture_file, "r") as f:
            data = json.load(f)
            for metric in data:
                aggregator.assert_metric(
                    metric["name"],
                    metric.get("value"),
                    hostname=metric.get("hostname"),
                    tags=metric.get("tags"),
                )
    aggregator.assert_metric('unifi_console.healthy', metric_type=aggregator.GAUGE)
    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures("mock_api")
def test__initiate_api_connection(instance):
    with patch("datadog_checks.unifi_console.check.Unifi.login") as mock_connect:
        check = UnifiConsoleCheck("unifi", {}, [instance])

        mock_connect.side_effect = APIConnectionError()
        with pytest.raises(APIConnectionError):
            check._initiate_api_connection()


@pytest.mark.usefixtures("mock_api")
def test_check_status_fail(aggregator, dd_run_check, instance):
    with patch("datadog_checks.unifi_console.check.Unifi.status") as mock_status:
        check = UnifiConsoleCheck("unifi", {}, [instance])
        mock_status.side_effect = Exception()

        with pytest.raises(Exception):
            dd_run_check(check)

        aggregator.assert_service_check("unifi_console.can_connect", AgentCheck.CRITICAL, tags=check._config.tags)
        aggregator.assert_service_check("unifi_console.healthy", AgentCheck.CRITICAL, tags=check._config.tags)
        aggregator.assert_metric('unifi_console.healthy', 0, metric_type=aggregator.GAUGE)


@pytest.mark.usefixtures("mock_api")
def test_check_status_pass(aggregator, dd_run_check, instance):
    check = UnifiConsoleCheck("unifi", {}, [instance])

    dd_run_check(check)
    aggregator.assert_service_check("unifi_console.can_connect", AgentCheck.OK, tags=check._config.tags)
    aggregator.assert_service_check("unifi_console.healthy", AgentCheck.OK, tags=check._config.tags)
    aggregator.assert_metric('unifi_console.healthy', 1, metric_type=aggregator.GAUGE)


@pytest.mark.usefixtures("mock_api")
def test_get_devices_info_fails(aggregator, dd_run_check, instance):
    with patch("datadog_checks.unifi_console.check.Unifi.get_devices_info") as mock_get_devices_info:
        check = UnifiConsoleCheck("unifi", {}, [instance])
        mock_get_devices_info.side_effect = Exception()

        with pytest.raises(Exception):
            dd_run_check(check)


@pytest.mark.usefixtures("mock_api")
def test_get_clients_info_fails(aggregator, dd_run_check, instance):
    with patch("datadog_checks.unifi_console.check.Unifi.get_clients_info") as mock_get_clients_info:
        check = UnifiConsoleCheck("unifi", {}, [instance])
        mock_get_clients_info.side_effect = Exception()

        with pytest.raises(Exception):
            dd_run_check(check)


@pytest.mark.usefixtures("mock_api")
def test__submit_healthy_metrics(aggregator, instance):

    check = UnifiConsoleCheck("unifi", {}, [instance])

    info = "test"
    check._submit_healthy_metrics(info, check._config.tags)
    aggregator.assert_service_check("unifi_console.healthy", AgentCheck.CRITICAL, tags=check._config.tags)
    aggregator.assert_metric('unifi_console.healthy', 0, metric_type=aggregator.GAUGE)

    with open(os.path.join(HERE, "fixtures", "status_valid.json")) as f:
        check._submit_healthy_metrics(ControllerInfo(json.load(f)), check._config.tags)
    aggregator.assert_service_check("unifi_console.healthy", AgentCheck.OK, tags=check._config.tags)
    aggregator.assert_metric('unifi_console.healthy', 1, metric_type=aggregator.GAUGE)

    aggregator.reset()
    with open(os.path.join(HERE, "fixtures", "status_invalid.json")) as f:
        check._submit_healthy_metrics(ControllerInfo(json.load(f)), check._config.tags)
    aggregator.assert_service_check("unifi_console.healthy", AgentCheck.CRITICAL, tags=check._config.tags)
    aggregator.assert_metric('unifi_console.healthy', 0, metric_type=aggregator.GAUGE)


@pytest.mark.parametrize(
    "metric, expected_type",
    [
        (Gauge('test', 1, []), 0),
        (Count('test', 1, []), 2),
        (Rate('test', 1, []), 1),
    ],
)
@pytest.mark.usefixtures("mock_api")
def test__submit_metrics(aggregator, instance, metric, expected_type):
    check = UnifiConsoleCheck("unifi", {}, [instance])

    metrics = [metric]
    check._submit_metrics(metrics)
    aggregator.assert_metric('unifi_console.test', 1, metric_type=expected_type)
