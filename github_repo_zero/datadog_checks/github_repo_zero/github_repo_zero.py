from github import Github

from datadog_checks.base import AgentCheck


class GithubRepoZeroCheck(AgentCheck):
    def check(self, instance):
        g = Github()

        repo = g.get_repo("Datadog/integrations-core")
        self.log.debug(repo.full_name)
