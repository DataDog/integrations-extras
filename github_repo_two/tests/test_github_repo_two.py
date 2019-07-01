import logging

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.github_repo_two import GithubRepoTwoCheck

log = logging.getLogger('test_github_repo')


def test_check_invalid_configs():
    with pytest.raises(ConfigurationError):
        GithubRepoTwoCheck('github_repo', {}, {})

    check = GithubRepoTwoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    check = GithubRepoTwoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({})

    check = GithubRepoTwoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})


def test_check_service_checks(aggregator):
    check = GithubRepoTwoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    sc = aggregator.service_checks(GithubRepoTwoCheck.SERVICE_CHECK_NAME)
    assert sc[0].status == check.CRITICAL
