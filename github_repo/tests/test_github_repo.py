import pytest
import logging
import mock

from datadog_checks.base import ConfigurationError
from datadog_checks.github_repo import GithubRepoCheck


log = logging.getLogger('test_openstack_controller')

instance = {"repository_name": "Datadog/integrations-core"}


def test_check_invalid_configs():
    with pytest.raises(ConfigurationError):
        GithubRepoCheck('github_repo', {}, {})

    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({})

    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})


def test_check_service_checks(aggregator):
    check = GithubRepoCheck('github_repo', {'access_token': "foo"}, {})
    with pytest.raises(ConfigurationError):
        check.check({"repository_name": "bar"})

    sc = aggregator.service_checks(GithubRepoCheck.SERVICE_CHECK_NAME)
    assert sc[0].status == check.CRITICAL

# TODO: test below are using mock objects
# We also use a attr called `_ship_access_token` to not use the token when authenticating to Github


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


class CommitMock:
    def __init__(self, author):
        self.author = author


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
def test_check(stargazers_mock, watchers_mock, contributors_mock, subscribers_mock, get_commits_mock,
               instance, aggregator):
    check = GithubRepoCheck('github_repo', {"access_token": "fake_access_token"}, {})
    check._ship_access_token = True
    check.check({"repository_name": "Datadog/integrations-core"})

    aggregator.assert_metric('github_repo.stargazers', value=1.0, tags=['Datadog/integrations-core'], hostname='')
    aggregator.assert_metric('github_repo.watchers', value=2.0, tags=['Datadog/integrations-core'], hostname='')
    aggregator.assert_metric('github_repo.contributors', value=3.0, tags=['Datadog/integrations-core'], hostname='')
    aggregator.assert_metric('github_repo.subscribers', value=4.0, tags=['Datadog/integrations-core'], hostname='')

    aggregator.assert_metric('github_repo.commits', value=2.0,
                             tags=['Datadog/integrations-core', 'author1'], hostname='')
    aggregator.assert_metric('github_repo.commits', value=1.0,
                             tags=['Datadog/integrations-core', 'author2'], hostname='')

    aggregator.assert_all_metrics_covered()


# TODO: in this test we will use fixture to mock all http calls
# hence we should not need the `_ship_access_token` attr
# mock github.Requester.Requester.requestJson
# def __check(self, status, responseHeaders, output):
#     pass
#
# def requestJsonAndCheck(self, verb, url, parameters=None, headers=None, input=None):
#     based on teh url read and return the proper fixture
#     pass
#
# @mock.patch(
#     'github.Requester.Requester.requestJsonAndCheck',
#     side_effect=requestJsonAndCheck,
# )
# def test_check_using_fixtures(instance, aggregator):
#     # 'access_token': "9d34fa85024ffc195a93af23b7bd92195330c080"
#     # check = GithubRepoCheck('github_repo', {"access_token": "fake_access_token"}, {})
#     check = GithubRepoCheck('github_repo', {"access_token": "fake_access_token"}, {})
#     check._ship_access_token = True
#     # check.ship_access_token_validation = True
#     check.check({"repository_name": "Datadog/integrations-core"})
#
#     aggregator.assert_metric('github_repo.stargazers', value=1.0, tags=['Datadog/integrations-core'], hostname='')
#     aggregator.assert_metric('github_repo.watchers', value=2.0, tags=['Datadog/integrations-core'], hostname='')
#     aggregator.assert_metric('github_repo.contributors', value=3.0, tags=['Datadog/integrations-core'], hostname='')
#     aggregator.assert_metric('github_repo.subscribers', value=4.0, tags=['Datadog/integrations-core'], hostname='')
#
#     aggregator.assert_metric('github_repo.commits', value=2.0,
#                              tags=['Datadog/integrations-core', 'author1'], hostname='')
#     aggregator.assert_metric('github_repo.commits', value=1.0,
#                              tags=['Datadog/integrations-core', 'author2'], hostname='')
#
#     aggregator.assert_all_metrics_covered()

