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


@attr(requires='travis_integration')
class TestTravis_integration(AgentCheckTest):
    CHECK_NAME = 'travis_integration'

    def test_check(self):
        """
        Testing Travis_integration check.
        """
        # run your actual tests...
        self.run_check({})

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
