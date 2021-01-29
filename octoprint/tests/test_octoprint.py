import mock
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.base.stubs.aggregator import AggregatorStub

MOCK_RESPONSE = {
    "rpi_core_temp": 0.0,
    "printer_state": 1,
    "pct_completed": 0,
    "print_job_time": 1,
    "print_job_time_left": 9999999,
    "current_tool_temp": 50.0,
    "target_tool_temp": 190.0,
    "current_bed_temp": 68.0,
    "target_bed_temp": 70
}


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.octoprint.OctoPrintCheck._call_command')
def test_check(mock_cmd, aggregator, instance):
    # type: (mock.MagicMock, AggregatorStub, Dict[str, Any]) -> None
    mock_cmd.return_value = MOCK_RESPONSE

    check = OctoPrintCheck('octoprint', {}, [instance])
    check.check(instance)
    aggregator.assert_metric("octoprint.rpi_core_temp", 0.0, count=1)
    aggregator.assert_metric("octoprint.printer_state", 1, count=1)
    aggregator.assert_metric("octoprint.pct_completed", 0, count=1)
    aggregator.assert_metric("octoprint.print_job_time", 1, count=1)
    aggregator.assert_metric("octoprint.print_job_time_left", 9999999, count=1)
    aggregator.assert_metric("octoprint.current_tool_temp", 50.0, count=1)
    aggregator.assert_metric("octoprint.target_tool_temp", 190.0, count=1)
    aggregator.assert_metric("octoprint.current_bed_temp", 68.0, count=1)
    aggregator.assert_metric("octoprint.target_bed_temp", 70.0, count=1)

    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
@mock.patch('datadog_checks.octoprint.OctoPrintCheck._call_command')
def test_config(mock_cmd, *args, **kwargs):
    mock_cmd.return_value = MOCK_RESPONSE

    # okay to specify nothing
    instance = {}
    check = OctoPrintCheck('octoprint', {}, [instance])
    check.check(instance)


@pytest.mark.e2e
def test_e2e():
    return True
