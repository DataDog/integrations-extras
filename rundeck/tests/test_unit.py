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


def test_access_api_valid(unit_check, mock_http_response):
    endpoint = "/metrics/metrics"

    # setup
    mock_response = {"metrics": []}
    mock_http_response(
        json_data=mock_response,
        status_code=200,
    )
    # run
    actual = unit_check.access_api(endpoint)
    # check
    assert actual == mock_response


def test_access_api_invalid(unit_check, mock_http_response):
    endpoint = "/metrics/metrics"

    # setup
    mock_response = {"metrics": []}
    mock_http_response(
        json_data=mock_response,
        status_code=401,
    )
    # run and check
    with pytest.raises(HTTPError):
        unit_check.access_api(endpoint)


def test_access_api_with_pagination_without_params(unit_check, mocker):
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

    mocker.patch.object(unit_check, "access_api", side_effect=mock_access_api)
    # run
    actual = unit_check.access_api_with_pagination(endpoint, response_count_limit)
    # check
    assert len(actual) == 2


def test_access_api_with_pagination_with_params(unit_check, mocker):
    endpoint = "/metrics/metrics"

    # setup
    mock_params = {"before": 123}
    response_count_limit = 20
    mock_response_one = {"paging": {"count": 20, "total": 25}}
    mock_response_two = {"paging": {"count": 5, "total": 25}}

    def mock_access_api(url, params):
        if url == endpoint and params == {**mock_params, "max": response_count_limit, "offset": 0}:
            return mock_response_one
        if url == endpoint and params == {**mock_params, "max": response_count_limit, "offset": 20}:
            return mock_response_two
        raise ValueError(f"Unexpected call with url={url} and params={params}")

    mocker.patch.object(unit_check, "access_api", side_effect=mock_access_api)
    # run
    actual = unit_check.access_api_with_pagination(endpoint, response_count_limit, mock_params)
    # check
    assert len(actual) == 2


def test_send_metrics_endpoint_group(unit_check, mocker):
    mock_submission = mocker.MagicMock()
    patched_rename_metric = mocker.patch.object(unit_check, 'rename_metric', side_effect=lambda x: x)

    group_key = "gauges"
    data_key = "value"
    metric_name_with_val = "rundeck.scheduler.quartz.threadPoolSize"
    metric_name_without_val = "rundeck.services.execution_service.execution_job"
    raw_metrics = {group_key: {metric_name_with_val: {data_key: 0}, metric_name_without_val: {data_key: None}}}

    unit_check.send_metrics_endpoint_group(raw_metrics, group_key, data_key, mock_submission)

    assert patched_rename_metric.call_count == 1
    patched_rename_metric.assert_called_once_with(metric_name_with_val)

    assert mock_submission.call_count == 1
    mock_submission.assert_any_call(f"{METRICS_METRICS_METRIC_NAME_PREFIX}.{metric_name_with_val}", 0, tags=[])


@pytest.mark.parametrize(
    "mock_input,output",
    [
        pytest.param(f"{RundeckCheck.__NAMESPACE__}.abc", "abc", id="with prefix removal"),
        pytest.param("abc", "abc", id="without prefix removal"),
        pytest.param(
            "rundeck.services.AuthorizationService.systemAuthorization",
            "services.authorization_service.system_authorization",
            id="multiple parts removal",
        ),
    ],
)
def test_rename_metric(unit_check, mock_input, output):
    assert unit_check.rename_metric(mock_input) == output


@pytest.mark.parametrize(
    "mock_input,output",
    [
        pytest.param("", "", id="empty part"),
        pytest.param("a", "a", id="single char part, never convert"),
        pytest.param("A", "a", id="single char part, must convert"),
        pytest.param("ExecutionService", "execution_service", id="multiple char part"),
    ],
)
def test_convert_case(unit_check, mock_input, output):
    assert unit_check.convert_case(mock_input) == output


def test_check_system_info_endpoint(unit_check, mocker):
    unit_check.set_system_base_tags = mocker.MagicMock()
    unit_check.send_system_info = mocker.MagicMock()

    # invalid api response
    payload = {}
    mocker.patch.object(unit_check, "access_api", return_value=payload)
    unit_check.check_system_info_endpoint()
    unit_check.set_system_base_tags.assert_not_called()
    unit_check.send_system_info.assert_not_called()

    # reset
    unit_check.set_system_base_tags.reset_mock()
    unit_check.send_system_info.reset_mock()

    # valid response
    payload = {"system": {}}
    mocker.patch.object(unit_check, "access_api", return_value=payload)
    unit_check.check_system_info_endpoint()
    assert unit_check.set_system_base_tags.call_count == 1
    assert unit_check.send_system_info.call_count == 1


def test_set_system_base_tags(unit_check):
    # with and without value
    system_data = {"executions": {"active": True}, "rundeck": {}}
    unit_check.set_system_base_tags(system_data)
    assert len(unit_check.system_base_tags) == 1
    assert f"{SYSTEM_TAG_KEY_PREFIX}_executions_active:True" in unit_check.system_base_tags

    # ensure reset with empty api response
    empty_system_data = {}
    unit_check.set_system_base_tags(empty_system_data)
    assert len(unit_check.system_base_tags) == 0


def test_send_system_info(unit_check, mocker):
    unit_check.gauge = mocker.MagicMock()

    # without stats data
    unit_check.send_system_info({})
    unit_check.gauge.assert_not_called()

    # with stats data, some empty
    system_data = {"stats": {"cpu": {"loadAverage": {"average": 0, "unit": "percent"}}, "memory": {"free": None}}}
    unit_check.send_system_info(system_data)
    assert unit_check.gauge.call_count == 1
    unit_check.gauge.assert_any_call(f"{SYSTEM_METRIC_NAME_PREFIX}.cpu.load_average.average", 0, [])


def test_check_project_executions_running(unit_check, mocker):
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

    mocker.patch.object(unit_check, "access_api_with_pagination", side_effect=mock_access_api_with_pagination)

    unit_check.send_execution_status = mocker.MagicMock()

    # run
    unit_check.check_project_executions_running(project_name)

    # check
    assert unit_check.access_api_with_pagination.call_count == 1
    unit_check.access_api_with_pagination.assert_called_with(api_endpoint)

    assert unit_check.send_execution_status.call_count == 2
    unit_check.send_execution_status.assert_any_call(execution_one)
    unit_check.send_execution_status.assert_any_call(execution_two)


@pytest.mark.parametrize(
    "execution,expected_len,expected_value",
    [
        pytest.param({"customStatus": None}, 0, None, id="tag_value is None"),
        pytest.param({"successfulNodes": []}, 0, None, id="tag_value is empty list"),
        pytest.param(
            {"customStatus": "status"},
            1,
            EXEC_TAG_TEMPLATE.format(key="custom_status", value="status"),
            id="tag_value is string",
        ),
        pytest.param(
            {"successfulNodes": ["abc"]},
            1,
            EXEC_TAG_TEMPLATE.format(key="successful_nodes", value="abc"),
            id="tag_value is list of 1 string",
        ),
    ],
)
def test_get_completed_execution_tags_param(unit_check, execution, expected_len, expected_value):
    actual = unit_check.get_completed_execution_tags(execution)
    assert len(actual) == expected_len

    if expected_len > 0:
        assert actual[0] == expected_value


def test_send_execution_status_running_exec(unit_check, mocker):
    # setup
    system_tags = ["system_executions_active:true"]
    unit_check.system_base_tags = system_tags
    unit_check.gauge = mocker.MagicMock()
    unit_check.get_completed_execution_tags = mocker.MagicMock()
    unit_check.send_execution_duration = mocker.MagicMock()
    execution = {"id": 1000, "status": EXEC_STATUS_RUNNING, "user": None, "job_group": ""}

    # run
    unit_check.send_execution_status(execution)

    # check
    expected_tags = [f"{EXEC_TAG_KEY_PREFIX}_id:1000", f"{EXEC_TAG_KEY_PREFIX}_status:running"] + system_tags
    assert unit_check.get_completed_execution_tags.call_count == 0
    assert unit_check.gauge.call_count == 1
    unit_check.gauge.assert_called_with(EXEC_STATUS_METRIC_NAME, 1, tags=expected_tags)

    assert unit_check.send_execution_duration.call_count == 1
    unit_check.send_execution_duration.assert_called_with(execution, expected_tags)


def test_send_execution_status_completed_exec(unit_check, mocker):
    # setup
    system_tags = ["system_executions_active:true"]
    unit_check.system_base_tags = system_tags
    unit_check.gauge = mocker.MagicMock()
    unit_check.get_completed_execution_tags = mocker.MagicMock()
    unit_check.send_execution_duration = mocker.MagicMock()
    execution = {"status": "failed"}

    exec_completed_tag = f"{EXEC_TAG_KEY_PREFIX}_custom_status:my-status"
    unit_check.get_completed_execution_tags.return_value = [exec_completed_tag]

    # run
    unit_check.send_execution_status(execution)

    # check
    expected_tags = [f"{EXEC_TAG_KEY_PREFIX}_status:failed", exec_completed_tag] + system_tags
    assert unit_check.get_completed_execution_tags.call_count == 1
    unit_check.get_completed_execution_tags.assert_called_with(execution)

    assert unit_check.gauge.call_count == 1
    unit_check.gauge.assert_called_with(EXEC_STATUS_METRIC_NAME, 1, tags=expected_tags)

    assert unit_check.send_execution_duration.call_count == 1
    unit_check.send_execution_duration.assert_called_with(execution, expected_tags)


@pytest.mark.parametrize(
    "execution",
    [
        pytest.param({}, id="missing start ms"),
        pytest.param({"status": "succeeded", "date-started": {"unixtime": 1_700_000_000_000}}, id="missing end ms"),
    ],
)
def test_send_execution_duration_never_send(unit_check, mocker, execution):
    # setup
    unit_check.gauge = mocker.MagicMock()

    # run
    unit_check.send_execution_duration(execution, [])

    # check
    assert unit_check.gauge.call_count == 0


def test_send_execution_duration_running_exec(unit_check, mocker):
    # setup
    frozen_time = 1_700_000_000.0
    duration = 10000
    started_ms = int(frozen_time * 1000) - duration
    execution = {
        "status": EXEC_STATUS_RUNNING,
        "date-started": {"unixtime": started_ms},
    }
    mocker.patch("time.time", return_value=frozen_time)
    unit_check.gauge = mocker.MagicMock()

    # run
    unit_check.send_execution_duration(execution, [])

    # check
    assert unit_check.gauge.call_count == 1
    unit_check.gauge.assert_called_with(EXEC_RUNNING_DURATION_METRIC_NAME, duration, tags=[])


def test_send_execution_duration_completed_exec(unit_check, mocker):
    # setup
    started_ms = 1_700_000_000_000
    ended_ms = 2_000_000_000_000
    execution = {
        "status": "succeeded",
        "date-started": {"unixtime": started_ms},
        "date-ended": {"unixtime": ended_ms},
    }
    unit_check.gauge = mocker.MagicMock()

    # run
    unit_check.send_execution_duration(execution, [])

    # check
    assert unit_check.gauge.call_count == 1
    unit_check.gauge.assert_called_with(EXEC_COMPLETED_DURATION_METRIC_NAME, ended_ms - started_ms, tags=[])


def test_check_project_executions_completed(unit_check, mocker):
    # setup
    project_name = "test-project"
    unit_check.projects = [{"name": project_name}, {"label": "missing name"}]
    api_endpoint = f"/project/{project_name}/executions"
    api_params = {"begin": 0, "end": 0}

    unit_check.send_execution_status = mocker.MagicMock()

    def mock_access_api_with_pagination(endpoint, limit=20, query_params=None):
        if endpoint == api_endpoint and query_params == api_params:
            return [{"executions": [{}]}]
        raise ValueError(f"Unexpected call with url={endpoint}, params={query_params}")

    mocker.patch.object(unit_check, "access_api_with_pagination", side_effect=mock_access_api_with_pagination)

    # run
    unit_check.check_project_executions_completed(0, 0, project_name)

    # check
    assert unit_check.access_api_with_pagination.call_count == 1
    unit_check.access_api_with_pagination.assert_called_with(api_endpoint, query_params=api_params)
    assert unit_check.send_execution_status.call_count == 1


@pytest.mark.parametrize(
    "projects",
    [pytest.param([], id="no projects"), pytest.param([{"id": "missing name key"}], id="name missing from project")],
)
def test_check_project_executions_cannot_call(unit_check, mocker, projects):
    # setup
    unit_check.projects = projects
    unit_check.check_project_executions_running = mocker.MagicMock()
    unit_check.check_project_executions_completed = mocker.MagicMock()

    # run
    unit_check.check_project_executions(0, 0)

    # check
    assert unit_check.check_project_executions_running.call_count == 0
    assert unit_check.check_project_executions_completed.call_count == 0


@pytest.mark.parametrize(
    "begin,end,completed_call_count",
    [pytest.param(None, 0, 0, id="begin is None"), pytest.param(0, 2, 1, id="begin is not None")],
)
def test_check_project_executions_can_call(unit_check, mocker, begin, end, completed_call_count):
    # setup
    project_name = "my-project"
    unit_check.projects = [{"name": project_name}]
    unit_check.check_project_executions_running = mocker.MagicMock()
    unit_check.check_project_executions_completed = mocker.MagicMock()

    # run
    unit_check.check_project_executions(begin, end)

    # check
    assert unit_check.check_project_executions_running.call_count == 1
    unit_check.check_project_executions_running.assert_called_with(project_name)

    assert unit_check.check_project_executions_completed.call_count == completed_call_count
    if completed_call_count > 0:
        unit_check.check_project_executions_completed.assert_called_with(begin, end, project_name)


@pytest.mark.parametrize(
    "cache_value,expected_begin,expected_end",
    [
        pytest.param("", None, 2, id="empty cache"),
        pytest.param("1", 1, 2, id="cache with value"),
    ],
)
def test_check_timestamp_cache(unit_check, mocker, cache_value, expected_begin, expected_end):
    # setup
    unit_check.read_persistent_cache = mocker.MagicMock()
    unit_check.read_persistent_cache.return_value = cache_value

    mocker.patch("time.time_ns", return_value=2_000_000)

    unit_check.check_project_endpoint = mocker.MagicMock()
    unit_check.check_system_info_endpoint = mocker.MagicMock()
    unit_check.check_metrics_endpoint = mocker.MagicMock()
    unit_check.check_project_executions = mocker.MagicMock()
    unit_check.write_persistent_cache = mocker.MagicMock()

    # run
    unit_check.check(None)

    # check
    assert unit_check.check_project_endpoint.call_count == 1
    assert unit_check.check_system_info_endpoint.call_count == 1
    assert unit_check.check_metrics_endpoint.call_count == 1

    assert unit_check.check_project_executions.call_count == 1
    unit_check.check_project_executions.assert_called_with(expected_begin, expected_end)

    assert unit_check.write_persistent_cache.call_count == 1
    unit_check.write_persistent_cache.assert_called_with(CACHE_KEY_TIMESTAMP, "2")
