# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.dev.utils import get_metadata_metrics

from .common import EXPECTED_CHECKS


@pytest.mark.e2e
def test_check_ok(dd_agent_check):
    aggregator = dd_agent_check(rate=True)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    for check in EXPECTED_CHECKS:
        aggregator.assert_service_check(check)
