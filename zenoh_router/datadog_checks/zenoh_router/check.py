#!/usr/bin/python3

import time
from collections import defaultdict

from datadog_checks.base import AgentCheck  # noqa: F401


class ZenohRouterCheck(AgentCheck):
    __NAMESPACE__ = 'zenoh.router'

    __PREFIX = '@/router/'
    __RID_LEN = 32

    def __init__(self, name, init_config, instances):
        super(ZenohRouterCheck, self).__init__(name, init_config, instances)

        self.__cache = defaultdict(lambda: {'metrics': {}, 'timestamp': time.time()})

    def __parse_stats(self, stats):
        res = {}
        for name, val in stats.items():
            if isinstance(val, dict):
                for space, space_val in val.items():
                    res[(name, space)] = space_val
            else:
                res[(name, '')] = val
        return res

    def __map_to_ddtags(self, m):
        return [k + ':' + v for k, v in m.items()]

    def __process_stats(self, stats, tags, rid):
        cached_values = self.__cache.get(rid)

        timestamp = time.time()
        elapsed_seconds = timestamp - self.__cache[rid]['timestamp']
        self.__cache[rid]['timestamp'] = timestamp

        val = self.__parse_stats(stats)
        for k, v in val.items():
            v = float(v)
            if cached_values is not None and k in cached_values['metrics']:
                d = (v - cached_values['metrics'][k]) / elapsed_seconds
                if d < 0:
                    d = 0
                name, space = k
                tags['space'] = space
                self.gauge(name, d, tags=self.__map_to_ddtags(tags))
            self.__cache[rid]['metrics'][k] = v

    def __tags_by_config(self, value):
        # fmt: off
        return {
            'zid': value['zid'],
            'name': value['metadata']['name'],
            'zenoh_version': value['metadata']['zenoh_version']
        }
        # fmt: on

    def __process_peers(self, value, tags):
        peer_counts = defaultdict(lambda: 0)
        for s in value:
            peer_counts[s['whatami']] += 1

        for k, v in peer_counts.items():
            tags['whatami'] = k
            self.count('sessions', v, tags=self.__map_to_ddtags(tags))

    def check(self, instance):
        url = instance.get('url')
        try:
            response = self.http.get(url + '/' + self.__PREFIX + '*?_stats=true')
            response.raise_for_status()
            data = response.json()

            for item in data:
                k = item['key'][len(self.__PREFIX) :]
                rid = k[: self.__RID_LEN]
                value = item['value']
                gtags = self.__tags_by_config(value)
                self.__process_stats(value['stats'], gtags.copy(), rid)
                self.__process_peers(value['sessions'], gtags.copy())

            self.service_check('can_connect', AgentCheck.OK)

        except Exception as e:
            self.service_check('can_connect', AgentCheck.CRITICAL, message=str(e))
