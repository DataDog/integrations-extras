import re

from datadog_checks.base import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'stardog'


def convert_value(in_key, in_val, db_name):
    key = "stardog.%s" % in_key
    val = in_val['value']
    return {key: val}


def convert_count(in_key, in_val, dn_name):
    key = "stardog.%s" % in_key
    val = in_val['count']
    return {key: val}


def convert_query_speed(in_key, in_val, dn_name):
    try:
        if in_val['duration_units'] != 'seconds':
            raise Exception('Unsupported duration units')
        if in_val['rate_units'] != 'calls/second':
            raise Exception('Unsupported rate units')
    except KeyError:
        raise Exception('The units are not properly defined')

    entry_key = [
        "count",
        "max",
        "mean",
        "min",
        "p50",
        "p75",
        "p95",
        "p98",
        "p99",
        "p999",
        "stddev",
        "m15_rate",
        "m1_rate",
        "m5_rate",
        "mean_rate",
    ]
    out_dict = {}
    for ent in entry_key:
        new_key = "stardog.%s.%s" % (in_key, ent)
        out_dict[new_key] = in_val[ent]
    return out_dict


def convert_db_specific(in_key, in_val, dn_name, func):
    key = in_key.replace("%s." % dn_name, '')
    return func(key, in_val, dn_name)


def convert_count_db(in_key, in_val, dn_name):
    return convert_db_specific(in_key, in_val, dn_name, convert_count)


def convert_query_speed_db(in_key, in_val, dn_name):
    return convert_db_specific(in_key, in_val, dn_name, convert_query_speed)


_g_metrics_map = {
    'dbms.mem.mapped.max': convert_value,
    'dbms.memory.heap.reserve': convert_value,
    'dbms.mem.direct.pool.used': convert_value,
    'dbms.mem.mapped.used': convert_value,
    'dbms.mem.heap.used': convert_value,
    'dbms.memory.direct.reserve': convert_value,
    'dbms.mem.direct.max': convert_value,
    'dbms.page.cache.size': convert_value,
    'system.cpu.usage': convert_value,
    'dbms.mem.heap.max': convert_value,
    'dbms.mem.direct.buffer.used': convert_value,
    'dbms.mem.direct.buffer.max': convert_value,
    'databases.system.planCache.ratio': convert_value,
    'databases.system.planCache.size': convert_value,
    'system.uptime': convert_value,
    'dbms.memory.managed.heap': convert_value,
    'dbms.mem.direct.pool.max': convert_value,
    'dbms.mem.direct.used': convert_value,
    'dbms.memory.managed.direct': convert_value,
}


_g_bd_specific_map = {
    r'databases\.(.*).txns.openTransactions': convert_count_db,
    r'databases\.(.*).txns.speed': convert_query_speed_db,
    r'databases\.(.*).queries.running': convert_count_db,
    r'databases\.(.*).queries.speed': convert_query_speed_db,
    r'databases\.(.*).openConnections': convert_count_db,
}


class StardogCheck(AgentCheck):
    def _process_doc(self, doc, metrics, tags, add_db_tags=False):
        for k in doc:
            # find match
            for regex in metrics:
                p = re.compile(regex)
                m = p.match(k)
                if m is not None:
                    convert_func = metrics[regex]
                    local_tags = tags[:]
                    db_name = None
                    if add_db_tags:
                        try:
                            db_name = m.group(1)
                            local_tags.append("database:%s" % db_name)
                        except Exception:
                            self.log.warning("No database name was found")
                    values_map = convert_func(k, doc[k], db_name)
                    for report_key in values_map:
                        self.log.debug("Sending %s=%s to Datadog", report_key, values_map[report_key])
                        self.gauge(report_key, values_map[report_key], tags=local_tags)
                    break

    def check(self, _):
        try:
            response = self.http.get(self.instance['stardog_url'] + '/admin/status')
        except KeyError:
            raise Exception('The Stardog check instance is not properly configured')

        if response.status_code != 200:
            response.raise_for_status()
        json_doc = response.json()
        try:
            tags = self.instance['tags']
            if type(tags) != list:
                self.log.warning('The tags list in the Stardog check is not configured properly')
                tags = []
        except KeyError:
            tags = []

        tags.append("stardog_url:%s" % self.instance['stardog_url'])
        self._process_doc(json_doc, _g_metrics_map, tags)
        self._process_doc(json_doc, _g_bd_specific_map, tags, add_db_tags=True)
