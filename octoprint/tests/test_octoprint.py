import mock
import pytest

from datadog_checks.octoprint import OctoPrintCheck


@pytest.mark.skip
@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
@mock.patch('datadog_checks.octoprint.OctoPrintCheck.get_rpi_core_temp')
def test_check(mock_rpi_temp, aggregator, mock_api_request, instance):
    mock_rpi_temp.return_value = 49.0

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
@mock.patch('datadog_checks.octoprint.OctoPrintCheck.get_rpi_core_temp')
def test_empty_job(mock_rpi_temp, aggregator, mock_empty_api_request, instance):
    mock_rpi_temp.return_value = 49.0

    check = OctoPrintCheck('octoprint', {}, [instance])
    check.check(instance)

    aggregator.assert_metric("octoprint.rpi_core_temp", 49.0, count=1)
    aggregator.assert_metric("octoprint.printer_state", 0, count=1)
    aggregator.assert_metric("octoprint.current_tool_temp", 25.0, count=1)
    aggregator.assert_metric("octoprint.target_tool_temp", 200.0, count=1)
    aggregator.assert_metric("octoprint.current_bed_temp", 24.77, count=1)
    aggregator.assert_metric("octoprint.target_bed_temp", 70.0, count=1)

    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
@mock.patch('datadog_checks.octoprint.OctoPrintCheck.get_rpi_core_temp')
def test_active_job(mock_rpi_temp, aggregator, mock_active_api_request, instance):
    mock_rpi_temp.return_value = 49.0

    check = OctoPrintCheck('octoprint', {}, [instance])
    check.check(instance)

    aggregator.assert_metric("octoprint.rpi_core_temp", 49.0, count=1)
    aggregator.assert_metric("octoprint.printer_state", 2, count=1)
    aggregator.assert_metric("octoprint.est_print_time", 146, count=1)
    aggregator.assert_metric("octoprint.pct_completed", 0.22, count=1)
    aggregator.assert_metric("octoprint.print_job_time", 4, count=1)
    aggregator.assert_metric("octoprint.print_job_time_left", 15, count=1)
    aggregator.assert_metric("octoprint.current_tool_temp", 25.0, count=1)
    aggregator.assert_metric("octoprint.target_tool_temp", 200.0, count=1)
    aggregator.assert_metric("octoprint.current_bed_temp", 24.77, count=1)
    aggregator.assert_metric("octoprint.target_bed_temp", 70.0, count=1)

    aggregator.assert_all_metrics_covered()


@pytest.mark.e2e
def test_e2e():
    return True
