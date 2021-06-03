from datadog_checks.base.checks import AgentCheck
from datadog_checks.base.errors import CheckException


class Neo4jCheck(AgentCheck):
    SERVICE_CHECK_NAME = 'neo4j.can_connect'

    HTTP_CONFIG_REMAPPER = {
        'user': {
            'name': 'username',
        },
        'default_timeout': {
            'name': 'timeout',
        },
    }

    # Neo4j metrics to send
    keys = set(
        [
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
            'ha.pull_interval',
            'dbms.memory.pagecache.size',
        ]
    )

    display = {
        'storecreationdate': 'neo4j.store.creationdate',
        'storelogversion': 'neo4j.store.log.version',
        'kernelstarttime': 'neo4j.kernel.starttime',
        'lastcommittedtxid': 'neo4j.last.committed.transaction.id',
        'peaknumberofconcurrenttransactions': 'neo4j.peak.concurrent.transactions',
        'numberofrolledbacktransactions': 'neo4j.peak.rolledback.transactions',
        'numberofopentransactions': 'neo4j.open.transactions',
        'numberofopenedtransactions': 'neo4j.opened.transactions',
        'numberofcommittedtransactions': 'neo4j.committed.transactions',
        'logicallogsize': 'neo4j.logicallog.size',
        'propertystoresize': 'neo4j.property.store.size',
        'arraystoresize': 'neo4j.array.store.size',
        'totalstoresize': 'neo4j.total.store.size',
        'relationshipstoresize': 'neo4j.relationship.store.size',
        'stringstoresize': 'neo4j.string.store.size',
        'nodestoresize': 'neo4j.node.store.size',
        'locks': 'neo4j.locks',
        'numberofaverteddeadlocks': 'neo4j.adverted.locks',
        'numberofrelationshipidsinuse': 'neo4j.relationship.ids.inuse',
        'numberofpropertyidsinuse': 'neo4j.property.ids.inuse',
        'numberofnodeidsinuse': 'neo4j.node.ids.inuse',
        'numberofrelationshiptypeidsinuse': 'neo4j.relationshiptype.ids.inuse',
        'memorypools': 'neo4j.memory.pools',
        'pins': 'neo4j.page.cache.pins',
        'evictions': 'neo4j.page.cache.evictions',
        'byteswritten': 'neo4j.bytes.written',
        'filemappings': 'neo4j.page.cache.file.mappings',
        'fileunmappings': 'neo4j.page.cache.file.unmappings',
        'bytesread': 'neo4j.bytes.read',
        'flushes': 'neo4j.page.cache.flushes',
        'evictionexceptions': 'neo4j.page.cache.eviction.exceptions',
        'faults': 'neo4j.page.cache.faults',
        'ha.pull_interval': 'neo4j.ha.pull_interval',
        'dbms.memory.pagecache.size': 'neo4j.dbms.memory.pagecache.size',
    }

    def check(self, _):
        host, port, server_name = self._get_config(self.instance)
        tags = self.instance.get('tags', [])
        tags.append('server_name:{}'.format(server_name))
        service_check_tags = tags + ['url:{}'.format(host)]

        # Neo specific
        # Create payload using built-in Neo4j queryJmx stored procedure
        payload = {
            "statements": [
                {
                    "statement": "CALL dbms.queryJmx('org.neo4j:*') yield attributes with  "
                    "keys(attributes) as k, attributes unwind k as "
                    "row return row, attributes[row]['value'];"
                }
            ]
        }
        try:
            version = self._get_version(host, port, service_check_tags)

            if version > 2:
                check_url = "{}:{}/db/data/transaction/commit".format(host, port)
            else:
                check_url = "{}:{}/v1/service/metrics".format(host, port)
            r = self.http.post(check_url, json=payload)
        except Exception as e:
            msg = "Unable to fetch Neo4j stats: {}".format(e)
            self._critical_service_check(service_check_tags, msg)
            raise CheckException(msg)

        if r.status_code != 200:
            msg = "Unexpected status of {0} when fetching Neo4j stats, response: {1}"
            msg = msg.format(r.status_code, r.text)
            self._critical_service_check(service_check_tags, msg)
            r.raise_for_status()

        stats = r.json()
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=service_check_tags)

        for doc in stats['results'][0]['data']:
            name = doc['row'][0].lower()
            if name in self.keys:
                try:
                    self.gauge(self.display.get(name, ""), doc['row'][1], tags=tags)
                except TypeError:
                    continue
                except ValueError:
                    continue

    def _get_config(self, instance):
        host = instance.get('neo4j_url', '')
        port = int(instance.get('port', 7474))
        server_name = instance.get('server_name', '')

        return host, port, server_name

    def _get_version(self, host, port, service_check_tags):
        version_url = '{}:{}/db/data/'.format(host, port)
        r = self.http.get(version_url)
        if r.status_code != 200:
            msg = "unexpected status of {0} when fetching Neo4j stats, response: {1}"
            msg = msg.format(r.status_code, r.text)
            self._critical_service_check(service_check_tags, msg)
            r.raise_for_status()
        stats = r.json()
        version = stats.get('neo4j_version')
        self.log.debug("Neo4j version: %s", version)
        version = version.split('.')
        if version:
            return int(version[0])
        return 0

    def _critical_service_check(self, service_check_tags, message):
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags=service_check_tags, message=message)
