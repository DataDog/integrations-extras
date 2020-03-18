import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.gitclient import GitclientCheck


@pytest.mark.integration
def test_check(aggregator, instance):
    c = GitclientCheck('gitclient', {}, [instance])

    # this should not fail unless the Datadog integrations repo changes
    c.check({'git_http_repo_url': 'https://github.com/DataDog/integrations-extras.git'})
    aggregator.assert_service_check('gitclient', GitclientCheck.OK)


@pytest.mark.unit
def test_config():
    instance = {}
    c = GitclientCheck('gitclient', {}, [instance])

    # empty instance
    with pytest.raises(ConfigurationError):
        c.check(instance)

    # bad key name
    with pytest.raises(ConfigurationError):
        c.check({'bad_key_value': 'https://foobar'})

    # bad format (needs http:// or https://)
    with pytest.raises(ConfigurationError):
        c.check({'git_http_repo_url': 'git://foobar'})

    # this should not fail
    c.check({'git_http_repo_url': 'http://foobar'})
