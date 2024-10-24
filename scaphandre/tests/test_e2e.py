# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.base.constants import ServiceCheck

from . import common


@pytest.mark.e2e
def test_check_scaphandre_e2e(dd_agent_check, instance):
    aggregator = dd_agent_check(instance, rate=True)
    metrics = common.METRICS

    for metric in metrics:
        aggregator.assert_metric(name='scaphandre.' + metric)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('scaphandre.openmetrics.health', ServiceCheck.OK, count=2)
