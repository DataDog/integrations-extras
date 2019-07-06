# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import logging

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.github_repo import GithubRepoCheck

log = logging.getLogger('test_github_repo')


def test_check_invalid_configs():
    # Test missing access_token
    with pytest.raises(ConfigurationError):
        GithubRepoCheck('github_repo', {}, {})

    # Test missing repository_name
    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({})

    # Test invalid access_token
    check = GithubRepoCheck('github_repo', {'access_token': "invalid"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})


def test_check_service_checks(aggregator):
    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    sc = aggregator.service_checks(GithubRepoCheck.SERVICE_CHECK_NAME)
    assert sc[0].status == check.CRITICAL
