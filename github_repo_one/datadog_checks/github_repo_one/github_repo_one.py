from github import Github
from github.GithubException import BadCredentialsException, RateLimitExceededException, UnknownObjectException

from datadog_checks.base import AgentCheck, ConfigurationError


class GithubRepoOneCheck(AgentCheck):
    SERVICE_CHECK_NAME = "github_repo.up"

    def __init__(self, name, init_config, agentConfig, instances=None):
        super(GithubRepoOneCheck, self).__init__(name, init_config, agentConfig, instances)

        # Fetch Config
        self.access_token = init_config.get('access_token')
        if not self.access_token:
            raise ConfigurationError('Configuration error, please set an access_token')

    def check(self, instance):
        repository_name = instance.get('repository_name')
        if not repository_name:
            raise ConfigurationError('Configuration error, please set a repository_name')

        # NOTE: custom_tags is a stretch
        tags = instance.get('custom_tags', [])

        # Get repository
        g = Github(self.access_token)

        try:
            repo = g.get_repo(repository_name)
            self.log.debug(repo.full_name)
            tags.append(repository_name)

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

        # NOTE: The OK state service check must be at the end
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=tags)

    def handle_exception(self, msg, status, tags, e):
        self.warning(msg)
        self.log.debug("{}: {}".format(msg, e))
        self.service_check(self.SERVICE_CHECK_NAME, status, tags=tags)
        raise ConfigurationError(msg)
