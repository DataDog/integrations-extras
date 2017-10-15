# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import requests

# project
from checks import AgentCheck
from collections import defaultdict

EVENT_TYPE = SOURCE_TYPE_NAME = 'storm'


def _g(stat_map, default, func=None, *components):
    """ Helper method to return value, tag tuple from a stat map get.

    :param stat_map: stat map
    :param default: default value
    :param func: function to apply after getting the value.
    :param components: components in order to traverse
    :return: stat value
    """
    value = stat_map
    for component in components:
        if isinstance(component, (int, long)):
            if isinstance(value, (list, tuple)) and len(value) >= component:
                value = value[component]
            else:
                return default
        else:
            if component not in value:
                return default
            else:
                value = value[component]
    if value not in (None, ''):
        if func is not None:
            try:
                return func(value)
            except Exception:
                return default
        return value
    else:
        return default


def _gt(stat_map, default, tags, func=None, *components):
    """ Helper method to return value, tag tuple from a stat map get.

    :param stat_map: stat map
    :param default: default value
    :param tags: tags
    :param func: function to apply after getting the value.
    :param components: components in order to traverse
    :return: tuple of stat value and tags.
    """
    return _g(stat_map, default, func, *components), tags


def _float(v):
    """Try to convert to a float

    :param v: value
    :rtype: float
    """
    try:
        return float(v)
    except Exception:
        return 0.0


def _long(v):
    """Try to convert to a long

    :param v: value
    :rtype: long
    """
    try:
        return long(v)
    except Exception:
        return 0


class StormCheck(AgentCheck):

    nimbus_server = 'localhost:9005'
    http_prefix = 'http://'

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def get_storm_cluster_summary(self):
        url = self.http_prefix + self.nimbus_server + "/api/v1/cluster/summary"
        try:
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning("Error retrieving Storm Cluster Summary from " + url)
                return {}
            return data
        except Exception as e:
            self.log.warning("Error retrieving Storm Cluster Summary from " + url)
            self.log.exception(e)
            return {}

    def get_storm_nimbus_summary(self):
        url = self.http_prefix + self.nimbus_server + "/api/v1/nimbus/summary"
        try:
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning("Error retrieving Storm Nimbus Summary from " + url)
                return {}
            return data
        except Exception as e:
            self.log.warning("Error retrieving Storm Nimbus Summary from " + url)
            self.log.exception(e)
            return {}

    def get_storm_supervisor_summary(self):
        url = self.http_prefix + self.nimbus_server + "/api/v1/supervisor/summary"
        try:
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning("Error retrieving Storm Supervisor Summary from " + url)
                return {}
            return data
        except Exception as e:
            self.log.warning("Error retrieving Storm Supervisor Summary from " + url)
            self.log.exception(e)
            return {}

    def get_storm_topology_summary(self):
        url = self.http_prefix + self.nimbus_server + "/api/v1/topology/summary"
        try:
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning("Error retrieving Storm Topology Summary from " + url)
                return {}
            return data
        except Exception as e:
            self.log.warning("Error retrieving Storm Topology Summary from " + url)
            self.log.exception(e)
            return {}

    def get_topology_info(self, topology_id):
        url = self.http_prefix + self.nimbus_server + "/api/v1/topology/" + topology_id
        try:
            params = {'window': 60}  # set a 1 minute window
            resp = requests.get(url, params=params)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning('Topology "' + topology_id + '" returned error')
                return {}
            return data
        except Exception as e:
            self.log.warning("Error retrieving Storm Topology Info from " + url)
            self.log.exception(e)
            return {}

    def get_topology_metrics(self, topology_id):
        url = self.http_prefix + self.nimbus_server + "/api/v1/topology/" + topology_id + "/metrics"
        try:
            params = {'window': 60}  # set a 1 minute window
            resp = requests.get(url, params=params)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning('Topology "' + topology_id + '" returned error')
                return {}
            return data
        except Exception as e:
            self.log.warning("Error retrieving Storm Topology Metrics from " + url)
            self.log.exception(e)
            return {}

    def process_cluster_stats(self, environment, cluster_stats):
        if len(cluster_stats) == 0:
            return {}
        else:
            version = _g(cluster_stats, 'unknown', None, 'version').replace(' ', '_').lower()
            tags = ['#stormClusterEnvironment:{}'.format(environment), '#stormVersion:{}'.format(version)]
            return {
                # 1.0.x minimum
                'storm.cluster.executorsTotal': _gt(cluster_stats, 0, tags, _long, 'executorsTotal'),
                'storm.cluster.slotsTotal': _gt(cluster_stats, 0, tags, _long, 'slotsTotal'),
                'storm.cluster.slotsFree': _gt(cluster_stats, 0, tags, _long, 'slotsFree'),
                'storm.cluster.topologies': _gt(cluster_stats, 0, tags, _long, 'topologies'),
                'storm.cluster.supervisors': _gt(cluster_stats, 0, tags, _long, 'supervisors'),
                'storm.cluster.tasksTotal': _gt(cluster_stats, 0, tags, _long, 'tasksTotal'),
                'storm.cluster.slotsUsed': _gt(cluster_stats, 0, tags, _long, 'slotsUsed'),
                # 1.1.x additions
                'storm.cluster.totalMem': _gt(cluster_stats, 0, tags, _float, 'totalMem'),
                'storm.cluster.totalCpu': _gt(cluster_stats, 0, tags, _float, 'totalCpu'),
                'storm.cluster.availMem': _gt(cluster_stats, 0, tags, _float, 'availMem'),
                'storm.cluster.availCpu': _gt(cluster_stats, 0, tags, _float, 'availCpu'),
                'storm.cluster.memAssignedPercentUtil': _gt(cluster_stats, 0, tags, _float, 'memAssignedPercentUtil'),
                'storm.cluster.cpuAssignedPercentUtil': _gt(cluster_stats, 0, tags, _float, 'cpuAssignedPercentUtil'),
            }

    def process_nimbus_stats(self, environment, nimbus_stats):
        if len(nimbus_stats) == 0:
            return []
        else:
            stats = []
            numLeaders = 0
            numFollowers = 0
            numDead = 0
            numOffline = 0
            for ns in nimbus_stats.get('nimbuses', []):
                nimbus_status = _g(ns, 'offline', None, 'status').lower()
                version = _g(ns, 'unknown', None, 'version').replace(' ', '_').lower()
                storm_host = _g(ns, 'unknown', None, 'host')
                tags = [
                    '#stormClusterEnvironment:{}'.format(environment),
                    '#stormVersion:{}'.format(version),
                    '#stormHost:{}'.format(storm_host),
                    '#stormStatus:{}'.format(nimbus_status)
                ]

                if nimbus_status == 'offline':
                    numOffline += 1
                elif nimbus_status == 'leader':
                    numLeaders += 1
                elif nimbus_status == 'dead':
                    numDead += 1
                else:
                    numFollowers += 1

                stats.append({'storm.nimbus.upTimeSeconds': _gt(ns, 0, tags, _long, 'nimbusUpTimeSeconds')})
            tags = ['#stormClusterEnvironment:{}'.format(environment)]
            stats.append({
                'storm.nimbus.numLeaders': (numLeaders, tags),
                'storm.nimbus.numFollowers': (numFollowers, tags),
                'storm.nimbus.numOffline': (numOffline, tags),
                'storm.nimbus.numDead': (numDead, tags),
            })
            return stats

    def process_supervisor_stats(self, supervisor_stats):
        if len(supervisor_stats) == 0:
            return {}
        else:
            r = []
            for ss in supervisor_stats.get('supervisors', []):
                host = _g(ss, 'unknown', None, 'host')
                version = _g(ss, 'unknown', None, 'version').replace(' ', '_').lower()
                storm_id = _g(ss, 'unknown', None, 'id')
                tags = ['#stormHost:{}'.format(host), '#stormVersion:{}'.format(version),
                        '#stormSupervisorId:{}'.format(storm_id)]
                stat = {
                    'storm.supervisor.uptimeSeconds': _gt(ss, 0, tags, _long, 'uptimeSeconds'),
                    'storm.supervisor.slotsTotal': _gt(ss, 0, tags, _long, 'slotsTotal'),
                    'storm.supervisor.slotsUsed': _gt(ss, 0, tags, _long, 'slotsUsed'),
                    'storm.supervisor.totalMem': _gt(ss, 0, tags, _float, 'totalMem'),
                    'storm.supervisor.usedMem': _gt(ss, 0, tags, _float, 'usedMem'),
                    'storm.supervisor.totalCpu': _gt(ss, 0, tags, _float, 'totalCpu'),
                    'storm.supervisor.usedCpu': _gt(ss, 0, tags, _float, 'usedCpu')
                }
                r.append(stat)
            return r

    def process_topology_stats(self, topology_stats, interval):

        def _mts(metric_name):
            return 'storm.topologyStats.last_{}.{}'.format(interval, metric_name)

        if len(topology_stats) == 0:
            return {}
        else:
            name = _g(topology_stats, 'unknown', None, 'name').replace('.', '_').replace(':', '_')
            tags = ['#topology:{}'.format(name)]
            r = {'topologyStats': {}, 'bolts': [], 'spouts': [], 'workers': []}
            r['topologyStats'][_mts('emitted')] = _gt(topology_stats, 0, tags, _long, 'topologyStats', 0, 'emitted')
            r['topologyStats'][_mts('transferred')] = _gt(topology_stats, 0, tags, _long,
                                                          'topologyStats', 0, 'transferred')
            r['topologyStats'][_mts('acked')] = _gt(topology_stats, 0, tags, _long, 'topologyStats', 0, 'acked')
            r['topologyStats'][_mts('failed')] = _gt(topology_stats, 0, tags, _long, 'topologyStats', 0, 'failed')
            r['topologyStats'][_mts('completeLatency')] = _gt(topology_stats, 0, tags, _float,
                                                              'topologyStats', 0, 'completeLatency')
            r['topologyStats'][_mts('uptimeSeconds')] = _gt(topology_stats, 0, tags, _long, 'uptimeSeconds')
            r['topologyStats'][_mts('executorsTotal')] = _gt(topology_stats, 0, tags, _long, 'executorsTotal')

            # Bolt Stats
            def _mb(metric_name):
                return 'storm.bolt.last_{}.{}'.format(interval, metric_name)

            r['topologyStats'][_mts('numBolts')] = _gt(topology_stats, [], tags, len, 'bolts')
            for b in _g(topology_stats, [], None, 'bolts'):
                bolt_stat = {}
                bolt_name = _g(b, 'unknown', None, 'boltId').replace('.', '_').replace(':', '_')
                bolt_tags = tags + ['#bolt:{}'.format(bolt_name)]
                bolt_stat[_mb('tasks')] = _gt(b, 0, bolt_tags, _long, 'tasks')
                bolt_stat[_mb('executeLatency')] = _gt(b, 0, bolt_tags, _float, 'executeLatency')
                bolt_stat[_mb('processLatency')] = _gt(b, 0, bolt_tags, _float, 'processLatency')
                bolt_stat[_mb('capacity')] = _gt(b, 0, bolt_tags, _float, 'capacity')
                bolt_stat[_mb('failed')] = _gt(b, 0, bolt_tags, _long, 'failed')
                bolt_stat[_mb('emitted')] = _gt(b, 0, bolt_tags, _long, 'emitted')
                bolt_stat[_mb('acked')] = _gt(b, 0, bolt_tags, _long, 'acked')
                bolt_stat[_mb('transferred')] = _gt(b, 0, bolt_tags, _long, 'transferred')
                bolt_stat[_mb('executed')] = _gt(b, 0, bolt_tags, _long, 'executed')
                bolt_stat[_mb('executors')] = _gt(b, 0, bolt_tags, _long, 'executors')
                bolt_stat[_mb('errorLapsedSecs')] = _gt(b, 1E10, bolt_tags, _long, 'errorLapsedSecs')
                bolt_stat[_mb('requestedMemOnHeap')] = _gt(b, 0, bolt_tags, _long, 'requestedMemOnHeap')
                bolt_stat[_mb('requestedMemOffHeap')] = _gt(b, 0, bolt_tags, _long, 'requestedMemOffHeap')
                bolt_stat[_mb('requestedCpu')] = _gt(b, 0, bolt_tags, _float, 'requestedCpu')
                r['bolts'].append(bolt_stat)
            r['topologyStats'][_mts('replicationCount')] = _gt(topology_stats, 0, tags, _long, 'replicationCount')
            r['topologyStats'][_mts('tasksTotal')] = _gt(topology_stats, 0, tags, _long, 'tasksTotal')

            # Process Spout stats
            def _ms(metric_name):
                return 'storm.spout.last_{}.{}'.format(interval, metric_name)

            r['topologyStats'][_mts('numSpouts')] = _gt(topology_stats, [], tags, len, 'spouts')
            for s in _g(topology_stats, [], None, 'spouts'):
                spout_stat = {}
                spout_name = _g(s, 'unknown', None, 'spoutId').replace('.', '_').replace(':', '_')
                spout_tags = tags + ['#spout:{}'.format(spout_name)]
                spout_stat[_ms('tasks')] = _gt(s, 0, spout_tags, _long, 'tasks')
                spout_stat[_ms('completeLatency')] = _gt(s, 0, spout_tags, _float, 'completeLatency')
                spout_stat[_ms('failed')] = _gt(s, 0, spout_tags, _long, 'failed')
                spout_stat[_ms('acked')] = _gt(s, 0, spout_tags, _long, 'acked')
                spout_stat[_ms('transferred')] = _gt(s, 0, spout_tags, _long, 'transferred')
                spout_stat[_ms('emitted')] = _gt(s, 0, spout_tags, _long, 'emitted')
                spout_stat[_ms('executors')] = _gt(s, 0, spout_tags, _long, 'executors')
                spout_stat[_ms('errorLapsedSecs')] = _gt(s, 1E10, spout_tags, _long, 'errorLapsedSecs')
                spout_stat[_ms('requestedMemOnHeap')] = _gt(s, 0, spout_tags, _long, 'requestedMemOnHeap')
                spout_stat[_ms('requestedMemOffHeap')] = _gt(s, 0, spout_tags, _long, 'requestedMemOffHeap')
                spout_stat[_ms('requestedCpu')] = _gt(s, 0, spout_tags, _float, 'requestedCpu')
                r['spouts'].append(spout_stat)

            # Process worker stats
            def _mw(metric_name):
                return 'storm.worker.last_{}.{}'.format(interval, metric_name)

            r['topologyStats'][_mts('workersTotal')] = (topology_stats['workersTotal'] or 0, tags)
            for w in _g(topology_stats, [], None, 'workers'):
                worker_stat = {}
                host = _g(w, 'unknown', None, 'host')
                port = _g(w, 0, _long, 'port')
                supervisor_id = _g(w, 'unknown', None, 'supervisorId')
                worker_tags = tags + ['#worker:{}:{}'.format(host, port), '#supervisor:{}'.format(supervisor_id)]
                worker_stat[_mw('executorsTotal')] = _gt(w, 0, worker_tags, _long, 'executorsTotal')
                worker_stat[_mw('assignedMemOnHeap')] = _gt(w, 0, worker_tags, _long, 'assignedMemOnHeap')
                worker_stat[_mw('assignedMemOffHeap')] = _gt(w, 0, worker_tags, _long, 'assignedMemOffHeap')
                worker_stat[_mw('assignedCpu')] = _gt(w, 0, worker_tags, _float, 'assignedCpu')
                worker_stat[_mw('uptimeSeconds')] = _gt(w, 0, worker_tags, _long, 'uptimeSeconds')
                for cn, cv in _g(w, {}, None, 'componentNumTasks').items():
                    worker_stat[_mw('componentNumTasks')] = (_long(cv or 0), worker_tags + ['component:{}'.format(cn)])
                r['workers'].append(worker_stat)

            debug_mode = _g(topology_stats, False, bool, 'debug')
            r['topologyStats'][_mts('debug')] = (1 if debug_mode else 0, tags)
            r['topologyStats'][_mts('samplingPct')] = _gt(topology_stats, 0.0, tags, _float, 'samplingPct')
            r['topologyStats'][_mts('msgTimeout')] = _gt(topology_stats, 0, tags, _long, 'msgTimeout')
            r['topologyStats'][_mts('assignedMemOnHeap')] = _gt(topology_stats, 0, tags, _long, 'assignedMemOnHeap')
            r['topologyStats'][_mts('assignedMemOffHeap')] = _gt(topology_stats, 0, tags, _long, 'assignedMemOffHeap')
            r['topologyStats'][_mts('assignedTotalMem')] = _gt(topology_stats, 0, tags, _long, 'assignedTotalMem')
            r['topologyStats'][_mts('assignedCpu')] = _gt(topology_stats, 0.0, tags, _float, 'assignedCpu')
            r['topologyStats'][_mts('requestedMemOnHeap')] = _gt(topology_stats, 0, tags, _long, 'requestedMemOnHeap')
            r['topologyStats'][_mts('requestedMemOffHeap')] = _gt(topology_stats, 0, tags, _long, 'requestedMemOffHeap')
            r['topologyStats'][_mts('requestedCpu')] = _gt(topology_stats, 0.0, tags, _float, 'requestedCpu')
            return r

    def process_topology_metrics(self, topology_name, topology_stats):
        if len(topology_stats) == 0:
            return {}
        else:
            name = topology_name.replace('.', '_').replace(':', '_')
            tags = ['#topology:{}'.format(name)]
            r = {'bolts': [], 'spouts': []}
            for k in r.keys():
                for s in _g(topology_stats, [], None, k):
                    k_stat = defaultdict(list)
                    k_name = _g(s, 'unknown', None, 'id').replace('.', '_').replace(':', '_')
                    k_tags = tags + ['#{}:{}'.format(k, k_name)]
                    for sc in ['emitted', 'transferred', 'acked', 'failed', 'complete_ms_avg', 'process_ms_avg',
                               'executed', 'executed_ms_avg']:
                        for ks in _g(s, [], None, sc):
                            stream_id = _g(ks, 'unknown', None, 'stream_id')
                            ks_tags = k_tags + ['#stream:{}'.format(stream_id)]
                            component_id = _g(ks, None, None, 'component_id')
                            if component_id:
                                ks_tags.append('#component:{}'.format(component_id))

                            component_value = _g(ks, 0.0, _float, 'value')
                            if component_value is not None:
                                # will make stats like these two examples
                                # storm.topologyStats.metrics.spouts.emitted
                                # storm.topologyStatus.metrics.bolts.acked
                                k_stat['storm.topologyStats.metrics.{}.{}'.format(k, sc)].append(
                                    (component_value, ks_tags))
                    r[k].append(k_stat)
            return r

    def report_gauge(self, metric, value, tags, additional_tags=list()):
        all_tags = tags + [
            '#env:{}'.format(self.environment_name),
            '#environment:{}'.format(self.environment_name)] + additional_tags
        self.gauge(
            metric=metric,
            value=value,
            tags=all_tags
        )

    def update_from_config(self, instance):
        if instance.get('https', self.init_config.get('https', "False")).lower() in ['true', 't', '1']:
            self.http_prefix = 'https://'
        else:
            self.http_prefix = 'http://'
        self.nimbus_server = instance.get('server', self.init_config.get('server', 'localhost:9005'))
        self.environment_name = instance.get('environment', self.init_config.get('environment', 'dev'))
        self.additional_tags = instance.get('tags', [])
        self.excluded_topologies = instance.get('excluded', [])
        intervals = instance.get('intervals', self.init_config.get('intervals', [60]))
        self.intervals = []
        if isinstance(intervals, (list, tuple)):
            for interval in intervals:
                if isinstance(interval, (list, tuple)):
                    for i in interval:
                        self.intervals.append(int(i))
                else:
                    self.intervals.append(int(interval))
        elif isinstance(intervals, (int, long)):
            self.intervals.append(intervals)
        else:
            self.intervals.extend([int(i) for i in intervals.split(',')])

    def check(self, instance):
        # Setup
        self.update_from_config(instance)

        # Cluster Stats
        cluster_stats = self.get_storm_cluster_summary()
        for k, v in self.process_cluster_stats(self.environment_name, cluster_stats).items():
            value = v[0]
            tags = v[1]
            self.report_gauge(metric=k, value=value, tags=tags, additional_tags=self.additional_tags)

        # Nimbus Stats
        nimbus_stats = self.get_storm_nimbus_summary()
        for ns in self.process_nimbus_stats(self.environment_name, nimbus_stats):
            for k, v in ns.items():
                value = v[0]
                tags = v[1]
                self.report_gauge(metric=k, value=value, tags=tags, additional_tags=self.additional_tags)

        # Supervisor Stats
        supervisor_stats = self.get_storm_supervisor_summary()
        for ss in self.process_supervisor_stats(supervisor_stats):
            for k, v in ss.items():
                value = v[0]
                tags = v[1]
                self.report_gauge(metric=k, value=value, tags=tags, additional_tags=self.additional_tags)

        # Topology Stats
        summary = self.get_storm_topology_summary()
        for topology in summary['topologies']:
            topology_id = topology.get('id')
            topology_name = _g(topology, 'unknown', None, 'name')
            if topology_name not in self.excluded_topologies:
                stats = self.get_topology_info(topology_id=topology_id)
                interval_results = []
                for interval in self.intervals:
                    results = self.process_topology_stats(topology_stats=stats, interval=interval)
                    if len(results) > 0:
                        interval_results.append(results)
                metric_stats = self.get_topology_metrics(topology_id=topology_id)
                metric_results = self.process_topology_metrics(topology_name, metric_stats)

                topology_status = _g(stats, 'unknown', None, 'status').upper()
                if topology_status != 'ACTIVE':
                    check_status = AgentCheck.CRITICAL
                    self.service_check(
                        'topology-check.{}'.format(topology_name),
                        status=check_status,
                        message='{} topology status marked as: {}'.format(topology_name, topology_status),
                        tags=['#env:{}'.format(self.environment_name),
                              '#environment:{}'.format(self.environment_name)] + self.additional_tags
                    )
                else:
                    check_status = AgentCheck.OK
                    self.service_check(
                        'topology-check.{}'.format(topology_name),
                        status=check_status,
                        message='{} topology is active'.format(topology_name),
                        tags=['#env:{}'.format(self.environment_name),
                              '#environment:{}'.format(self.environment_name)] + self.additional_tags
                    )

                if len(interval_results) > 0:
                    for results in interval_results:
                        for k, v in results['topologyStats'].items():
                            value = v[0]
                            tags = v[1]
                            self.report_gauge(metric=k, value=value, tags=tags, additional_tags=self.additional_tags)

                        # Bolt stats
                        for stat in results['bolts']:
                            for k, v in stat.items():
                                value = v[0]
                                tags = v[1]
                                self.report_gauge(metric=k, value=value, tags=tags, additional_tags=self.additional_tags)

                        # Spout stats
                        for stat in results['spouts']:
                            for k, v in stat.items():
                                value = v[0]
                                tags = v[1]
                                self.report_gauge(metric=k, value=value, tags=tags, additional_tags=self.additional_tags)

                if len(metric_results) > 0:
                    # Bolt stats
                    for stats in metric_results['bolts']:
                        for k, stat in stats.items():
                            for v in stat:
                                value = v[0]
                                tags = v[1]
                                self.report_gauge(metric=k, value=value, tags=tags,
                                                  additional_tags=self.additional_tags)

                    # Spout stats
                    for stats in metric_results['spouts']:
                        for k, stat in stats.items():
                            for v in stat:
                                value = v[0]
                                tags = v[1]
                                self.report_gauge(metric=k, value=value, tags=tags,
                                                  additional_tags=self.additional_tags)
