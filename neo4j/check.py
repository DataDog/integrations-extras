import time
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
        host, port, user, password, connect_timeout, server_name, version = self._get_config(instance)
        usrPass = user + ":" + password
        b64Val = base64.b64encode(usrPass)
        url = instance['neo4j_url'] + ":" + str(port) + "/"
        if int(version[0]) > 2:
            checkURL = host + ":" + str(port) + "/db/data/transaction/commit"
        else:
            checkURL = host + ":" + str(port) + "/v1/service/metrics"
        print checkURL
        tags = instance.get('tags', [])
        service_check_tags = tags + ['url:%s' % url]


# Neo specific
# Create payload using built-in Neo4j queryJmx stored procedure
        try:
            payload = {"statements" : [{"statement" : "CALL dbms.queryJmx('org.neo4j:*') yield attributes with  keys(attributes) as k, attributes unwind k as row return row, attributes[row]['value'];"}]}
            headers_sent = {'Content-Type':'application/json','Authorization':'Basic ' + b64Val + '','Content-Type':'application/json'}
            r = requests.post(checkURL, data=json.dumps(payload),headers=headers_sent)

        except (socket.timeout, socket.error, HttpLib2Error) as e:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL,
                               message="Unable to fetch Neo4j stats: %s" % str(e),
                               tags=service_check_tags)
            raise


        if r.status_code != 200:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL,
                               tags=service_check_tags,
                               message="Unexpected status of %s when fetching Neo4j stats, "
                               "response: %s" % (r.status_code, r))
        stats = r.json()
        self.service_check(
            self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=service_check_tags)

        for doc in stats['results'][0]['data']:
            if doc['row'][0].lower() in self.keys:
                self.gauge(server_name + "." + self.display.get(doc['row'][0].lower(),""), doc['row'][1], tags=tags)
#                self.gauge(server_name + "." + doc['row'][0].lower(), doc['row'][1], tags=tags)


    def timeout_event(self, url, timeout, aggregation_key):
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'http_check',
            'msg_title': 'URL timeout',
            'msg_text': '%s timed out after %s seconds.' % (url, timeout),
            'aggregation_key': aggregation_key
        })

    def status_code_event(self, url, r, aggregation_key):
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'http_check',
            'msg_title': 'Invalid reponse code for %s' % url,
            'msg_text': '%s returned a status of %s' % (url, r.status_code),
            'aggregation_key': aggregation_key
        })

    def _get_config(self, instance):
        self.host = instance.get('neo4j_url', '')
        self.port = int(instance.get('port', 7474))
        user = instance.get('user', '')
        password = str(instance.get('password', ''))
        connect_timeout = instance.get('connect_timeout', None)
        server_name = instance.get('server_name','')
        version = instance.get('neo4j_version', '3.1')

        return (self.host, self.port, user, password, connect_timeout,server_name, version)



if __name__ == '__main__':
    check, instances = Neo4jCheck.from_yaml('neo4j.yaml')
    for instance in instances:
        print "\nRunning the check against url: %s" % (instance['neo4j_url'])
        check.check(instance)
        if check.has_events():
            print 'Events: %s' % (check.get_events())
        print 'Metrics: %s' % (check.get_metrics())
