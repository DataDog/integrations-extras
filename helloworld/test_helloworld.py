# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p

# project
from tests.checks.common import AgentCheckTest


instance = {
    'url': 'http://localhost:8080',
}


# NOTE: Feel free to declare multiple test classes if needed

@attr(requires='helloworld')
class TestHelloworld(AgentCheckTest):
    """Basic Test for helloworld integration."""
    CHECK_NAME = 'helloworld'

    def test_check(self):
        """
        Testing Helloworld check.
        """
	self.run_check({"instances": [instance]})
	self.assertMetric("helloworld.value", count=1, tags=["url:http://localhost:8080"])
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
