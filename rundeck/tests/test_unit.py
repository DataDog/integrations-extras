import pytest
from requests.exceptions import HTTPError

from datadog_checks.rundeck import RundeckCheck
from datadog_checks.rundeck.constants import (
    CACHE_KEY_TIMESTAMP,
    EXEC_COMPLETED_DURATION_METRIC_NAME,
    EXEC_RUNNING_DURATION_METRIC_NAME,
    EXEC_STATUS_METRIC_NAME,
    EXEC_STATUS_RUNNING,
    EXEC_TAG_KEY_PREFIX,
    EXEC_TAG_TEMPLATE,
    METRICS_METRICS_METRIC_NAME_PREFIX,
    SYSTEM_METRIC_NAME_PREFIX,
    SYSTEM_TAG_KEY_PREFIX,
)


def test_access_api_valid(instance, mock_http_response):
    check = RundeckCheck("rundeck", {}, [instance])
    endpoint = "/metrics/metrics"

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
    endpoint = "/metrics/metrics"

    # setup
    mock_response = {"metrics": []}
    mock_http_response(
        json_data=mock_response,
        status_code=401,
    )
    # run and check
    with pytest.raises(HTTPError):
        check.access_api(endpoint)


def test_access_api_with_pagination_without_params(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    endpoint = "/metrics/metrics"

    # setup
    response_count_limit = 20
    mock_response_one = {"paging": {"count": 20, "total": 25}}
    mock_response_two = {"paging": {"count": 5, "total": 25}}

    def mock_access_api(url, params):
        if url == endpoint and params == {"max": response_count_limit, "offset": 0}:
            return mock_response_one
        if url == endpoint and params == {"max": response_count_limit, "offset": 20}:
            return mock_response_two
        raise ValueError(f"Unexpected call with url={url} and params={params}")

    mocker.patch.object(check, "access_api", side_effect=mock_access_api)
    # run
    actual = check.access_api_with_pagination(endpoint, response_count_limit)
    # check
    assert len(actual) == 2


def test_access_api_with_pagination_with_params(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])
    endpoint = "/metrics/metrics"

    # setup
    params = {"before": 123}
    response_count_limit = 20
    mock_response_one = {"paging": {"count": 20, "total": 25}}
    mock_response_two = {"paging": {"count": 5, "total": 25}}

    def mock_access_api(url, params):
        if url == endpoint and params == {**params, "max": response_count_limit, "offset": 0}:
            return mock_response_one
        if url == endpoint and params == {**params, "max": response_count_limit, "offset": 20}:
            return mock_response_two
        raise ValueError(f"Unexpected call with url={url} and params={params}")

    mocker.patch.object(check, "access_api", side_effect=mock_access_api)
    # run
    actual = check.access_api_with_pagination(endpoint, response_count_limit, params)
    # check
    assert len(actual) == 2


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


def test_convert_case(instance):
    check = RundeckCheck("rundeck", {}, [instance])

    # empty part
    assert check.convert_case("") == ""

    # single char part
    assert check.convert_case("a") == "a"
    assert check.convert_case("A") == "a"

    # multiple char part
    assert check.convert_case("ExecutionService") == "execution_service"


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


def test_check_project_executions_running(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    project_name = "test-project"
    api_endpoint = f"/project/{project_name}/executions/running"
    api_params = None

    execution_one = {"id": 1000}
    execution_two = {"id": 1001}
    payload = [{"executions": [execution_one]}, {"executions": [execution_two]}]

    def mock_access_api_with_pagination(endpoint, limit=20, query_params=None):
        if endpoint == api_endpoint and query_params == api_params:
            return payload
        raise ValueError(f"Unexpected call with url={endpoint}, params={query_params}")

    mocker.patch.object(check, "access_api_with_pagination", side_effect=mock_access_api_with_pagination)

    check.send_execution_status = mocker.MagicMock()

    # run
    check.check_project_executions_running(project_name)

    # check
    assert check.access_api_with_pagination.call_count == 1
    check.access_api_with_pagination.assert_called_with(api_endpoint)

    assert check.send_execution_status.call_count == 2
    check.send_execution_status.assert_any_call(execution_one)
    check.send_execution_status.assert_any_call(execution_two)


def test_get_completed_execution_tags(instance):
    check = RundeckCheck("rundeck", {}, [instance])

    # check handle tag_value==None
    execution = {"customStatus": None}
    actual = check.get_completed_execution_tags(execution)
    assert len(actual) == 0

    # check handle tag_value==str
    execution = {"customStatus": "status"}
    actual = check.get_completed_execution_tags(execution)
    assert len(actual) == 1
    assert actual[0] == EXEC_TAG_TEMPLATE.format(key="custom_status", value="status")

    # check handle tag_value==empty list
    execution = {"successfulNodes": []}
    actual = check.get_completed_execution_tags(execution)
    assert len(actual) == 0

    # check handle tag_value==not empty list
    execution = {"successfulNodes": ["abc"]}
    actual = check.get_completed_execution_tags(execution)
    assert len(actual) == 1
    assert actual[0] == EXEC_TAG_TEMPLATE.format(key="successful_nodes", value="abc")


def test_send_execution_status_running_exec(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    system_tags = ["system_executions_active:true"]
    check.system_base_tags = system_tags
    check.gauge = mocker.MagicMock()
    check.get_completed_execution_tags = mocker.MagicMock()
    check.send_execution_duration = mocker.MagicMock()
    execution = {"id": 1000, "status": EXEC_STATUS_RUNNING, "user": None, "job_group": ""}

    # run
    check.send_execution_status(execution)

    # check
    expected_tags = [f"{EXEC_TAG_KEY_PREFIX}_id:1000", f"{EXEC_TAG_KEY_PREFIX}_status:running"] + system_tags
    assert check.get_completed_execution_tags.call_count == 0
    assert check.gauge.call_count == 1
    check.gauge.assert_called_with(EXEC_STATUS_METRIC_NAME, 1, tags=expected_tags)

    assert check.send_execution_duration.call_count == 1
    check.send_execution_duration.assert_called_with(execution, expected_tags)


def test_send_execution_status_completed_exec(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    system_tags = ["system_executions_active:true"]
    exec_completed_tag = f"{EXEC_TAG_KEY_PREFIX}_custom_status:my-status"
    check.system_base_tags = system_tags
    check.gauge = mocker.MagicMock()
    check.get_completed_execution_tags = mocker.MagicMock()
    check.get_completed_execution_tags.return_value = [exec_completed_tag]
    check.send_execution_duration = mocker.MagicMock()
    execution = {"status": "failed"}

    # run
    check.send_execution_status(execution)

    # check
    assert check.get_completed_execution_tags.call_count == 1
    check.get_completed_execution_tags.assert_called_with(execution)

    expected_tags = [f"{EXEC_TAG_KEY_PREFIX}_status:failed", exec_completed_tag] + system_tags
    assert check.gauge.call_count == 1
    check.gauge.assert_called_with(EXEC_STATUS_METRIC_NAME, 1, tags=expected_tags)
    assert check.send_execution_duration.call_count == 1
    check.send_execution_duration.assert_called_with(execution, expected_tags)


def test_send_execution_duration_missing_start_ms(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    check.gauge = mocker.MagicMock()
    execution = {}

    # run
    check.send_execution_duration(execution, [])

    # check
    assert check.gauge.call_count == 0


def test_send_execution_duration_running_exec(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    frozen_time = 1_700_000_000.0
    duration = 10000
    started_ms = int(frozen_time * 1000) - duration
    execution = {
        "status": EXEC_STATUS_RUNNING,
        "date-started": {"unixtime": started_ms},
    }
    mocker.patch("time.time", return_value=frozen_time)
    check.gauge = mocker.MagicMock()

    # run
    check.send_execution_duration(execution, [])

    # check
    assert check.gauge.call_count == 1
    check.gauge.assert_called_with(EXEC_RUNNING_DURATION_METRIC_NAME, duration, tags=[])


def test_send_execution_duration_completed_exec_missing_end_ms(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    started_ms = 1_700_000_000_000
    execution = {"status": "succeeded", "date-started": {"unixtime": started_ms}}
    check.gauge = mocker.MagicMock()

    # run
    check.send_execution_duration(execution, [])

    # check
    assert check.gauge.call_count == 0


def test_send_execution_duration_completed_exec(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    started_ms = 1_700_000_000_000
    ended_ms = 2_000_000_000_000
    execution = {
        "status": "succeeded",
        "date-started": {"unixtime": started_ms},
        "date-ended": {"unixtime": ended_ms},
    }
    check.gauge = mocker.MagicMock()

    # run
    check.send_execution_duration(execution, [])

    # check
    assert check.gauge.call_count == 1
    check.gauge.assert_called_with(EXEC_COMPLETED_DURATION_METRIC_NAME, ended_ms - started_ms, tags=[])


def test_check_project_executions_completed(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    project_name = "test-project"
    check.projects = [{"name": project_name}, {"label": "missing name"}]
    api_endpoint = f"/project/{project_name}/executions"
    api_params = {"begin": 0, "end": 0}

    check.send_execution_status = mocker.MagicMock()

    def mock_access_api_with_pagination(endpoint, limit=20, query_params=None):
        if endpoint == api_endpoint and query_params == api_params:
            return [{"executions": [{}]}]
        raise ValueError(f"Unexpected call with url={endpoint}, params={query_params}")

    mocker.patch.object(check, "access_api_with_pagination", side_effect=mock_access_api_with_pagination)

    # run
    check.check_project_executions_completed(0, 0, project_name)

    # check
    assert check.access_api_with_pagination.call_count == 1
    check.access_api_with_pagination.assert_called_with(api_endpoint, query_params=api_params)
    assert check.send_execution_status.call_count == 1


def test_check_project_executions_no_projects(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    check.projects = []
    check.check_project_executions_running = mocker.MagicMock()
    check.check_project_executions_completed = mocker.MagicMock()

    # run
    check.check_project_executions(0, 0)

    # check
    assert check.check_project_executions_running.call_count == 0
    assert check.check_project_executions_completed.call_count == 0


def test_check_project_executions_project_missing_name(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    check.projects = [{"id": "missing name key"}]
    check.check_project_executions_running = mocker.MagicMock()
    check.check_project_executions_completed = mocker.MagicMock()

    # run
    check.check_project_executions(0, 0)

    # check
    assert check.check_project_executions_running.call_count == 0
    assert check.check_project_executions_completed.call_count == 0


def test_check_project_executions_project_begin_None(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    project_name = "my-project"
    check.projects = [{"name": project_name}]
    check.check_project_executions_running = mocker.MagicMock()
    check.check_project_executions_completed = mocker.MagicMock()

    # run
    check.check_project_executions(None, 0)

    # check
    assert check.check_project_executions_running.call_count == 1
    check.check_project_executions_running.assert_called_with(project_name)

    assert check.check_project_executions_completed.call_count == 0


def test_check_project_executions_project_begin_not_None(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    project_name = "my-project"
    check.projects = [{"name": project_name}]
    check.check_project_executions_running = mocker.MagicMock()
    check.check_project_executions_completed = mocker.MagicMock()

    # run
    begin = 0
    end = 2
    check.check_project_executions(begin, end)

    # check
    assert check.check_project_executions_running.call_count == 1
    check.check_project_executions_running.assert_called_with(project_name)

    assert check.check_project_executions_completed.call_count == 1
    check.check_project_executions_completed.assert_called_with(begin, end, project_name)


def test_check_last_timestamp_empty(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    check.read_persistent_cache = mocker.MagicMock()
    check.read_persistent_cache.return_value = ""

    mocker.patch("time.time_ns", return_value=2_000_000)

    check.check_project_endpoint = mocker.MagicMock()
    check.check_system_info_endpoint = mocker.MagicMock()
    check.check_metrics_endpoint = mocker.MagicMock()
    check.check_project_executions = mocker.MagicMock()
    check.write_persistent_cache = mocker.MagicMock()

    # run
    check.check(None)

    # check
    assert check.check_project_endpoint.call_count == 1
    assert check.check_system_info_endpoint.call_count == 1
    assert check.check_metrics_endpoint.call_count == 1

    assert check.check_project_executions.call_count == 1
    check.check_project_executions.assert_called_with(None, 2)

    assert check.write_persistent_cache.call_count == 1
    check.write_persistent_cache.assert_called_with(CACHE_KEY_TIMESTAMP, "2")


def test_check_last_timestamp_not_empty(instance, mocker):
    check = RundeckCheck("rundeck", {}, [instance])

    # setup
    check.read_persistent_cache = mocker.MagicMock()
    check.read_persistent_cache.return_value = "1"

    mocker.patch("time.time_ns", return_value=2_000_000)

    check.check_project_endpoint = mocker.MagicMock()
    check.check_system_info_endpoint = mocker.MagicMock()
    check.check_metrics_endpoint = mocker.MagicMock()
    check.check_project_executions = mocker.MagicMock()
    check.write_persistent_cache = mocker.MagicMock()

    # run
    check.check(None)

    # check
    assert check.check_project_endpoint.call_count == 1
    assert check.check_system_info_endpoint.call_count == 1
    assert check.check_metrics_endpoint.call_count == 1

    assert check.check_project_executions.call_count == 1
    check.check_project_executions.assert_called_with(1, 2)

    assert check.write_persistent_cache.call_count == 1
    check.write_persistent_cache.assert_called_with(CACHE_KEY_TIMESTAMP, "2")
