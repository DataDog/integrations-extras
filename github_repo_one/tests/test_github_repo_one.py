import logging

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.github_repo_one import GithubRepoOneCheck

log = logging.getLogger('test_openstack_controller')


def test_check_invalid_configs():
    with pytest.raises(ConfigurationError):
        GithubRepoOneCheck('github_repo', {}, {})

    check = GithubRepoOneCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    check = GithubRepoOneCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({})

    check = GithubRepoOneCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    # check = GithubRepoOneCheck('github_repo', {'access_token': "<YOUR_TOKEN>"}, {})
    # check.check({"repository_name": "Datadog/integrations-core"})


def test_check_service_checks(aggregator):
    check = GithubRepoOneCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    sc = aggregator.service_checks(GithubRepoOneCheck.SERVICE_CHECK_NAME)
    assert sc[0].status == check.CRITICAL

    # check = GithubRepoOneCheck('github_repo', {'access_token': "<YOUR_TOKEN>"}, {})
    # check.check({"repository_name": "Datadog/integrations-core"})
    # assert sc[0].status == check.OK
