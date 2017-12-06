# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p

# project
from tests.checks.common import AgentCheckTest


instance = {
    'status_url': 'http://localhost:8000'
}


@attr(requires='burrow')
class TestBurrow(AgentCheckTest):
    """Basic Test for burrow integration."""
    CHECK_NAME = 'burrow'

    def test_check(self):
        """
        Testing Burrow check.
        """
        self.load_check({}, {})
        self.assertTrue(True)
        
