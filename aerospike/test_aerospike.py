# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

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

@attr(requires='aerospike')
class TestAerospike(AgentCheckTest):
    CHECK_NAME = 'aerospike'

    def test_check(self):
        config = {
            'instances': [
                {
                    'metrics':['cluster_size'],
                    'namespace_metrics':['objects'],
                    'namespaces':{'test'},
                    'tags':['tag:value']
                }
            ]
        }
        self.run_check(config)

        self.assertMetric('aerospike.cluster_size', at_least=1)
        self.assertMetric('aerospike.namespace.objects', at_least=1)
        self.assertServiceCheckOK('aerospike.cluster_up')

        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
