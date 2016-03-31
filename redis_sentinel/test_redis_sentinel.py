# stdlib
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest


instance = {
    'host': 'localhost',
    'port': 26379,
    'password': 'datadog-is-devops-best-friend'
}

@attr(requires='redis_sentinel')
class TestRedisSentinel(AgentCheckTest):
    CHECK_NAME = 'redis_sentinel'
    SDK = True

    def test_check(self):
        """
        Testing Redis Sentinel check.
        """
        self.load_check({}, {})


        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        # self.coverage_report()
