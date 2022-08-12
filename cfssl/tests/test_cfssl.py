# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any, Dict

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.cfssl import CfsslCheck

CHECK_NAME = 'cfssl'


@pytest.mark.unit
def test_config_empty():
    instance = {}
    c = CfsslCheck(CHECK_NAME, {}, [instance])
    # empty should fail
    with pytest.raises(ConfigurationError):
        c.check(instance)


@pytest.mark.unit
def test_invalid_config(aggregator):
    # type: (AggregatorStub) -> None
    instance = {"url": "www.example.com"}

    # Invalid url parameter - should fail
    with pytest.raises(Exception):
        c = CfsslCheck(CHECK_NAME, {}, [instance])
        c.check(instance)
        aggregator.assert_service_check(CfsslCheck.SERVICE_CHECK_CONNECT_NAME, CfsslCheck.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    c = CfsslCheck(CHECK_NAME, {}, [instance])

    c.check(instance)
    aggregator.assert_service_check(CfsslCheck.SERVICE_CHECK_CONNECT_NAME, CfsslCheck.OK)
    aggregator.assert_service_check(CfsslCheck.SERVICE_CHECK_HEALTH_NAME, CfsslCheck.OK)

    instance['url'] = "http://localhost:7777"
    with pytest.raises(Exception):
        c.check(instance)
        aggregator.assert_service_check(CfsslCheck.SERVICE_CHECK_CONNECT_NAME, CfsslCheck.CRITICAL)
