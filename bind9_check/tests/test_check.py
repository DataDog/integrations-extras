# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.bind9_check import bind9_check


def test_check(aggregator):
    c = bind9_check('bind9_check', {}, {}, None)
    c.check({})
    aggregator.assert_all_metrics_covered()
