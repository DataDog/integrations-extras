# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from datadog_checks.nifi import NiFiCheck


def test_check(aggregator):
    c = NiFiCheck('nifi', {}, {}, None)
    instance = {'host': 'localhost', 'port': "8080"}
    c.check(instance)
    aggregator.assert_all_metrics_covered()
