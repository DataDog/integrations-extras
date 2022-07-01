# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any

import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.base.stubs.aggregator import AggregatorStub

from .common import CHECK_CONFIG
from .metrics import METRICS


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    # type: (Any) -> None
    aggregator = dd_agent_check(CHECK_CONFIG, rate=True)  # type: AggregatorStub

    for metric in METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()

    for instance in CHECK_CONFIG['instances']:
        tags = [
            'instance:trino-{}-{}'.format(instance['host'], instance['port']),
            'jmx_server:{}'.format(instance['host']),
        ]
        aggregator.assert_service_check('trino.can_connect', status=AgentCheck.OK, tags=tags)
