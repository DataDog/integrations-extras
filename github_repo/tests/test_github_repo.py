# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.github_repo import GithubRepoCheck


# Replace with real GitHub token
ACCESS_TOKEN = ""

if ACCESS_TOKEN == "":
    pytest.fail('ACCESS_TOKEN needs to be filled in for tests to execute properly')


def test_check_invalid_configs(instance, dd_run_check):
    # Test missing access_token
    with pytest.raises(ConfigurationError):
        GithubRepoCheck('github_repo', {}, [{}])

    # Test missing repository_name
    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, [{}])
    with pytest.raises(Exception, match='Configuration error, please set a repository_name'):
        dd_run_check(check)

    # Test invalid access_token
    check = GithubRepoCheck('github_repo', {'access_token': "invalid"}, [{"repository_name": "bar"}])
    with pytest.raises(Exception, match='Failed to authenticate to Github with given access_token'):
        dd_run_check(check)

    check = GithubRepoCheck('github_repo', {'access_token': ACCESS_TOKEN}, [instance])
    dd_run_check(check)


def test_check_service_checks(instance, aggregator, dd_run_check):
    check = GithubRepoCheck('github_repo', {'access_token': "invalid"}, [{"repository_name": "invalid"}])
    with pytest.raises(Exception, match="Failed to authenticate to Github with given access_token"):
        dd_run_check(check)

    aggregator.assert_service_check(GithubRepoCheck.SERVICE_CHECK_NAME, status=check.CRITICAL)

    # We need to reset the aggregator between tests
    aggregator.reset()

    check = GithubRepoCheck('github_repo', {'access_token': ACCESS_TOKEN}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check(
        GithubRepoCheck.SERVICE_CHECK_NAME, status=check.OK, tags=['repository_name:DataDog/integrations-extras']
    )
