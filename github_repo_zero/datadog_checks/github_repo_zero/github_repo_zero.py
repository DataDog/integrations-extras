from github import Github

from datadog_checks.base import AgentCheck


class GithubRepoZeroCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        # NOTE: We need super to initialize self.log
        super(GithubRepoZeroCheck, self).__init__(name, init_config, agentConfig, instances)

    def check(self, instance):
        g = Github()

        repo = g.get_repo("Datadog/integrations-core")
        self.log.debug(repo.full_name)
