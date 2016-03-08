# stdlib
from nose.plugins.attrib import attr

# project
from checks import AgentCheck
from tests.checks.common import AgentCheckTest


@attr(requires='redis')
class TestRedisSentinel(AgentCheckTest):

     def test_check(self):

        # Raises when COVERAGE=true and coverage < 100%
        self.test_checkcoverage_report()
