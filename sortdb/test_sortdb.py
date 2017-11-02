# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import os
from nose.plugins.attrib import attr
import json
# 3p
from mock import MagicMock
# project
from tests.checks.common import AgentCheckTest, Fixtures


instance = {
    'url': 'http://localhost:8080/stats'
}

SORTDB_SERVICE_CHECK = 'sortdb.http.can_connect'

EXPECTED_VALUES = (("sortdb.stats.total_requests", 2),
  ("sortdb.stats.total_seeks", 24),
  ("sortdb.stats.get_requests",3),
  ("sortdb.stats.get_hits", 3),
  ("sortdb.stats.get_misses",0),
  ("sortdb.stats.get_requests.avg",448),
  ("sortdb.stats.get_requests.95percentile",1323),
  ("sortdb.stats.get_requests.99percentile",1323),
  ("sortdb.stats.mget_requests", 0),
  ("sortdb.stats.mget_hits",0),
  ("sortdb.stats.mget_misses", 0),
  ("sortdb.stats.mget_requests.avg",0),
  ("sortdb.stats.mget_requests.95percentile",0),
  ("sortdb.stats.mget_requests.99percentile",0),
  ("sortdb.stats.fwmatch_requests",1),
  ("sortdb.stats.fwmatch_hits",1),
  ("sortdb.stats.fwmatch_misses",0),
  ("sortdb.stats.fwmatch_requests.avg",10),
  ("sortdb.stats.fwmatch_requests.95percentile",10),
  ("sortdb.stats.fwmatch_requests.99percentile",10),
  ("sortdb.stats.range_requests",2),
  ("sortdb.stats.range_hits",1),
  ("sortdb.stats.range_misses",1),
  ("sortdb.stats.range_requests.avg",18),
  ("sortdb.stats.range_requests.95percentile",24),
  ("sortdb.stats.range_requests.99percentile",24),
  ("sortdb.stats.db_size.bytes",767557632),
  ("sortdb.stats.db_mtime",1435463934))


class TestSortdb(AgentCheckTest):
    """Basic Test for sortdb integration."""
    CHECK_NAME = 'sortdb'
    FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'ci')
 

    def test_check(self):
        """
        Testing Sortdb check.
        """
        content_type = 'application/json; version=0.0.4'
        f_name = os.path.join(os.path.dirname(__file__), 'ci', 'sortdb_metrics.json')
        with open(f_name, 'r') as f:
            bin_data = json.load(f)
        mocks = {
            '_get_response_from_url': MagicMock(return_value=bin_data)
        }
        self.run_check({'instances': [instance]}, mocks=mocks)
        for metric, value in EXPECTED_VALUES:
            self.assertMetric(metric, value=value)

        self.assertServiceCheck(SORTDB_SERVICE_CHECK)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
