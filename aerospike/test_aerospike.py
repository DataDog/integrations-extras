# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest


instance = {
    'host': 'localhost',
    'port': 26379,
    'password': 'datadog-is-devops-best-friend'
}


# NOTE: Feel free to declare multiple test classes if needed

@attr('unix')
@attr(requires='aerospike')
class TestAerospike(AgentCheckTest):
    CHECK_NAME = 'aerospike'

    def test_check(self):
        import aerospike

        config = {
            'instances': [
                {
                    'metrics': ['cluster_size', 'batch_error'],
                    'namespace_metrics': [
                        'objects',
                        'hwm_breached',
                        'client_write_error',
                        'client_write_success',
                        'objects',
                        'tombstones',
                        'stop_writes_count',
                        'truncate_lut',
                        'memory_data_bytes'],
                    'namespaces': {'test'},
                    'tags': ['tag:value']
                }
            ]
        }

        # sample Aerospike Python Client code
        # https://www.aerospike.com/docs/client/python/usage/kvs/write.html
        client = aerospike.client({'hosts': [('127.0.0.1', 3000)]}).connect()
        key = ('test', 'characters', 'bender')
        bins = {
            'name': 'Bender',
            'serialnum': 2716057,
            'lastsentence': {
                'BBS': "Well, we're boned",
                'TBwaBB': 'I love you, meatbags!',
                'BG': 'Whip harder, Professor!',
                'ltWGY': 'Into the breach, meatbags. Or not, whatever'},
            'composition': ["40% zinc", "40% titanium", "30% iron", "40% dolomite"],
            'apartment': bytearray(b'\x24'),
            'quote_cnt': 47
        }
        client.put(key, bins)
        client.close()

        self.run_check(config)
        self.assertMetric('aerospike.cluster_size', at_least=1)
        self.assertMetric('aerospike.namespace.objects', at_least=1)
        self.assertMetric('aerospike.namespace.hwm_breached', at_least=1)

        self.assertMetric('aerospike.batch_error', value='0', at_least=1)
        self.assertMetric('aerospike.namespace.client_write_error', value='0', at_least=1)
        self.assertMetric('aerospike.namespace.client_write_success', value='1', at_least=1)
        self.assertMetric('aerospike.namespace.truncate_lut', value='0', at_least=1)
        self.assertMetric('aerospike.namespace.tombstones', value='0', at_least=1)
        self.assertMetric('aerospike.set.tombstones', value='0', at_least=1)
        self.assertMetric('aerospike.set.objects', value='1', at_least=1)
        self.assertMetricTag('aerospike.set.objects', tag='namespace:test', at_least=1)
        self.assertMetric('aerospike.set.stop_writes_count', value='0', at_least=1)
        self.assertMetricTag('aerospike.set.stop_writes_count', tag='set:characters', at_least=1)
        self.assertMetric('aerospike.set.truncate_lut', value='0', at_least=1)
        self.assertMetric('aerospike.set.memory_data_bytes', value='289', at_least=1)

        self.assertServiceCheckOK('aerospike.cluster_up')
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
