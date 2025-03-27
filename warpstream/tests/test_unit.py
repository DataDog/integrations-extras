# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.warpstream import WarpstreamCheck

from . import common


@pytest.mark.parametrize(
    'status_code, expected_healthy_status, expected_healthy_value',
    [
        (200, AgentCheck.OK, 1),
        (500, AgentCheck.WARNING, 1),
    ],
)
def test_check(dd_run_check, aggregator, status_code, expected_healthy_status, expected_healthy_value):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    instance = common.FULL_CONFIG['instances'][0]
    check = WarpstreamCheck('warpstream', {}, [instance])

    with mock.patch('datadog_checks.base.utils.http.requests') as req:
        print(status_code)
        mock_resp = mock.MagicMock(status_code=status_code)
        req.get.return_value = mock_resp

        check.check(None)

    aggregator.assert_service_check('warpstream.can_connect', expected_healthy_status, count=1)
    aggregator.assert_metric('warpstream.can_connect', expected_healthy_value, count=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
