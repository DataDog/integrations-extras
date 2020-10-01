import time
from collections import defaultdict

import redis

from datadog_checks.base import AgentCheck, ConfigurationError

EVENT_TYPE = SOURCE_TYPE_NAME = 'redis_sentinel'


class RedisSentinelCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
        self._masters = defaultdict(lambda: "")

    def _load_config(self, instance):
        host = instance.get('sentinel_host')
        port = instance.get('sentinel_port')

        if not host or not port:
            raise ConfigurationError('Configuration error, please fix redis_sentinel configuration')

        if not isinstance(port, int):
            raise ConfigurationError('Configuration error. "sentinel_port" must be an int.')

        passwd = instance.get('sentinel_password', None)

        return host, port, passwd

    def check(self, instance):
        self.log.info(instance)

        host, port, password = self._load_config(instance)

        redis_conn = redis.StrictRedis(host=host, port=port, password=password, db=0)

        for master_name in instance['masters']:
            base_tags = ['redis_name:%s' % master_name] + instance.get('tags', [])
            try:
                self._process_instance_master(redis_conn, master_name, base_tags)
            except Exception as e:
                self.warning("Error collecting metrics for master %s: %s", master_name, e)

    def _process_instance_master(self, redis_conn, master_name, base_tags):
        master_tags = self._process_master_stats(redis_conn, master_name, base_tags)
        self._process_slaves_stats(redis_conn, master_name, base_tags, master_tags)
        self._process_sentinels_stats(redis_conn, master_name, base_tags, master_tags)

    def _process_sentinels_stats(self, redis_conn, master_name, base_tags, master_tags):
        """
        [{
            'down-after-milliseconds': 5000,
            'flags': 's_down,sentinel',
            'ip': '10.1.2.3',
            'is_disconnected': False,
            'is_master': False,
            'is_master_down': False,
            'is_odown': False,
            'is_sdown': True,
            'is_sentinel': True,
            'is_slave': False,
            'last-hello-message': 12345678,
            'last-ok-ping-reply': 12345678,
            'last-ping-reply': 12345679
            'last-ping-sent': 12345678,
            'name': '10.1.2.3:26379',
            'link-pending-commands': 78,
            'port': 26379,
            'runid': '123456789abcdef',
            's-down-time': 12345678,
            'voted-leader': '?',
            'voted-leader-epoch': 0,
        }]
        """
        sentinels_stats = redis_conn.sentinel_sentinels(master_name)
        # sentinel_stats returns stats for other sentinels only
        # so increment once for current sentinel
        self.increment('redis.sentinel.ok_sentinels', tags=master_tags)
        for stats in sentinels_stats:
            sentinel_tags = ['sentinel_ip:%s' % stats['ip']] + base_tags
            if stats['is_odown'] or stats['is_sdown']:  # sentinel keeps track of old sentinels
                continue
            self.increment('redis.sentinel.ok_sentinels', tags=master_tags)

            pending = stats.get('link-pending-commands', stats.get('pending-commands'))
            if pending is not None:
                self.gauge('redis.sentinel.link_pending_commands', pending, tags=['sentinel'] + sentinel_tags)

            reply = stats.get('last-ping-reply')
            sent = stats.get('last-ping-sent')
            if reply is not None and sent is not None:
                self.gauge('redis.sentinel.ping_latency', reply - sent, sentinel_tags)

            ok_reply = stats.get('last-ok-ping-reply')
            if ok_reply is not None and sent is not None:
                self.gauge('redis.sentinel.last_ok_ping_latency', reply - ok_reply, sentinel_tags)

    def _process_slaves_stats(self, redis_conn, master_name, base_tags, master_tags):
        """
        [{
            'down-after-milliseconds': 5000,
            'flags': 'slave',
            'info-refresh': 2628,
            'ip': '10.1.2.3',
            'is_disconnected': False,
            'is_master': False,
            'is_master_down': False,
            'is_odown': False,
            'is_sdown': False,
            'is_sentinel': False,
            'is_slave': True
            'last-ok-ping-reply': 429,
            'last-ping-reply': 429,
            'last-ping-sent': 0,
            'master-host': '10.1.2.3',
            'master-link-down-time': 0,
            'master-link-status': 'ok',
            'master-port': 6379,
            'name': '10.1.2.3:6379',
            'pending-commands': 0,
            'port': 6379,
            'role-reported': 'slave',
            'role-reported-time': 3124725,
            'runid': '123456789abcdef',
            'slave-priority': 100,
            'slave-repl-offset': 12345678,
        }]
        """
        slaves_stats = redis_conn.sentinel_slaves(master_name)
        slaves_odown = 0
        slaves_sdown = 0

        for stats in slaves_stats:
            # sentinel keeps track of old slaves
            if stats['is_odown']:
                slaves_odown += 1
                continue
            elif stats['is_sdown']:
                slaves_sdown += 1
                continue

            self.increment('redis.sentinel.ok_slaves', tags=master_tags)
            slave_tags = ['slave_ip:%s' % stats['ip']] + base_tags

            pending = stats.get('link-pending-commands', stats.get('pending-commands'))
            if pending is not None:
                self.gauge('redis.sentinel.link_pending_commands', pending, tags=['slave'] + slave_tags)

            self.service_check(
                'redis.sentinel.slave_is_disconnected',
                AgentCheck.CRITICAL if stats['is_disconnected'] else AgentCheck.OK,
                tags=slave_tags,
            )
            self.service_check(
                'redis.sentinel.slave_master_link_down',
                AgentCheck.CRITICAL if stats['master-link-status'] != 'ok' else AgentCheck.OK,
                tags=slave_tags,
            )

        self.gauge('redis.sentinel.odown_slaves', slaves_odown, tags=master_tags)
        self.gauge('redis.sentinel.sdown_slaves', slaves_sdown, tags=master_tags)

    def _process_master_stats(self, redis_conn, master_name, base_tags):
        """
        {
            'config-epoch': 94,
            'down-after-milliseconds': 5000,
            'failover-timeout': 60000,
            'flags': 'master',
            'info-refresh': 1234,
            'ip': '10.1.2.3',
            'is_disconnected': False,
            'is_master': True,
            'is_master_down': False,
            'is_odown': False,
            'is_sdown': False,
            'is_sentinel': False,
            'is_slave': False,
            'last-ok-ping-reply': 49,
            'last-ping-reply': 49,
            'last-ping-sent': 0,
            'name': 'delancie-backend',
            'num-other-sentinels': 4
            'num-slaves': 3,
            'parallel-syncs': 10,
            'pending-commands': 0,
            'port': 6379,
            'quorum': 2,
            'role-reported': 'master',
            'role-reported-time': 12345678,
            'runid': '123456789abcdef',
        }
        """
        stats = redis_conn.sentinel_master(master_name)
        master_tags = ['master_ip:%s' % stats['ip']] + base_tags

        pending = stats.get('link-pending-commands', stats.get('pending-commands'))
        if pending is not None:
            self.gauge('redis.sentinel.link_pending_commands', pending, tags=['master'] + master_tags)

        known_slaves = stats.get('num-slaves')
        if known_slaves is not None:
            self.gauge('redis.sentinel.known_slaves', known_slaves, tags=master_tags)

        known_sentinels = stats.get('num-other-sentinels')
        if known_slaves is not None:
            self.gauge('redis.sentinel.known_sentinels', known_sentinels + 1, tags=master_tags)

        self.service_check(
            'redis.sentinel.master_is_disconnected',
            AgentCheck.CRITICAL if stats.get('is_disconnected') else AgentCheck.OK,
            tags=master_tags,
        )

        self.service_check(
            'redis.sentinel.master_is_down',
            AgentCheck.CRITICAL if stats.get('is_master_down') else AgentCheck.OK,
            tags=master_tags,
        )

        if self._masters[master_name] != stats['ip']:
            if self._masters[master_name] != "":  # avoid check initialization
                self.increment('redis.sentinel.failover', tags=base_tags)
                self.event(
                    {
                        'timestamp': int(time.time()),
                        'event_type': EVENT_TYPE,
                        'msg_title': '%s failover from %s to %s'
                        % (master_name, self._masters[master_name], stats['ip']),
                        'alert_type': 'info',
                        "source_type_name": SOURCE_TYPE_NAME,
                        "event_object": master_name,
                        "tags": base_tags,
                    }
                )

            self._masters[master_name] = stats['ip']

        return master_tags
