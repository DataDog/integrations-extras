# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import requests

# stdlib

# 3rd party

# project
from checks import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'gnatsd_streaming'

class GnatsdStreamingCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
        self.counts = {}

    def check(self, instance):
        self.InstanceCheck(instance, self).check()

    class InstanceCheck:
        SERVICE_CHECK_NAME = 'gnatsd_streaming.can_connect'

        METRICS = {
            'serverz': {
                'clients': 'gauge',
                'subscriptions': 'count',
                'channels': 'gauge',
                'total_msgs': 'count',
                'total_bytes': 'count',
            },
            'storez': {
                'total_msgs': 'count',
                'total_bytes': 'count',
            },
            'clientsz': {
                'total': 'gauge',
            },
            'channelsz': {
                'total': 'gauge',
                'channels': {
                    'msgs': 'count',
                    'bytes': 'count'
                }
            }
        }

        TAGS = {
            'serverz': ['cluster_id','server_id','version','go'],
            'storez': ['cluster_id','server_id'],
            'clientsz': ['cluster_id','server_id'],
            'channelsz': ['cluster_id','server_id'],
        }

        def __init__(self, instance, checker):
            self.instance = instance
            self.checker = checker
            self.config = self.Config(instance)
            self.tags = self.config.tags + ['server_name:%s' % self.config.server_name]
            self.service_check_tags = self.tags + ['url:%s' % self.config.host]

        def check(self):
            # Confirm monitor endpoint is available
            self._status_check()

            # Gather NATS Streaming metrics
            for endpoint, metrics in self.METRICS.items():
                self._check_endpoint(endpoint, metrics)

        def _status_check(self):
            try:
                response = requests.get(self.config.url)

                if response.status_code == 200:
                    self.checker.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=self.service_check_tags)
                else:
                    raise ValueError('Non 200 response from NATS monitor port')
            except Exception as e:
                msg = "Unable to fetch NATS Streaming stats: %s" % str(e)
                self.checker.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=msg, tags=self.service_check_tags)
                raise e

        def _check_endpoint(self, endpoint, metrics, pagination={}):
            params = self._params(endpoint)
            params.update(pagination)

            data = requests.get(self.config.url + '/' + endpoint, params).json()
            self._track_metrics(endpoint, metrics, data)

            if data.get('count', 0) > 0:
                offset = data.get('offset') + data.get('limit')
                self._check_endpoint(endpoint, metrics, pagination={'offset': offset})

        def _track_metrics(self, namespace, metrics, data, tags={}):
            if not tags:
                tags = self._metric_tags(namespace, data)

            for mname, mtype in metrics.items():
                path = namespace + '.' + mname

                if type(mtype) is dict:
                    for instance in data.get(mname, []):
                        title = str(instance.get('name')) if 'channels' in namespace else ''
                        self._track_metrics(path + '.' + title.replace(".","_"), mtype, instance, tags=self._metric_tags(path, instance))
                else:
                    if mtype == 'count':
                        metric = self._count_delta(path, data[mname])
                    else:
                        metric = data[mname]

                    # Send metric to Datadog
                    getattr(self.checker, mtype)('gnatsd.streaming.' + path, metric, tags=tags)

        def _params(self, endpoint):
            return {
                'channelsz': {
                    'subs': 1,
                    'limit': self.config.pagination_limit
                }
            }.get(endpoint, {})

        def _metric_tags(self, endpoint, data):
            tags = []
            if endpoint in self.TAGS:
                for tag in self.TAGS[endpoint]:
                    if tag in data:
                        tags.append('nss-' + tag + ':' + str(data[tag]))
            return self.tags + tags

        def _count_delta(self, count_id, current_value):
            self.checker.counts.setdefault(count_id, 0)
            delta = current_value - self.checker.counts[count_id]
            self.checker.counts[count_id] = current_value

            return delta

        class Config:
            def __init__(self, instance):
                self.instance = instance
                self.host = instance.get('host', '')
                self.port = int(instance.get('port', 8222))
                self.url = self.host + ':' + str(self.port) + '/streaming'
                self.server_name = instance.get('server_name', '')
                self.pagination_limit = instance.get('pagination_limit', 1024)
                self.tags = instance.get('tags', [])
