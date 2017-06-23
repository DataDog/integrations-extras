# Aerospike agent check for Datadog Agent.
# Copyright (C) 2015 Pippio, Inc. All rights reserved.

# stdlib
import socket
from contextlib import closing
from collections import namedtuple

# project
from checks import AgentCheck

SOURCE_TYPE_NAME = 'aerospike'
SERVICE_CHECK_NAME = '%s.cluster_up' % SOURCE_TYPE_NAME
CLUSTER_EVENT_TYPE = SOURCE_TYPE_NAME
NAMESPACE_EVENT_TYPE = '%s.namespace' % SOURCE_TYPE_NAME

Addr = namedtuple('Addr', ['host', 'port'])

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

                for ns in self._get_namespaces(conn, fp, required_namespaces):
                    conn.send('namespace/%s\r' % ns)
                    self._process_data(fp, NAMESPACE_EVENT_TYPE, namespace_metrics, tags|{'namespace:%s' % ns})

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
        tags = set(instance.get('tags', []))

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

    def _process_data(self, fp, event_type, required_keys=[], tags={}):
        d = dict(x.split('=', 1) for x in fp.readline().rstrip().split(';'))
        if required_keys:
            required_data = {k: d[k] for k in required_keys if k in d}
        else:
            required_data = d

        for key, value in required_data.items():
            self._process_datum(event_type, key, value, tags)

    def _process_datum(self, event_type, key, val, tags={}):
        if val.isdigit():
            self.gauge(self._make_key(event_type, key), val, tags=tags)

    @staticmethod
    def _make_key(event_type, n):
        return '%s.%s' % (event_type, n.replace('-', '_'))
