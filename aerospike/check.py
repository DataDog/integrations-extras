# Aerospike agent check for Datadog Agent.
# Copyright (C) 2015 Pippio, Inc. All rights reserved.

# stdlib
import socket
import time
import re
from contextlib import closing
from collections import namedtuple

# project
from checks import AgentCheck

SOURCE_TYPE_NAME = 'aerospike'
SERVICE_CHECK_NAME = '%s.cluster_up' % SOURCE_TYPE_NAME
CLUSTER_EVENT_TYPE = SOURCE_TYPE_NAME
NAMESPACE_EVENT_TYPE = '%s.namespace' % SOURCE_TYPE_NAME
NAMESPACE_TPS_EVENT_TYPE = '%s.namespace.tps' % SOURCE_TYPE_NAME
SINDEX_EVENT_TYPE = '%s.sindex' % SOURCE_TYPE_NAME

Addr = namedtuple('Addr', ['host', 'port'])

def parse_sindex_namespace(data, namespace):
    idxs = []
    while data != []:
        l = data.pop(0)

        match = re.match('^ns=%s:[^:]+:indexname=([^:]+):.*$' % namespace,l)
        if match == None:
            continue
        idxs.append(match.groups()[0])

    return idxs   

class AerospikeCheck(AgentCheck):

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
        self.connections = {}

    def check(self, instance):
        addr, metrics, namespace_metrics, required_namespaces, tags = \
            self._get_config(instance)

        try:
            conn = self._get_connection(addr)

            with closing(conn.makefile('r')) as fp:
                conn.send('statistics\r')
                self._process_data(fp, CLUSTER_EVENT_TYPE, metrics, tags=tags)

                namespaces = self._get_namespaces(conn, fp, required_namespaces)

                for ns in namespaces:
                    conn.send('namespace/%s\r' % ns)
                    self._process_data(fp, NAMESPACE_EVENT_TYPE, namespace_metrics, tags+['namespace:%s' % ns])

                    conn.send('sindex/%s\r' % ns)
                    for idx in parse_sindex_namespace(fp.readline().split(';')[:-1], ns):
                        conn.send('sindex/%s/%s\r' % (ns,idx))
                        self._process_data(fp, SINDEX_EVENT_TYPE, [], 
                                tags+['namespace:%s' % ns, 'sindex:%s' % idx])

                conn.send('throughput:\r')
                self._process_throughput(fp.readline().rstrip().split(';'), NAMESPACE_TPS_EVENT_TYPE, namespaces, tags)

            self.service_check(SERVICE_CHECK_NAME, AgentCheck.OK, tags=tags)
        except Exception as e:
            self.log.exception('Error while collectin Aerospike metrics at %s: %s', addr, e)
            self.connections.pop(addr, None)
            raise e

    @staticmethod
    def _get_config(instance):
        host = instance.get('host', 'localhost')
        port = int(instance.get('port', 3003))
        metrics = set(instance.get('metrics', []))
        namespace_metrics = set(instance.get('namespace_metrics', []))
        required_namespaces = instance.get('namespaces', None)
        tags = instance.get('tags', [])

        return (Addr(host,port), metrics, namespace_metrics, required_namespaces, tags)

    def _get_namespaces(self, conn, fp, required_namespaces=[]):
        conn.send('namespaces\r')
        namespaces = fp.readline().rstrip().split(';')
        if required_namespaces:
            return [v for v in namespaces if v in required_namespaces]
        else:
            return namespaces

    def _get_connection(self, addr):
        conn = self.connections.get(addr, None)

        if conn is None:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(addr)
            self.connections[addr] = conn

        return conn

    def _process_throughput(self, data, event_type, namespaces, tags={}):
        while data != []:
            l = data.pop(0)

            # skip errors
            while l.startswith('error-'):
                if data == []:
                    return
                l = data.pop(0)

            match = re.match('^{(.+)}-([^:]+):',l)
            if match == None:
                continue

            ns = match.groups()[0]
            if ns not in namespaces:
                continue

            key = match.groups()[1]
            if data == []:
                return # unexpected EOF
            val = data.pop(0).split(',')[1]

            self._send(event_type, key, val, tags + ['namespace:%s' % ns] )

    def _process_data(self, fp, event_type, required_keys=[], tags={}):
        d = dict(x.split('=', 1) for x in fp.readline().rstrip().split(';'))
        if required_keys:
            required_data = {k: d[k] for k in required_keys if k in d}
        else:
            required_data = d

        for key, value in required_data.items():
            self._send(event_type, key, value, tags)

    def _send(self, event_type, key, val, tags={}):
        datatype = 'event'

        if re.match('^{(.+)}-^[-]+-hist',key):
            return # skip histogram configuration

        if key == 'cluster_key':
            val = str(int(val, 16))

        if val.isdigit():
            datatype = 'gauge'
        elif val.lower() in ('true', 'on', 'enable', 'enabled'): # boolean : true
            val = 1
            datatype = 'gauge'
        elif val.lower() in ('false', 'off', 'disable', 'disabled'): # boolean : false
            val = 0
            datatype = 'gauge'
        else:
            try:
                float(val)
                datatype = 'gauge'
            except ValueError:
                datatype = 'event'

        if datatype == 'gauge':
            self.gauge(self._make_key(event_type, key), val, tags=tags)
        #else:
        #    self.event({
        #        'timestamp': int(time.time()),
        #        'event_type': self._make_key(event_type, key),
        #        'aggregation_key': 'text-metrics',
        #        'msg_title': key,
        #        'msg_text': val,
        #        'tags': tags
        #    })

    @staticmethod
    def _make_key(event_type, n):
        return '%s.%s' % (event_type, n.replace('-', '_'))
