import sys
from datetime import datetime, timedelta

import requests  # SKIP_HTTP_VALIDATION
from requests.auth import HTTPBasicAuth

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException

EVENT_TYPE = SOURCE_TYPE_NAME = 'redisenterprise'


class RedisenterpriseCheck(AgentCheck):
    """RedisenterpriseCheck attempts to connect to the cluster and ensure the node is the master node"""

    # Here we need to change the default configuration on the http wrapper
    # This can still be overwritten if necessary in the configuration file to ensure valid TLS certs
    HTTP_CONFIG_REMAPPER = {
        'tls_verify': {'name': 'tls_verify', 'default': False},
        'tls_ignore_warning': {'name': 'tls_ignore_warning', 'default': True},
    }

    def __init__(self, name, init_config, instances):
        super(RedisenterpriseCheck, self).__init__(name, init_config, instances)
        # Set this to two minutes ago which may cause duplicates but we need to get everything in the case of failover
        self.last_event_timestamp_seen = datetime.utcnow() - timedelta(0, 120)

    def _timestamp(self, date):
        """Allows us to return an epoch time stamp if we use python2 or python3"""
        if sys.version_info[0] < 3 or sys.version_info[1] < 4:
            import time

            return int(time.mktime(date.timetuple()))
        else:
            return int(date.timestamp())

    def check(self, instance):
        host = self.instance.get('host')
        timeout = self.instance.get('timeout')
        port = self.instance.get('port', 9443)
        username = self.instance.get('username')
        password = self.instance.get('password')
        event_limit = self.instance.get('event_limit', 100)
        is_mock = self.instance.get('is_mock', False)
        service_check_tags = self.instance.get('tags', [])

        if not host:
            raise ConfigurationError(
                'Configuration Error: host is not set in redisenterprise.d/conf.yaml',
            )

        try:

            # check everything if we are the cluster master
            if self._check_not_follower(host, port, username, password, timeout, is_mock):

                # add the cluster FQDN to the tags
                fqdn = self._get_fqdn(host, port, service_check_tags)
                service_check_tags.append('redis_cluster:{}'.format(fqdn))

                # collect the license data
                self._get_license(host, port, service_check_tags)

                # collect the node data
                self._get_nodes(host, port, service_check_tags)

                # grab the DBD ID to name mapping
                bdb_dict = self._get_bdb_dict(host, port, service_check_tags)
                self._get_bdb_stats(host, port, bdb_dict, service_check_tags)
                self._shard_usage(bdb_dict, service_check_tags, host)

                # collect the events from the API - we set the timeout higher here
                self._get_events(host, port, username, password, bdb_dict, service_check_tags, event_limit)

                # update the timestamp if everything else passes
                self.last_timestamp_seen = datetime.utcnow()

                # Only run the service check if we are master
                self.service_check(
                    'redisenterprise.running',
                    self._get_version(host, port, service_check_tags),
                    tags=service_check_tags,
                )

            self.last_timestamp_seen = datetime.utcnow()

        except Exception as e:
            # if we have issues we want to know when not running in mock
            if not is_mock:
                self.service_check('redisenterprise.running', self.CRITICAL, message=str(e), tags=service_check_tags)
                raise CheckException(e)

        pass

    def _check_not_follower(self, host, port, username, password, timeout, is_mock):
        """The RedisEnterprise returns a 307 if a node is a cluster follower (not leader)"""
        if is_mock:
            return False

        # We are using requests specifically because we do not want to follow redirects
        r = requests.get(
            'https://{}:{}/v1/cluster'.format(host, port),
            auth=HTTPBasicAuth(username, password),
            headers={'Content-Type': 'application/json'},
            allow_redirects=False,
            verify=False,
        )

        if r.status_code != 307:
            return True
        return False

    def _api_fetch_json(self, endpoint, service_check_tags, params=None):
        host = self.instance.get('host')
        port = self.instance.get('port')
        """ Get a Python dictionary back from a Redis Enterprise endpoint """
        headers_sent = {'Content-Type': 'application/json'}
        url = 'https://{}:{}/v1/{}'.format(host, port, endpoint)
        r = self.http.get(url, extra_headers=headers_sent)
        if r.status_code != 200:
            msg = "unexpected status of {0} when fetching stats, response: {1}"
            msg = msg.format(r.status_code, r.text)
            r.raise_for_status()
        info = r.json()
        return info

    def _get_fqdn(self, host, port, service_check_tags):
        """Get the cluster FQDN back from the endpoints"""
        try:
            info = self._api_fetch_json("cluster", service_check_tags)
            fqdn = info.get('name')
            if fqdn:
                return fqdn
            return "unknown"
        except Exception:
            return "unknown"

    def _get_version(self, host, port, service_check_tags):
        info = self._api_fetch_json("bootstrap", service_check_tags)
        version = info.get('local_node_info').get('software_version')
        if version:
            return self.OK
        return self.CRITICAL

    def _get_bdb_dict(self, host, port, service_check_tags):
        bdb_dict = {}
        bdbs = self._api_fetch_json("bdbs", service_check_tags)
        for i in bdbs:

            # collect the number of shards and multiply by 2 if replicated
            shards_used = i['shards_count']
            if i['replication']:
                shards_used = shards_used * 2

            bdb_dict[i['uid']] = {
                'name': i['name'],
                'limit': i['memory_size'],
                'shards_used': shards_used,
                'endpoints': len(i['endpoints'][-1]['addr']),
            }
        return bdb_dict

    def _get_events(self, host, port, username, password, bdb_dict, service_check_tags, event_limit):
        """ Scrape the LOG endpoint and put all log entries into Datadog events """

        # We need to use requests to send the get params since the http wrapper does not allow this
        r = requests.get(
            'https://{}:{}/v1/logs'.format(host, port),
            auth=HTTPBasicAuth(username, password),
            headers={'Content-Type': 'application/json'},
            allow_redirects=False,
            verify=False,
            params={
                "stime": self.last_event_timestamp_seen.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "order": "desc",
                "limit": event_limit,
            },
        )
        if r.status_code != 200:
            msg = 'RedisEnterprise: Unable to fetch logs from endpoint: HTTP Status {}'.format(r.status_code)
            self.log.info(msg)

        evnts = r.json()

        for evnt in evnts:
            msg = {k: v for k, v in evnt.items() if k not in ['time', 'severity']}
            self.event(
                {
                    "timestamp": self._timestamp(datetime.strptime(evnt['time'], "%Y-%m-%dT%H:%M:%SZ")),
                    "event_type": EVENT_TYPE,
                    "msg_title": evnt['type'],
                    "msg_text": ", ".join(["=".join([key, str(val)]) for key, val in msg.items()]),
                    "alert_type": evnt['severity'].lower(),
                    "source_type_name": SOURCE_TYPE_NAME,
                    "host": host,
                    "tags": service_check_tags,
                }
            )

            # Be sure to add 1 second to the last event so we don't pick it up again
            ts = datetime.strptime(evnt['time'], "%Y-%m-%dT%H:%M:%SZ")
            if ts > self.last_event_timestamp_seen:
                self.last_event_timestamp_seen = ts + timedelta(0, 1)

    def _get_bdb_stats(self, host, port, bdb_dict, service_check_tags):
        """Collect Enterprise database related stats"""
        gauges = [
            'avg_latency',
            'avg_latency_max',
            'avg_other_latency',
            'avg_read_latency',
            'avg_write_latency',
            'conns',
            'egress_bytes',
            'evicted_objects',
            'expired_objects',
            'fork_cpu_system',
            'ingress_bytes',
            'listener_acc_latency',
            'main_thread_cpu_system',
            'main_thread_cpu_system_max',
            'memory_limit',
            'no_of_keys',
            'other_req',
            'read_hits',
            'read_misses',
            'read_req',
            'shard_cpu_system',
            'shard_cpu_system_max',
            'total_req',
            'total_req_max',
            'used_memory',
            'write_hits',
            'write_misses',
            'write_req',
            'bigstore_objs_ram',
            'bigstore_objs_flash',
            'bigstore_io_reads',
            'bigstore_io_writes',
            'bigstore_throughput',
            'big_write_ram',
            'big_write_flash',
            'big_del_ram',
            'big_del_flash',
        ]

        # If there are no databases created the following link will 404, so we need to handle this
        try:
            stats = self._api_fetch_json("bdbs/stats/last", service_check_tags)
        except Exception as e:
            if e.response.status_code == 404:
                self.gauge('redisenterprise.database_count', 0, tags=service_check_tags, hostname=host)
                return 0
            else:
                raise e
        self.gauge('redisenterprise.database_count', len(stats), tags=service_check_tags, hostname=host)
        for i in stats:
            tgs = []
            tgs.append('database:{}'.format(bdb_dict[int(i)]['name']))
            # add the stats only available from the bdb_dict
            self.gauge(
                'redisenterprise.endpoints', bdb_dict[int(i)]['endpoints'], tags=tgs + service_check_tags, hostname=host
            )
            self.gauge(
                'redisenterprise.memory_limit',
                bdb_dict[int(i)]['limit'],
                tags=tgs + service_check_tags,
                hostname=host,
            )
            # derive our own stats from others
            self.gauge(
                'redisenterprise.used_memory_percent',
                100 * stats[i]['used_memory'] / bdb_dict[int(i)]['limit'],
                tags=tgs + service_check_tags,
                hostname=host,
            )
            # derive our cache hit rate - be sure not to divide by 0
            if (
                stats[i]['read_hits'] + stats[i]['read_misses'] + stats[i]['write_hits'] + stats[i]['write_misses']
            ) == 0:
                self.gauge(
                    'redisenterprise.cache_hit_rate',
                    0.0,
                    tags=tgs + service_check_tags,
                    hostname=host,
                )
            else:
                self.gauge(
                    'redisenterprise.cache_hit_rate',
                    100
                    * (stats[i]['read_hits'] + stats[i]['write_hits'])
                    / (
                        stats[i]['read_hits']
                        + stats[i]['read_misses']
                        + stats[i]['write_hits']
                        + stats[i]['write_misses']
                    ),
                    tags=tgs + service_check_tags,
                    hostname=host,
                )
            # derive flash object percentage being sure that the key exists and is not 0
            if 'bigstore_objs_flash' in stats[i].keys():
                if stats[i]['bigstore_objs_flash'] > 0:
                    self.gauge(
                        'redisenterprise.bigstore_objs_percent',
                        100
                        * stats[i]['bigstore_objs_ram']
                        / (stats[i]['bigstore_objs_ram'] + stats[i]['bigstore_objs_flash']),
                        tags=tgs + service_check_tags,
                    )

            for j in stats[i].keys():
                if j in gauges:
                    self.gauge('redisenterprise.{}'.format(j), stats[i][j], tags=tgs + service_check_tags)
        return 0

    def _get_license(self, host, port, service_check_tags):
        """Collect Enterprise License Information"""
        stats = self._api_fetch_json("license", service_check_tags)
        expire = datetime.strptime(stats['expiration_date'], "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.now()
        self.gauge('redisenterprise.license_days', (expire - now).days, tags=service_check_tags)
        self.gauge('redisenterprise.license_shards', stats['shards_limit'], tags=service_check_tags)

        # Check the time remaining on the license as a service check
        license_check = RedisenterpriseCheck.OK
        if stats['expired']:
            license_check = RedisenterpriseCheck.CRITICAL
        elif (expire - now).days < 7:
            license_check = RedisenterpriseCheck.WARNING
        self.service_check(
            'redisenterprise.license_status',
            license_check,
            tags=service_check_tags,
        )

    def _shard_usage(self, bdb_dict, service_check_tags, host):
        """Sum up the number of shards"""
        used = 0
        for x in bdb_dict.values():
            used += x['shards_used']
        self.gauge('redisenterprise.total_shards_used', used, tags=service_check_tags, hostname=host)

    def _get_nodes(self, host, port, service_check_tags):
        """Collect Enterprise Node Information"""
        stats = self._api_fetch_json("nodes", service_check_tags)
        res = {'total_node_cores': 0, 'total_node_memory': 0, 'total_node_count': 0, 'total_active_nodes': 0}

        for i in stats:
            res['total_node_cores'] += i['cores']
            res['total_node_memory'] += i['total_memory']
            res['total_node_count'] += 1
            if i['status'] == "active":
                res['total_active_nodes'] += 1

        for x in res.keys():
            self.gauge('redisenterprise.{}'.format(x), res[x], tags=service_check_tags, hostname=host)
