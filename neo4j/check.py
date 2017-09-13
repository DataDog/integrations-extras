import requests

# stdlib
import socket

# 3rd party
from httplib2 import HttpLib2Error
import simplejson as json
import base64

# project
from checks import AgentCheck

class Neo4jCheck(AgentCheck):
    SERVICE_CHECK_NAME = 'neo4j.can_connect'

    # Neo4j metrics to send
    keys = set([
        'kernelversion',
        'storeid',
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
    ])

    display = {'kernelversion':'neo4j.kernel.version',
               'storeid':'neo4j.storeid',
               'storecreationdate':'neo4j.store.creationdate',
               'storelogversion':'neo4j.store.log.version',
               'kernelstarttime':'neo4j.kernel.starttime',
               'lastcommittedtxid':'neo4j.last.committed.transaction.id',
               'peaknumberofconcurrenttransactions':'neo4j.peak.concurrent.transactions',
               'numberofrolledbacktransactions':'neo4j.peak.rolledback.transactions',
               'numberofopentransactions':'neo4j.open.transactions',
               'numberofopenedtransactions':'neo4j.opened.transactions',
               'numberofcommittedtransactions':'neo4j.committed.transactions',
               'logicallogsize':'neo4j.logicallog.size',
               'propertystoresize':'neo4j.property.store.size',
               'arraystoresize':'neo4j.array.store.size',
               'totalstoresize':'neo4j.total.store.size',
               'relationshipstoresize':'neo4j.relationship.store.size',
               'stringstoresize':'neo4j.string.store.size',
               'nodestoresize':'neo4j.node.store.size',
               'locks':'neo4j.locks',
               'numberofaverteddeadlocks':'neo4j.adverted.locks',
               'numberofrelationshipidsinuse':'neo4j.relationship.ids.inuse',
               'numberofpropertyidsinuse':'neo4j.property.ids.inuse',
               'numberofnodeidsinuse':'neo4j.node.ids.inuse',
               'numberofrelationshiptypeidsinuse':'neo4j.relationshiptype.ids.inuse',
               'memorypools':'neo4j.memory.pools',
               'pins':'neo4j.page.cache.pins',
               'evictions':'neo4j.page.cache.evictions',
               'byteswritten':'neo4j.bytes.written',
               'filemappings':'neo4j.page.cache.file.mappings',
               'fileunmappings':'neo4j.page.cache.file.unmappings',
               'bytesread':'neo4j.bytes.read',
               'flushes':'neo4j.page.cache.flushes',
               'evictionexceptions':'neo4j.page.cache.eviction.exceptions',
               'faults':'neo4j.page.cache.faults',
               'ha.pull_interval':'neo4j.ha.pull_interval',
               'dbms.memory.pagecache.size':'neo4j.dbms.memory.pagecache.size'}

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        host, port, user, password, connect_timeout, server_name = self._get_config(instance)
        tags = instance.get('tags', [])
        tags = tags + ['server_name:%s' % server_name]
        service_check_tags = tags + ['url:%s' % host]

        version = self._get_version(instance, service_check_tags)
        usrPass = user + ":" + password
        b64Val = base64.b64encode(usrPass)

        if version > 2:
            checkURL = host + ":" + str(port) + "/db/data/transaction/commit"
        else:
            checkURL = host + ":" + str(port) + "/v1/service/metrics"

        # Neo specific
        # Create payload using built-in Neo4j queryJmx stored procedure
        try:
            payload = {"statements" : [{"statement" : "CALL dbms.queryJmx('org.neo4j:*') yield attributes with  keys(attributes) as k, attributes unwind k as row return row, attributes[row]['value'];"}]}
            headers_sent = {'Content-Type':'application/json','Authorization':'Basic ' + b64Val + '','Content-Type':'application/json'}
            r = requests.post(checkURL, data=json.dumps(payload),headers=headers_sent)

        except (socket.timeout, socket.error, HttpLib2Error) as e:
            msg = "Unable to fetch Neo4j stats: %s" % str(e)
            self._critical_service_check(service_check_tags, msg)
            raise


        if r.status_code != 200:
            msg = "nexpected status of {0} when fetching Neo4j stats, response: {1}"
            msg = msg.format(r.status_code, r.text)
            self._critical_service_check(service_check_tags, msg)
            r.raise_for_status()

        stats = r.json()
        self.service_check(
            self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=service_check_tags)

        for doc in stats['results'][0]['data']:
            if doc['row'][0].lower() in self.keys:
                self.gauge(self.display.get(doc['row'][0].lower(),""), doc['row'][1], tags=tags)

    def _get_config(self, instance):
        host = instance.get('neo4j_url', '')
        port = int(instance.get('port', 7474))
        user = instance.get('user', '')
        password = str(instance.get('password', ''))
        connect_timeout = instance.get('connect_timeout', None)
        server_name = instance.get('server_name','')

        return (host, port, user, password, connect_timeout,server_name)

    def _get_version(self, instance, service_check_tags):
        host, port, user, password, connect_timeout, server_name = self._get_config(instance)
        usrPass = user + ":" + password
        b64Val = base64.b64encode(usrPass)
        port = int(instance.get('port', 7474))
        versionURL = host + ":" + str(port) + '/db/data/'

        #check version
        headers_sent = {'Content-Type':'application/json','Authorization':'Basic ' + b64Val + '','Content-Type':'application/json'}
        r = requests.get(versionURL,headers=headers_sent)
        if r.status_code != 200:
            msg = "unexpected status of {0} when fetching Neo4j stats, response: {1}"
            msg = msg.format(r.status_code, r.text)
            self._critical_service_check(service_check_tags, msg)
            r.raise_for_status()
        stats = r.json()
        version = stats.get('neo4j_version')
        version = version.split('.')
        if len(version) > 0:
            return int(version[0])
        return 0

    def _critical_service_check(self, service_check_tags, message):
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL,
                           tags=service_check_tags,
                           message=message)

    def above_version(self, version, to_compare):
        if version == '':
            return False
        v = version.split('.')
        v2 = to_compare.split('.')
        i = 0
        for n in v:
            if len(v2) >= i - 1:
                if int(n) > int(v2[i]):
                    return False
        return True
