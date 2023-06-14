import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.wayfinder import WayfinderCheck

from .common import MOCK_INSTANCE


@pytest.mark.unit
def test_config():
    with pytest.raises(ConfigurationError):
        WayfinderCheck('wayfinder', {}, [{}])

    # this should not fail
    WayfinderCheck('wayfinder', {}, [MOCK_INSTANCE])


@pytest.mark.unit
def test_service_check(aggregator):
    check = WayfinderCheck('wayfinder', {}, [MOCK_INSTANCE])
    with pytest.raises(Exception):
        check.check(MOCK_INSTANCE)
        aggregator.assert_service_check()
