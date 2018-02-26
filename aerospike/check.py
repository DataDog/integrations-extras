# Aerospike agent check for Datadog Agent.
# Original work Copyright (C) 2015 Pippio, Inc. All rights reserved.
# Modified work Copyright (C) 2017 Red Sift
# Modified work Copyright (C) 2018 Aerospike, Inc.

# (C) Datadog, Inc. 2010-2018
# All rights reserved
# This software may be modified and distributed under the terms
# of the BSD-3 license. See the LICENSE file for details.


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
CLUSTER_METRIC_TYPE = SOURCE_TYPE_NAME
NAMESPACE_METRIC_TYPE = '%s.namespace' % SOURCE_TYPE_NAME
NAMESPACE_TPS_METRIC_TYPE = '%s.namespace.tps' % SOURCE_TYPE_NAME
SINDEX_METRIC_TYPE = '%s.sindex' % SOURCE_TYPE_NAME
SET_METRIC_TYPE = '%s.set' % SOURCE_TYPE_NAME

Addr = namedtuple('Addr', ['host', 'port'])

def parse_namespace(data, namespace, secondary):
    idxs = []
    while data != []:
        l = data.pop(0)

        # $ asinfo -v 'sindex/phobos_sindex'
        # ns=phobos_sindex:set=longevity:indexname=str_100_idx:num_bins=1:bins=str_100_bin:type=TEXT:sync_state=synced:state=RW; \
        # ns=phobos_sindex:set=longevity:indexname=str_uniq_idx:num_bins=1:bins=str_uniq_bin:type=TEXT:sync_state=synced:state=RW; \
        # ns=phobos_sindex:set=longevity:indexname=int_uniq_idx:num_bins=1:bins=int_uniq_bin:type=INT SIGNED:sync_state=synced:state=RW;

        # $ asinfo -v 'sets/bar'
        # ns=bar:set=demo:objects=1:tombstones=0:memory_data_bytes=34:truncate_lut=0:stop-writes-count=0:set-enable-xdr=use-default:disable-eviction=false;\
        # ns=bar:set=demo2:objects=123456:tombstones=0:memory_data_bytes=8518464:truncate_lut=0:stop-writes-count=0:set-enable-xdr=use-default:disable-eviction=false

        match = re.match('^ns=%s:([^:]+:)?%s=([^:]+):.*$' % (namespace, secondary), l)
        if match == None:
            continue
        idxs.append(match.groups()[1])

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
                self._process_data(fp, CLUSTER_METRIC_TYPE, metrics, tags=tags)

                namespaces = self._get_namespaces(conn, fp, required_namespaces)

                for ns in namespaces:
                    conn.send('namespace/%s\r' % ns)
                    self._process_data(fp, NAMESPACE_METRIC_TYPE, namespace_metrics, tags+['namespace:%s' % ns])

                    conn.send('sindex/%s\r' % ns)
                    for idx in parse_namespace(fp.readline().split(';')[:-1], ns,'indexname'):
                        conn.send('sindex/%s/%s\r' % (ns,idx))
                        self._process_data(fp, SINDEX_METRIC_TYPE, [], 
                                tags+['namespace:%s' % ns, 'sindex:%s.%s' % (ns,idx)])
                    
                    conn.send('sets/%s\r' % ns)
                    for s in parse_namespace(fp.readline().split(';'),ns,'set'):
                        conn.send('sets/%s/%s\r' % (ns,s))
                        self._process_data(fp, SET_METRIC_TYPE, [],
                                tags+['namespace:%s' % ns, 'set:%s.%s' % (ns,s)], ':')

                conn.send('throughput:\r')
                self._process_throughput(fp.readline().rstrip().split(';'), NAMESPACE_TPS_METRIC_TYPE, namespaces, tags)

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

    def _process_throughput(self, data, metric_type, namespaces, tags={}):
        while data != []:
            l = data.pop(0)

            # skip errors
            while l.startswith('error-'):
                if data == []:
                    return
                l = data.pop(0)

            # $ asinfo -v 'throughput:'
            # {ns}-read:23:56:38-GMT,ops/sec;23:56:48,0.0;{ns}-write:23:56:38-GMT,ops/sec;23:56:48,0.0; \
            # error-no-data-yet-or-back-too-small;error-no-data-yet-or-back-too-small
            #
            # data = [ "{ns}-read..","23:56:40,0.0", "{ns}-write...","23:56:48,0.0" ... ]

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

            self._send(metric_type, key, val, tags + ['namespace:%s' % ns] )

    def _process_data(self, fp, metric_type, required_keys=[], tags={}, delim=';'):
        d = dict(x.split('=', 1) for x in fp.readline().rstrip().split(delim))
        if required_keys:
            required_data = {k: d[k] for k in required_keys if k in d}
        else:
            required_data = d

        for key, value in required_data.items():
            self._send(metric_type, key, value, tags)

    def _send(self, metric_type, key, val, tags={}):
        datatype = 'event'

        if re.match('^{(.+)}-(.*)hist-track',key):
            self.log.debug("Histogram config skipped: %s=%s",key,str(val))
            return # skip histogram configuration

        if key == 'cluster_key':
            val = str(int(val, 16))

        if val.isdigit():
            if key in self.init_config.get('mappings',[]):
                datatype='rate'
            else:
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
            self.gauge(self._make_key(metric_type, key), val, tags=tags)
        elif datatype == 'rate':
            print "self.rate %s"%key
            self.rate(self._make_key(metric_type, key), val, tags=tags)
        else:
            return # Non numeric/boolean metric, discard

    @staticmethod
    def _make_key(event_type, n):
        return '%s.%s' % (event_type, n.replace('-', '_'))
