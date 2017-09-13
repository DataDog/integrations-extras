# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# project
from checks import AgentCheck
from tests.checks.common import AgentCheckTest


@attr(requires='neo4j')
class TestNeo4j(AgentCheckTest):
    CHECK_NAME = 'neo4j'

    METRIC_TAGS = ['tag1', 'tag2']

    NEO4J_MINIMAL_CONFIG = [{
        'neo4j_url': 'http://localhost',
        'user': 'neo4j',
        'password': 'dog',
        'port': '7474'
    }]

    CONNECTION_FAILURE = [{
        'neo4j_url': 'http://localhost',
        'user': 'unknown',
        'pass': 'dog',
    }]

    NEO4J_VARS = [
        'array.store.size',
        'node.ids.inuse',
        'total.store.size',
        'node.store.size',
        'property.ids.inuse',
        'relationshiptype.ids.inuse',
        'kernel.version',
        'property.store.size',
        'store.creationdate',
		'relationship.store.size',
		'storeid',
		'kernel.starttime',
		'string.store.size',
		'relationship.ids.inuse',
		'store.log.version',
		'logicallog.size'
    ]


    def _test_optional_metrics(self, optional_metrics, at_least):
        """
        Check optional metrics - there should be at least `at_least` matches
        """

        before = len(filter(lambda m: m[3].get('tested'), self.metrics))

        for mname in optional_metrics:
            self.assertMetric('neo4j.' + mname, tags=self.METRIC_TAGS, at_least=0)

        # Compute match rate
        after = len(filter(lambda m: m[3].get('tested'), self.metrics))

        self.assertTrue(after - before > at_least)

    def test_minimal_config(self):
        config = {'instances': self.NEO4J_MINIMAL_CONFIG}
        self.run_check_twice(config)

        # Test service check
        self.assertServiceCheck('neo4j.can_connect', status=AgentCheck.OK, count=1)

        # Test metrics
        testable_metrics = (self.NEO4J_VARS)

        for mname in testable_metrics:
            self.assertMetric('neo4j.' + mname, at_least=1)
        self.coverage_report()



    def test_connection_failure(self):
        """
        Service check reports connection failure
        """
        config = {'instances': self.CONNECTION_FAILURE}

        self.assertRaises(
            Exception,
            lambda: self.run_check(config)
        )

        self.assertServiceCheck('neo4j.can_connect', status=AgentCheck.CRITICAL, count=1)
        self.coverage_report()
