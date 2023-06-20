# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

from datadog_checks.base import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'gnatsd'


class GnatsdConfig:
    def __init__(self, instance):
        self.instance = instance
        self.host = instance.get('host', '')
        self.port = int(instance.get('port', 8222))
        self.url = '{}:{}'.format(self.host, self.port)
        self.server_name = instance.get('server_name', '')
        self.tags = instance.get('tags', [])


class GnatsdCheckInvocation:
    SERVICE_CHECK_NAME = 'gnatsd.can_connect'

    METRICS = {
        'varz': {
            'connections': 'gauge',
            'subscriptions': 'gauge',
            'slow_consumers': 'count',
            'remotes': 'gauge',
            'routes': 'gauge',
            'in_msgs': 'count',
            'out_msgs': 'count',
            'in_bytes': 'count',
            'out_bytes': 'count',
            'mem': 'gauge',
        },
        'connz': {
            'num_connections': 'gauge',
            'total': 'count',
            'connections': {
                'pending_bytes': 'gauge',
                'in_msgs': 'count',
                'out_msgs': 'count',
                'subscriptions': 'gauge',
                'in_bytes': 'count',
                'out_bytes': 'count',
            },
        },
        'routez': {
            'num_routes': 'gauge',
            'routes': {
                'pending_size': 'gauge',
                'in_msgs': 'count',
                'out_msgs': 'count',
                'subscriptions': 'gauge',
                'in_bytes': 'count',
                'out_bytes': 'count',
            },
        },
    }

    TAGS = {
        'varz': ['server_id'],
        'connz.connections': ['cid', 'ip', 'name', 'lang', 'version'],
        'routez.routes': ['rid', 'remote_id', 'ip'],
    }

    def __init__(self, instance, checker):
        self.instance = instance
        self.checker = checker
        self.config = GnatsdConfig(instance)
        self.tags = self.config.tags + ['server_name:%s' % self.config.server_name]
        self.service_check_tags = self.tags + ['url:%s' % self.config.host]

    def check(self):
        # Confirm monitor endpoint is available
        self._status_check()

        # Gather NATS metrics
        for endpoint, metrics in self.METRICS.items():
            self._check_endpoint(endpoint, metrics)

    def _status_check(self):
        try:
            response = self.checker.http.get(self.config.url)

            if response.status_code == 200:
                self.checker.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=self.service_check_tags)
            else:
                raise ValueError('Non 200 response from NATS monitor port')
        except Exception as e:
            msg = "Unable to fetch NATS stats: %s" % str(e)
            self.checker.service_check(
                self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=msg, tags=self.service_check_tags
            )
            raise e

    def _check_endpoint(self, endpoint, metrics):
        data = self.checker.http.get('{}/{}'.format(self.config.url, endpoint)).json()
        self._track_metrics(endpoint, metrics, data)

    def _track_metrics(self, namespace, metrics, data, tags=None):
        if not tags:
            tags = self._metric_tags(namespace, data)

        for mname, mtype in metrics.items():
            path = '{}.{}'.format(namespace, mname)

            if isinstance(mtype, dict):
                for instance in data.get(mname, []):
                    if 'routez' in namespace:
                        # . is not a valid character in identifiers so replace it in IP addresses with _
                        title = str(instance.get('ip')).replace('.', '_')
                    else:
                        title = str(instance.get('name') or 'unnamed')

                    self._track_metrics(
                        '{}.{}'.format(path, title), mtype, instance, tags=self._metric_tags(path, instance)
                    )
            else:
                if mtype == 'count':
                    mid = str(data.get('cid') or data.get('rid') or '')
                    metric = self._count_delta('{}.{}'.format(path, mid), data[mname])
                else:
                    metric = data[mname]

                # Send metric to Datadog
                getattr(self.checker, mtype)('gnatsd.{}'.format(path), metric, tags=tags)

    def _metric_tags(self, endpoint, data):
        tags = self.tags[:]
        if endpoint in self.TAGS:
            for tag in self.TAGS[endpoint]:
                if tag in data:
                    tags.append('gnatsd-{}:{}'.format(tag, data[tag]))
        return tags

    def _count_delta(self, count_id, current_value):
        self.checker.counts.setdefault(count_id, 0)
        delta = current_value - self.checker.counts[count_id]
        self.checker.counts[count_id] = current_value

        return delta


class GnatsdCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(GnatsdCheck, self).__init__(name, init_config, instances)
        self.counts = {}

    def check(self, instance):
        GnatsdCheckInvocation(instance, self).check()
