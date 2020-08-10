# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from collections import Counter
from datetime import datetime
from typing import Any, Dict

from github import Github
from github.GithubException import BadCredentialsException, RateLimitExceededException, UnknownObjectException

from datadog_checks.base import AgentCheck, ConfigurationError


class GithubRepoCheck(AgentCheck):
    SERVICE_CHECK_NAME = "github_repo.up"

    def __init__(self, name, init_config, instances):
        # NOTE: We need super to initialize self.log
        super(GithubRepoCheck, self).__init__(name, init_config, instances)

        # Fetch Config
        self.access_token = init_config.get('access_token')
        if not self.access_token:
            raise ConfigurationError('Configuration error, please set an access_token')

        self.cache = Counter()
        self.since = None

    def check(self, _):
        # type: (Dict[str, Any]) -> None

        repository_name = self.instance.get('repository_name')
        if not repository_name:
            raise ConfigurationError('Configuration error, please set a repository_name')

        # NOTE: custom_tags is a stretch
        tags = self.instance.get('custom_tags', [])

        g = Github(self.access_token)

        try:
            repo = g.get_repo(repository_name)
            self.log.debug('Getting stats for: {}'.format(repo.full_name))
            tags.append("repository_name:{}".format(repository_name))

        except BadCredentialsException as e:
            self.handle_exception(
                "Failed to authenticate to Github with given access_token", AgentCheck.CRITICAL, tags, e
            )
        except UnknownObjectException as e:
            self.handle_exception(
                "Failed to access repository. Check your repository_name config", AgentCheck.CRITICAL, tags, e
            )
        except RateLimitExceededException as e:
            self.handle_exception(
                "Rate limit exceeded. Make sure you provided an access_token", AgentCheck.WARNING, tags, e
            )

        try:
            stargazers = repo.get_stargazers().totalCount
            self.gauge('github_repo.stargazers', stargazers, tags=tags)
            watchers = repo.get_watchers().totalCount
            self.gauge('github_repo.watchers', watchers, tags=tags)
            contributors = repo.get_contributors().totalCount
            self.gauge('github_repo.contributors', contributors, tags=tags)
            subscribers = repo.get_subscribers().totalCount
            self.gauge('github_repo.subscribers', subscribers, tags=tags)

            if self.since is None:
                # We need to warm the cache
                commits = repo.get_commits()
            else:
                commits = repo.get_commits(since=self.since)

            self.since = datetime.now()

            for commit in commits:
                if commit.author:
                    author = commit.author.login
                else:
                    # CI produces empty author values
                    author = commit.commit.author.name
                self.cache[author] += 1

            # Submit metrics with author tag
            for author, commit_count in self.cache.items():
                self.gauge('github_repo.commits', commit_count, tags=tags + ["contributor:{}".format(author)])

        except RateLimitExceededException as e:
            self.handle_exception(
                "Rate limit exceeded. Make sure you provided an access_token", AgentCheck.WARNING, tags, e
            )

        # NOTE: The OK state service check must be at the end
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=tags)

    def handle_exception(self, msg, status, tags, e):
        self.warning(msg)
        self.log.debug("{}: {}".format(msg, e))
        self.service_check(self.SERVICE_CHECK_NAME, status, tags=tags)
        raise ConfigurationError(msg)
