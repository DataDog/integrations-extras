# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.nifi import NiFiCheck
from datadog_checks.errors import CheckException

CHECK_NAME = 'nifi'


def test_check(aggregator):
    c = NiFiCheck(CHECK_NAME, {}, {}, None)
    with pytest.raises(CheckException):
        c.check({})
    instance = {'url': 'http://localhost:8080'}
    c.check(instance)
    aggregator.assert_all_metrics_covered()
