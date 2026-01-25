import pytest

from datadog_checks.rundeck import RundeckCheck
from datadog_checks.rundeck.utils import convert_case, rename_metric


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
def test_rename_metric(mock_input, output):
    assert rename_metric(mock_input, RundeckCheck.__NAMESPACE__) == output


@pytest.mark.parametrize(
    "mock_input,output",
    [
        pytest.param("", "", id="empty part"),
        pytest.param("a", "a", id="single char part, never convert"),
        pytest.param("A", "a", id="single char part, must convert"),
        pytest.param("ExecutionService", "execution_service", id="multiple char part"),
    ],
)
def test_convert_case(mock_input, output):
    assert convert_case(mock_input) == output
