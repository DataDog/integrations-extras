# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import mock
import pytest

from typing import Any, Callable, Dict  # noqa: F401

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.warpstream import WarpstreamCheck

from . import common

@pytest.mark.parametrize(
    'json_resp, expected_healthy_status, expected_healthy_value',
    [
        ({'status': 'OK'}, AgentCheck.OK, 1),
        #({'status': 'KO'}, AgentCheck.CRITICAL, 0),
        #({}, AgentCheck.CRITICAL, 0),
    ],
)
def test_check(dd_run_check, aggregator, json_resp, expected_healthy_status, expected_healthy_value):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    instance = common.FULL_CONFIG['instances'][0]
    check = WarpstreamCheck('warpstream', {}, [instance])

    with mock.patch('datadog_checks.base.utils.http.requests') as req:
        mock_resp = mock.MagicMock(status_code=200)
        mock_resp.json.side_effect = [json_resp]
        req.get.return_value = mock_resp

        check.check(None)

    aggregator.assert_service_check('warpstream.can_connect', expected_healthy_status,  count=1)
    aggregator.assert_metric('warpstream.can_connect', expected_healthy_value, count=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
