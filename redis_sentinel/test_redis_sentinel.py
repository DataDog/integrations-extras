# stdlib
from nose.plugins.attrib import attr

# 3p

# project
from tests.checks.common import AgentCheckTest


instance = {
    'host': 'localhost',
    'port': 26379,
    'password': 'datadog-is-devops-best-friend'
}


# NOTE: Feel free to declare multiple test classes if needed

@attr(requires='redis_sentinel', mock=False)  # set mock to True if appropriate
class TestRedis_sentinel(AgentCheckTest):
    """Basic Test for redis_sentinel integration."""
    CHECK_NAME = 'redis_sentinel'

    def test_check(self):
        """
        Testing Redis_sentinel check.
        """
        self.load_check({}, {})

        # run your actual tests...

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
