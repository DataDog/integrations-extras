#!/usr/bin/python3

import re
import time
from collections import defaultdict

from datadog_checks.base import AgentCheck  # noqa: F401


class ZenohRouterCheck(AgentCheck):
    __NAMESPACE__ = 'zenoh.router'

    __URI = '/@/*/router?_stats=true'
    __RID_PATTERN = r'@/([a-f0-9]{32})/router'

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

    def __extract_rid(self, text):
        match = re.search(self.__RID_PATTERN, text)
        if match:
            return match.group(1)
        return None

    def check(self, instance):
        url = instance.get('url')
        try:
            response = self.http.get(url + self.__URI)
            response.raise_for_status()
            data = response.json()

            for item in data:
                rid = self.__extract_rid(item['key'])
                if rid is None:
                    continue
                value = item['value']
                gtags = self.__tags_by_config(value)
                self.__process_peers(value['sessions'], gtags.copy())
                if 'stats' in value:
                    self.__process_stats(value['stats'], gtags.copy(), rid)

            self.service_check('can_connect', AgentCheck.OK)

        except Exception as e:
            self.service_check('can_connect', AgentCheck.CRITICAL, message=str(e))
