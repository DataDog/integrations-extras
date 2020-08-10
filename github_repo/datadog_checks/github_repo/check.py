# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any, Dict

from github import Github
from github.GithubException import BadCredentialsException, RateLimitExceededException, UnknownObjectException

from datadog_checks.base import AgentCheck, ConfigurationError


class GithubRepoCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(GithubRepoCheck, self).__init__(name, init_config, instances)

        # Fetch Config
        self.access_token = init_config.get('access_token')
        if not self.access_token:
            raise ConfigurationError('Configuration error, please set an access_token')

    def check(self, _):
        # type: (Dict[str, Any]) -> None

        repository_name = self.instance.get('repository_name')
        if not repository_name:
            raise ConfigurationError('Configuration error, please set a repository_name')

        tags = []

        # Get repository
        g = Github(self.access_token)

        try:
            repo = g.get_repo(repository_name)
            self.log.debug('Getting stats for: {}'.format(repo.name))
            tags.append("repository_name:{}".format(repository_name))

        except BadCredentialsException as e:
            self.handle_exception("Failed to authenticate to Github with given access_token", e)
        except UnknownObjectException as e:
            self.handle_exception("Failed to access repository. Check your repository_name config", e)
        except RateLimitExceededException as e:
            self.handle_exception("Rate limit exceeded. Make sure you provided an access_token", e)

    def handle_exception(self, msg, e):
        self.warning(msg)
        self.log.debug("{}: {}".format(msg, e))
        raise ConfigurationError(msg)
