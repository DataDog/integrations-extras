# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.github_repo import GithubRepoCheck


def test_check_invalid_configs(dd_run_check, instance):
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

    check = GithubRepoCheck('github_repo', {'access_token': "<YOUR_ACCESS_TOKEN>"}, [instance])
    dd_run_check(check)
