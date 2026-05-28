from typing import Any, Callable, Dict  # noqa: F401
from unittest.mock import MagicMock, patch

import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.huntress import HuntressCheck


@pytest.fixture
def huntress_instance():
    return {
        "huntress_api_key": "test_key",
        "huntress_secret_key": "test_secret",
        "log_queries": [{"name": "all-logs", "esql_query": "FROM logs"}],
        "enrich_with_org_tags": False,
    }


def test_check_initializes(huntress_instance):
    check = HuntressCheck('huntress', {}, [huntress_instance])
    assert check is not None
    assert check.SERVICE_CHECK_NAME == 'huntress.siem.check_status'


def test_check_runs(dd_run_check, aggregator, huntress_instance):
    check = HuntressCheck('huntress', {}, [huntress_instance])
    check.log = MagicMock()

    empty_response = {"logs": [], "pagination": {}}

    with patch.object(
        check,
        "_request_with_retry",
        return_value=MagicMock(
            status_code=200,
            json=lambda: empty_response,
            headers={"x-huntress-api-call-limit": "60", "x-huntress-api-call-remaining": "60"},
        ),
    ):
        dd_run_check(check)
