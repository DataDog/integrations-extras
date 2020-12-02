import pytest

from datadog_checks.octoprint import OctoPrintCheck
from datadog_checks.base import ConfigurationError


@pytest.mark.unit
def test_config():
    instance = {}
    c = OctoPrintCheck('octoprint', {}, [instance])

    # empty instance
    with pytest.raises(ConfigurationError):
        c.check(instance)

    with pytest.raises(ConfigurationError):
        c.check({'octo_api_key': 'ABC123'})


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = OctoPrintCheck('octoprint', {}, [instance])

