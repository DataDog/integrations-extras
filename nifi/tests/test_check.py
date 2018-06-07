# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import pytest
from datadog_checks.nifi import NiFiCheck
from datadog_checks.errors import CheckException


def test_check(aggregator):
    c = NiFiCheck('nifi', {}, {}, None)
    with pytest.raises(CheckException):
        c.check({})
    instance = {'host': 'http://localhost:8080'}
    c.check(instance)
    aggregator.assert_all_metrics_covered()
