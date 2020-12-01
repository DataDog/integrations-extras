import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.octoprint import OctoprintCheck


@pytest.mark.unit
def test_config():
    instance = {}
    c = OctoprintCheck('octoprint', {}, [instance])

    # empty instance
    with pytest.raises(ConfigurationError):
        c.check(instance)

    # # only the url
    # with pytest.raises(ConfigurationError):
    #     c.check({'url': 'http://octoprint'})

    # # only the search string
    # with pytest.raises(ConfigurationError):
    #     c.check({'search_string': 'OctoPrint'})

    # # only the search string
    # with pytest.raises(ConfigurationError):
    #     c.check({'search_string': 'Python'})

    # # only the search string
    # with pytest.raises(ConfigurationError):
    #     c.check({'search_string': 'Please log in'})

    # # this shouldn't fail
    # c.check({'url': 'http://octoprint', 'search_string': 'OctoPrint'})


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = OctoprintCheck('octoprint', {}, [instance])

    # the check will send OK
    c.check(instance)
    aggregator.assert_service_check('octoprint.search', OctoprintCheck.OK)

    # the check will send WARNING
    instance['search_string'] = 'Apache'
    c.check(instance)
    aggregator.assert_service_check('octoprint.search', OctoprintCheck.WARNING)
