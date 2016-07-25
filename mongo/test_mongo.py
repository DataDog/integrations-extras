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

@attr(requires='mongo', mock=False)  # set mock to True if appropriate
class TestMongo(AgentCheckTest):
    """Basic Test for mongo integration."""
    CHECK_NAME = 'mongo'

    def test_check(self):
        """
        Testing Mongo check.
        """
        self.load_check({}, {})

        # run your actual tests...

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
