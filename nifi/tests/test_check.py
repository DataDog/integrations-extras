# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from datadog_checks.nifi import NiFiCheck


def test_check(aggregator):
    c = NiFiCheck('nifi', {}, {}, None)
    c.check({})
    aggregator.assert_all_metrics_covered()
