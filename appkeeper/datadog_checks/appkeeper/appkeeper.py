from datadog_checks.base import AgentCheck, ConfigurationError

class AppKeeperCheck(AgentCheck):
    def check(self, instance):
        self.service_check('appkeeper.test', self.OK)
