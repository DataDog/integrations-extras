# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import logging
import mock

from datadog_checks.github_repo import GithubRepoCheck


log = logging.getLogger('test_openstack_controller')


class TotalCountMock:
    def __init__(self, total_count):
        self.totalCount = total_count


def get_stargazers_mock():
    return TotalCountMock(1)


def get_watchers_mock():
    return TotalCountMock(2)


def get_contributors_mock():
    return TotalCountMock(3)


def get_subscribers_mock():
    return TotalCountMock(4)


class NamedUserMock:
    def __init__(self, login):
        self.login = login


class CommitMock:
    class AuthorMock:
        def __init__(self, login):
            self.login = login

    def __init__(self, author):
        self.author = NamedUserMock(author)


def get_commits_mock():
    return [CommitMock("author1"), CommitMock("author1"), CommitMock("author2")]


@mock.patch(
    'github.Repository.Repository.get_stargazers',
    side_effect=get_stargazers_mock,
)
@mock.patch(
    'github.Repository.Repository.get_watchers',
    side_effect=get_watchers_mock,
)
@mock.patch(
    'github.Repository.Repository.get_contributors',
    side_effect=get_contributors_mock,
)
@mock.patch(
    'github.Repository.Repository.get_subscribers',
    side_effect=get_subscribers_mock,
)
@mock.patch(
    'github.Repository.Repository.get_commits',
    side_effect=get_commits_mock,
)
def test_check_using_mocks(stargazers_mock, watchers_mock, contributors_mock, subscribers_mock, commits_mock,
               instance, aggregator):
    check = GithubRepoCheck('github_repo', {"access_token": "fake_access_token"}, {})
    check._ship_access_token = True
    check.check(instance)

    aggregator.assert_metric('github_repo.stargazers', value=1.0, tags=['Datadog/integrations-core'])
    aggregator.assert_metric('github_repo.watchers', value=2.0, tags=['Datadog/integrations-core'])
    aggregator.assert_metric('github_repo.contributors', value=3.0, tags=['Datadog/integrations-core'])
    aggregator.assert_metric('github_repo.subscribers', value=4.0, tags=['Datadog/integrations-core'])

    aggregator.assert_metric('github_repo.commits', value=2.0, tags=['Datadog/integrations-core', 'author1'])
    aggregator.assert_metric('github_repo.commits', value=1.0, tags=['Datadog/integrations-core', 'author2'])

    aggregator.assert_all_metrics_covered()
