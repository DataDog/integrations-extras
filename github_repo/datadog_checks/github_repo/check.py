# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any, Dict

from github import Github

from datadog_checks.base import AgentCheck


class GithubRepoCheck(AgentCheck):
    def check(self, _):
        # type: (Dict[str, Any]) -> None

        g = Github()

        repo = g.get_repo("DataDog/integrations-extras")
        self.log.debug('Getting stats for: {}'.format(repo.full_name))
