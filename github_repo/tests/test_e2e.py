import mock

from datadog_checks.github_repo import GithubRepoCheck


class TotalCountMock(object):
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


@mock.patch('github.Repository.Repository.get_stargazers', side_effect=get_stargazers_mock)
@mock.patch('github.Repository.Repository.get_watchers', side_effect=get_watchers_mock)
@mock.patch('github.Repository.Repository.get_contributors', side_effect=get_contributors_mock)
@mock.patch('github.Repository.Repository.get_subscribers', side_effect=get_subscribers_mock)
def test_check_using_mocks(stargazers_mock, watchers_mock, contributors_mock, subscribers_mock, instance, aggregator, dd_run_check):
    check = GithubRepoCheck('github_repo', {"access_token": "<YOUR_ACCESS_TOKEN>"}, [instance])
    dd_run_check(check)
    aggregator.assert_metric('github_repo.stargazers', value=1.0, tags=['repository_name:DataDog/integrations-extras'])
    aggregator.assert_metric('github_repo.watchers', value=2.0, tags=['repository_name:DataDog/integrations-extras'])
    aggregator.assert_metric(
        'github_repo.contributors', value=3.0, tags=['repository_name:DataDog/integrations-extras']
    )
    aggregator.assert_metric('github_repo.subscribers', value=4.0, tags=['repository_name:DataDog/integrations-extras'])

    aggregator.assert_all_metrics_covered()
