# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# project
from checks import AgentCheck
from utils.platform import Platform
from shared.test.common import AgentCheckTest


@attr(requires='mysql')
class TestMySql(AgentCheckTest):
    CHECK_NAME = 'neo4j'

    METRIC_TAGS = ['tag1', 'tag2']
    SC_TAGS = ['server:localhost', 'port:13306']
    SC_FAILURE_TAGS = ['server:localhost', 'port:unix_socket']


    MYSQL_MINIMAL_CONFIG = [{
        'server': 'localhost',
        'user': 'neo4j',
        'pass': 'neo4j',
        'port': '7474'
    }]


    CONNECTION_FAILURE = [{
        'server': 'localhost',
        'user': 'unknown',
        'pass': 'dog',
    }]

    NEO4J_VARS = [
        'kernelversion',
	#        'databasename',
        'mbeanquery',
        'storeid',
        'readonly',
        'storecreationdate',
        'storelogversion',
        'kernelstarttime',
        'lastcommittedtxid',
        'peaknumberofconcurrenttransactions',
        'numberofrolledbacktransactions',
        'numberofopentransactions',
        'numberofopenedtransactions',
        'numberofcommittedtransactions',
        'logicallogsize',
        'propertystoresize',
        'arraystoresize',
        'totalstoresize',
        'relationshipstoresize',
        'stringstoresize',
        'nodestoresize',
        'diagnosticsproviders',
        'locks',
        'numberofaverteddeadlocks',
        'numberofrelationshipidsinuse',
        'numberofpropertyidsinuse',
        'numberofnodeidsinuse',
        'numberofrelationshiptypeidsinuse',
        'memorypools',
        'pins',
        'evictions',
        'byteswritten',
        'filemappings',
        'fileunmappings',
        'bytesread',
        'flushes',
        'evictionexceptions',
        'faults',
        'metrics.neo4j.network.enabled',
        'metrics.neo4j.counts.enabled',
        'dbms.shell.read_only',
        'browser.remote_content_hostname_whitelist',
        'unsupported.dbms.edition',
        'dbms.connector.bolt.type',
        'dbms.backup.address',
        'dbms.connector.bolt.enabled',
        'dbms.unmanaged_extension_classes',
        'dbms.udc.enabled',
        'dbms.security.auth_enabled',
        'dbms.shell.rmi_name',
        'dbms.shell.enabled',
        'unsupported.dbms.directories.neo4j_home',
        'dbms.connector.https.address',
        'ha.pull_interval',
        'dbms.shell.host',
        'metrics.csv.enabled',
        'metrics.neo4j.tx.enabled',
        'metrics.csv.interval',
        'dbms.connector.http.enabled',
        'metrics.neo4j.pagecache.enabled',
        'metrics.enabled',
        'dbms.connector.https.type',
        'dbms.connector.http.type',
        'metrics.neo4j.enabled',
        'dbms.shell.port',
        'dbms.backup.enabled',
        'unsupported.dbms.security.auth_store.location',
        'dbms.allow_format_migration',
        'dbms.connector.https.enabled',
        'dbms.active_database',
        'dbms.memory.pagecache.size',
        'dbms.connector.bolt.tls_level',
        'dbms.connector.https.encryption',
    ]


    def _test_optional_metrics(self, optional_metrics, at_least):
        """
        Check optional metrics - there should be at least `at_least` matches
        """

        before = len(filter(lambda m: m[3].get('tested'), self.metrics))

        for mname in optional_metrics:
            self.assertMetric(mname, tags=self.METRIC_TAGS, at_least=0)

        # Compute match rate
        after = len(filter(lambda m: m[3].get('tested'), self.metrics))

        self.assertTrue(after - before > at_least)

    def test_minimal_config(self):
        config = {'instances': self.NEO4J_MINIMAL_CONFIG}
        self.run_check_twice(config)

        # Test service check
        self.assertServiceCheck('neo4j.can_connect', status=AgentCheck.OK,
                                tags=self.SC_TAGS, count=1)

        # Test metrics
        testable_metrics = (self.NEO4J_VARS)

        for mname in testable_metrics:
            self.assertMetric(mname, at_least=0)



    def test_connection_failure(self):
        """
        Service check reports connection failure
        """
        config = {'instances': self.CONNECTION_FAILURE}

        self.assertRaises(
            Exception,
            lambda: self.run_check(config)
        )

        self.assertServiceCheck('neo4j.can_connect', status=AgentCheck.CRITICAL,
                                tags=self.SC_FAILURE_TAGS, count=1)
        self.coverage_report()