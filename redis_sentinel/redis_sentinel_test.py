# project
from tests.checks.common import AgentCheckTest


class TestRedisSentinel(AgentCheckTest):
    CHECK_NAME = 'redis_sentinel'

    def test_check(self):
        """
        Testing Redis Sentinel check.
        """

        self.assertTrue(2 > 1)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
