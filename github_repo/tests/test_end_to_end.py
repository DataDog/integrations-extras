# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import json
import logging
import os

import mock

from datadog_checks.github_repo import GithubRepoCheck

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
log = logging.getLogger('test_github_repo')


def request_json_and_check(verb, url, parameters=None, headers=None, input=None):
    log.debug("URL {}".format(url))
    if url == "https://api.github.com/repos/DataDog/integrations-extras/commits":
        mock_path = "commits.json"
    elif url == "https://api.github.com/repos/DataDog/integrations-extras/contributors":
        mock_path = "contributors.json"
    elif url == "/repos/Datadog/integrations-extras":
        mock_path = "repo.json"
    elif url == "https://api.github.com/repos/DataDog/integrations-extras/stargazers":
        mock_path = "stargazers.json"
    elif url == "https://api.github.com/repos/DataDog/integrations-extras/subscribers":
        mock_path = "subscribers.json"
    elif url == "https://api.github.com/repos/DataDog/integrations-extras/watchers":
        mock_path = "watchers.json"
    else:
        raise RuntimeError()

    mock_path = os.path.join(FIXTURES_DIR, mock_path)
    with open(mock_path, 'r') as f:
        fixture = f.read()
        j = json.loads(fixture)
        log.debug("FIXTURE {}".format(fixture))
        log.debug("HEADER {}".format(j.get('header')))
        log.debug("DATA {}".format(j.get('data')))
        return j.get('header'), j.get('data')


@mock.patch('github.Requester.Requester.requestJsonAndCheck', side_effect=request_json_and_check)
def test_check_using_fixtures(request_json_and_check_mock, instance, aggregator):
    check = GithubRepoCheck('github_repo', {"access_token": "fake_access_token"}, {})
    check.check(instance)

    aggregator.assert_metric('github_repo.subscribers', value=1.0, tags=['repository_name:Datadog/integrations-extras'])
    aggregator.assert_metric('github_repo.stargazers', value=1.0, tags=['repository_name:Datadog/integrations-extras'])
    aggregator.assert_metric(
        'github_repo.commits', value=1.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:albertvaka']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=1.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:l0k0ms']
    )
    aggregator.assert_metric(
        'github_repo.commits',
        value=7.0,
        tags=['repository_name:Datadog/integrations-extras', 'contributor:FlorianVeaux'],
    )
    aggregator.assert_metric(
        'github_repo.commits', value=2.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:coignetp']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=2.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:dabcoder']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=2.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:ofek']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=1.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:mikekatica']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=2.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:therve']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=1.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:scseanchow']
    )
    aggregator.assert_metric(
        'github_repo.commits', value=7.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:hithwen']
    )
    aggregator.assert_metric(
        'github_repo.commits',
        value=1.0,
        tags=['repository_name:Datadog/integrations-extras', 'contributor:victorvanleeuwen'],
    )
    aggregator.assert_metric(
        'github_repo.commits',
        value=2.0,
        tags=['repository_name:Datadog/integrations-extras', 'contributor:AlexandreYang'],
    )
    aggregator.assert_metric(
        'github_repo.commits', value=1.0, tags=['repository_name:Datadog/integrations-extras', 'contributor:jeffwidman']
    )
    aggregator.assert_metric('github_repo.watchers', value=1.0, tags=['repository_name:Datadog/integrations-extras'])
    aggregator.assert_metric(
        'github_repo.contributors', value=1.0, tags=['repository_name:Datadog/integrations-extras']
    )

    aggregator.assert_all_metrics_covered()
