from unittest.mock import call

import pytest
from requests.exceptions import HTTPError

from datadog_checks.rundeck import RundeckCheck
from datadog_checks.rundeck.constants import (
    EXECUTION_TAG_KEY_PREFIX,
    EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX,
    EXECUTIONS_RUNNING_METRIC_NAME_PREFIX,
    METRICS_METRICS_METRIC_NAME_PREFIX,
    SYSTEM_METRIC_NAME_PREFIX,
    SYSTEM_TAG_KEY_PREFIX,
)


def test_access_api_valid(instance, mock_http_response):
    check = RundeckCheck("rundeck", {}, [instance])
    endpoint = "/api/30/metrics/metrics"

    # setup
    mock_response = {"metrics": []}
    mock_http_response(
        json_data=mock_response,
        status_code=200,
    )
    # run
    actual = check.access_api(endpoint)
    # check
    assert actual == mock_response


def test_access_api_invalid(instance, mock_http_response):
    check = RundeckCheck("rundeck", {}, [instance])
    endpoint = "/api/30/metrics/metrics"

    # setup
    mock_response = {"metrics": []}
    mock_http_response(
        json_data=mock_response,
        status_code=401,
    )
    # run and check
    with pytest.raises(HTTPError):
        check.access_api(endpoint)


def test_access_api_with_pagination(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    endpoint = "/api/30/metrics/metrics"

    # setup
    response_count_limit = 20
    mock_response_one = {"paging": {"count": 20, "total": 25}}
    mock_response_two = {"paging": {"count": 5, "total": 25}}
    mock_responses = {
        f"{endpoint}?max=20&offset=0": mock_response_one,
        f"{endpoint}?max=20&offset={response_count_limit}": mock_response_two,
    }
    mocker.patch.object(check, "access_api", side_effect=lambda url: mock_responses[url])
    # run
    actual = check.access_api_with_pagination(endpoint, response_count_limit)
    # check
    assert len(actual) == 2


def test_check_system_info_endpoint(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    check.set_system_base_tags = mocker.MagicMock()
    check.send_system_info = mocker.MagicMock()

    # invalid api response
    payload = {}
    mocker.patch.object(check, "access_api", return_value=payload)
    check.check_system_info_endpoint()
    check.set_system_base_tags.assert_not_called()
    check.send_system_info.assert_not_called()

    # reset
    check.set_system_base_tags.reset_mock()
    check.send_system_info.reset_mock()

    # valid response
    payload = {"system": {}}
    mocker.patch.object(check, "access_api", return_value=payload)
    check.check_system_info_endpoint()
    assert check.set_system_base_tags.call_count == 1
    assert check.send_system_info.call_count == 1


def test_set_system_base_tags(instance):
    check = RundeckCheck("rundeck", {}, [instance])

    # with and without value
    system_data = {"executions": {"active": True}, "rundeck": {}}
    check.set_system_base_tags(system_data)
    assert len(check.system_base_tags) == 1
    assert f"{SYSTEM_TAG_KEY_PREFIX}_executions_active:True" in check.system_base_tags

    # ensure reset with empty api response
    empty_system_data = {}
    check.set_system_base_tags(empty_system_data)
    assert len(check.system_base_tags) == 0


def test_send_system_info(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    check.gauge = mocker.MagicMock()

    # without stats data
    check.send_system_info({})
    check.gauge.assert_not_called()

    # with stats data, some empty
    system_data = {"stats": {"cpu": {"loadAverage": {"average": 0, "unit": "percent"}}, "memory": {"free": None}}}
    check.send_system_info(system_data)
    assert check.gauge.call_count == 1
    check.gauge.assert_any_call(f"{SYSTEM_METRIC_NAME_PREFIX}.cpu.load_average.average", 0, [])


def test_convert_case(instance):
    check = RundeckCheck("rundeck", {}, [instance])

    # empty part
    assert check.convert_case("") == ""

    # single char part
    assert check.convert_case("a") == "a"
    assert check.convert_case("A") == "a"

    # multiple char part
    assert check.convert_case("ExecutionService") == "execution_service"


def test_rename_metric(instance):
    check = RundeckCheck("rundeck", {}, [instance])

    # with/without prefix removal
    expected = "abc"
    assert check.rename_metric(f"{RundeckCheck.__NAMESPACE__}.{expected}") == expected
    assert check.rename_metric(expected) == expected

    # multiple parts
    assert (
        check.rename_metric("rundeck.services.AuthorizationService.systemAuthorization")
        == "services.authorization_service.system_authorization"
    )


def test_send_metrics_endpoint_group(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    mock_submission = mocker.MagicMock()
    patched_rename_metric = mocker.patch.object(check, 'rename_metric', side_effect=lambda x: x)

    group_key = "gauges"
    data_key = "value"
    metric_name_with_val = "rundeck.scheduler.quartz.threadPoolSize"
    metric_name_without_val = "rundeck.services.execution_service.execution_job"
    raw_metrics = {group_key: {metric_name_with_val: {data_key: 0}, metric_name_without_val: {data_key: None}}}

    check.send_metrics_endpoint_group(raw_metrics, group_key, data_key, mock_submission)

    assert patched_rename_metric.call_count == 1
    patched_rename_metric.assert_called_once_with(metric_name_with_val)

    assert mock_submission.call_count == 1
    mock_submission.assert_any_call(f"{METRICS_METRICS_METRIC_NAME_PREFIX}.{metric_name_with_val}", 0, tags=[])


def test_check_project_executions_running(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    check.send_running_execution = mocker.MagicMock()
    execution_one = {"id": 1000}
    execution_two = {"id": 1001}
    payload = [{"executions": [execution_one]}, {"executions": [execution_two]}]
    mocker.patch.object(check, "access_api_with_pagination", return_value=payload)

    # run
    check.check_project_executions_running()

    # check
    assert check.send_running_execution.call_count == 2
    check.send_running_execution.assert_any_call(execution_one)
    check.send_running_execution.assert_any_call(execution_two)


def test_send_running_execution(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    system_tags = ["system_executions_active:true"]
    check.system_base_tags = system_tags
    check.gauge = mocker.MagicMock()
    execution = {"id": 1000, "status": None}
    # run
    check.send_running_execution(execution)
    # check
    expected_tags = [f"{EXECUTION_TAG_KEY_PREFIX}_id:1000"] + system_tags
    assert check.gauge.call_count == 1
    check.gauge.assert_called_with(EXECUTIONS_RUNNING_METRIC_NAME_PREFIX, 1, tags=expected_tags)


def test_send_running_execution_with_duration(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    system_tags = ["system_executions_active:true"]
    check.system_base_tags = system_tags

    # setup
    check.gauge = mocker.MagicMock()
    frozen_time = 1700000000.0
    started_ms = int(frozen_time * 1000) - 10000
    mocker.patch("time.time", return_value=frozen_time)
    execution = {"id": 1001, "date-started": {"unixtime": started_ms}}
    # run
    check.send_running_execution(execution)
    # check
    expected_tags = [f"{EXECUTION_TAG_KEY_PREFIX}_id:1001"] + system_tags
    expected_sequence = [
        call(EXECUTIONS_RUNNING_METRIC_NAME_PREFIX, 1, tags=expected_tags),
        call(EXECUTIONS_RUNNING_DURATION_METRIC_NAME_PREFIX, 10000, tags=expected_tags),
    ]
    assert check.gauge.call_count == 2
    check.gauge.assert_has_calls(expected_sequence, any_order=False)
