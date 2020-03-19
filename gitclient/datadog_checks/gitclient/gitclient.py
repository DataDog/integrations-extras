import datetime

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.utils.subprocess_output import get_subprocess_output


class GitclientCheck(AgentCheck):
    def check(self, instance):

        # Grab input parameters
        git_http_repo_url = instance.get('git_http_repo_url')

        # Ensure input parameters exist
        if not git_http_repo_url:
            raise ConfigurationError('Configuration error, please add git_http_repo_url value to gitclient.yaml')

        # Ensure using http or https
        if 'https://' not in git_http_repo_url and 'http://' not in git_http_repo_url:
            raise ConfigurationError('Configuration error, please use https:// or http:// url')

        # Ensure Git client exists on system
        out, err, retcode = get_subprocess_output(["git", "--version"], self.log, raise_on_empty_output=True)
        if retcode != 0:
            raise ConfigurationError('Git client not installed on the system which is running the Git Client check')

        # Check if git client can connect to remote repo
        t0 = datetime.datetime.now()
        out, err, retcode = get_subprocess_output(["git", "ls-remote"], self.log, raise_on_empty_output=True)

        # Submit Metric
        t1 = datetime.datetime.now()
        elapsed = t1 - t0
        response_time = int(elapsed.total_seconds() * 1000)
        self.gauge("gitclient.latency", response_time)

        # Submit Service check
        if retcode != 0:
            e = "Git client received return code {0} when connecting to git_http_repo_url: {1}".format(
                retcode, git_http_repo_url
            )
            self.service_check('gitclient', self.CRITICAL, message=str(e))
        else:
            self.service_check('gitclient', self.OK)
