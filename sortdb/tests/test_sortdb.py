# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import json
import os

import pytest
from mock import MagicMock

from datadog_checks.sortdb import SortdbCheck

CHECK_NAME = 'sortdb'
HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def instance():
    return {'url': 'http://localhost:8080/stats'}


EXPECTED_VALUES = (
    ("sortdb.stats.total_requests", 2),
    ("sortdb.stats.total_seeks", 24),
    ("sortdb.stats.get_requests", 3),
    ("sortdb.stats.get_hits", 3),
    ("sortdb.stats.get_misses", 0),
    ("sortdb.stats.get_requests.avg", 448),
    ("sortdb.stats.get_requests.95percentile", 1323),
    ("sortdb.stats.get_requests.99percentile", 1323),
    ("sortdb.stats.mget_requests", 0),
    ("sortdb.stats.mget_hits", 0),
    ("sortdb.stats.mget_misses", 0),
    ("sortdb.stats.mget_requests.avg", 0),
    ("sortdb.stats.mget_requests.95percentile", 0),
    ("sortdb.stats.mget_requests.99percentile", 0),
    ("sortdb.stats.fwmatch_requests", 1),
    ("sortdb.stats.fwmatch_hits", 1),
    ("sortdb.stats.fwmatch_misses", 0),
    ("sortdb.stats.fwmatch_requests.avg", 10),
    ("sortdb.stats.fwmatch_requests.95percentile", 10),
    ("sortdb.stats.fwmatch_requests.99percentile", 10),
    ("sortdb.stats.range_requests", 2),
    ("sortdb.stats.range_hits", 1),
    ("sortdb.stats.range_misses", 1),
    ("sortdb.stats.range_requests.avg", 18),
    ("sortdb.stats.range_requests.95percentile", 24),
    ("sortdb.stats.range_requests.99percentile", 24),
    ("sortdb.stats.db_size.bytes", 767557632),
    ("sortdb.stats.db_mtime", 1435463934),
)


def test_check(aggregator, instance):
    """
    Testing Sortdb check.
    """
    check = SortdbCheck(CHECK_NAME, {}, {})
    with open(os.path.join(HERE, 'sortdb_metrics.json'), 'r') as f:
        check._get_response_from_url = MagicMock(return_value=json.load(f))

    check.check(instance)
    for metric, value in EXPECTED_VALUES:
        aggregator.assert_metric(metric, value=value)

    aggregator.assert_service_check(check.SORTDB_SERVICE_CHECK)
    # Raises when COVERAGE=true and coverage < 100%
    aggregator.assert_all_metrics_covered()
