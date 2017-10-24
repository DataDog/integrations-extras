# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import requests

# project
from checks import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'storm'


def _g(stat_map, default, func, *components):
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


def _get_length(stat_map, default, *components):
    """ Helper Function to get the length of an array type from the map.

    :param stat_map: stat map
    :param default: default length value
    :param components: components in order to traverse.
    :return: length of array or default value.
    :rtype: int
    """
    return _g(stat_map, default, len, *components)


def _get_long(stat_map, default, *components):
    """ Helper Function to get the long value from the map.

    :param stat_map: stat map
    :param default: default length value
    :param components: components in order to traverse.
    :return: long of value or default value.
    :rtype: long
    """
    return _g(stat_map, default, _long, *components)


def _get_float(stat_map, default, *components):
    """ Helper Function to get the float value from the map.

    :param stat_map: stat map
    :param default: default length value
    :param components: components in order to traverse.
    :return: float of value or default value.
    :rtype: float
    """
    return _g(stat_map, default, _float, *components)


class StormCheck(AgentCheck):
    """
    Apache Storm 1.x.x Topology Execution Stats
    """

    def __init__(self, name, init_config, agentConfig, instances=None):
        self.nimbus_server = 'http://localhost:9005'
        self.additional_tags = []
        self.excluded_topologies = []
        self.environment_name = 'dev'
        self.intervals = []
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def get_request_json(self, url_part, error_message, params=None):
        url = "{}{}".format(self.nimbus_server, url_part)
        try:
            self.log.debug("Fetching url %s", url)
            resp = requests.get(url, params=params)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning("[url:{}] {}".format(url, error_message))
                return {}
            return data
        except Exception as e:
            self.log.warning("[url:{}] {}".format(url, error_message))
            self.log.exception(e)
            return {}

    def get_storm_cluster_summary(self):
        """ Make the storm cluster summary metric request.

        :return: Cluster Summary Stats Response
        :rtype: dict
        """
        return self.get_request_json("/api/v1/cluster/summary", "Error retrieving Storm Cluster Summary")

    def get_storm_nimbus_summary(self):
        """ Make the storm nimbus summary metric request.

        :return: Nimbus Summary Stats Response
        :rtype: dict
        """
        return self.get_request_json("/api/v1/nimbus/summary", "Error retrieving Storm Nimbus Summary")

    def get_storm_supervisor_summary(self):
        """ Make the storm supervisor summary metric request.

        :return: Supervisor Summary Stats Response
        :rtype: dict
        """
        return self.get_request_json("/api/v1/supervisor/summary", "Error retrieving Storm Supervisor Summary")

    def get_storm_topology_summary(self):
        """ Make the storm topology summary metric request.

        :return: Topology Summary Stats Response
        :rtype: dict
        """
        return self.get_request_json("/api/v1/topology/summary", "Error retrieving Storm Topology Summary")

    def get_topology_info(self, topology_id, interval=60):
        """ Make the topology info metric request.

        :param topology_id: Topology Id
        :type topology_id: str
        :return: Topology Info Response
        :rtype: dict
        """
        params = {'window': interval}
        return self.get_request_json("/api/v1/topology/{}".format(topology_id),
                                     "Error retrieving Storm Topology Info for topology:{}".format(topology_id),
                                     params=params)

    def get_topology_metrics(self, topology_id, interval=60):
        """ Make the storm topology metrics request.

        :param topology_id: Topology Id
        :type topology_id: str
        :param interval: Interval in seconds
        :type interval: int|long
        :return: Topology Metrics Stats Response
        :rtype: dict
        """

        params = {'window': interval}
        return self.get_request_json("/api/v1/topology/{}/metrics".format(topology_id),
                                     "Error retrieving Storm Topology Metrics for topology:{}".format(topology_id),
                                     params=params)

    def process_cluster_stats(self, environment, cluster_stats):
        """ Process Cluster Stats Response

        :param environment: Storm Environment
        :type environment: str
        :param cluster_stats: Cluster stats response
        :type cluster_stats: dict
        :return: Extracted cluster stats metrics
        :rtype: dict
        """
        if len(cluster_stats) == 0:
            return {}
        else:
            version = _g(cluster_stats, 'unknown', None, 'version').replace(' ', '_').lower()
            tags = ['stormClusterEnvironment:{}'.format(environment), 'stormVersion:{}'.format(version)]
            # Longs
            for metric_name in ['executorsTotal', 'slotsFree', 'slotsTotal', 'slotsUsed', 'supervisors', 'tasksTotal',
                                'topologies']:
                self.report_gauge('storm.cluster.{}'.format(metric_name), _get_long(cluster_stats, 0, metric_name),
                                  tags=tags, additional_tags=self.additional_tags)
            # Floats
            for metric_name in ['availCpu', 'availMem', 'cpuAssignedPercentUtil', 'memAssignedPercentUtil', 'totalCpu',
                                'totalMem']:
                self.report_gauge('storm.cluster.{}'.format(metric_name),
                                  _get_float(cluster_stats, 0.0, metric_name),
                                  tags=tags, additional_tags=self.additional_tags)

    def process_nimbus_stats(self, environment, nimbus_stats):
        """ Process Nimbus Stats Response

        :param environment: Storm Environment
        :type environment: str
        :param nimbus_stats: Nimbus stats response
        :type nimbus_stats: dict
        :return: Extracted nimbus stats metrics
        :rtype: dict
        """
        if len(nimbus_stats) > 0:
            numLeaders = 0
            numFollowers = 0
            numDead = 0
            numOffline = 0
            for ns in nimbus_stats.get('nimbuses', []):
                nimbus_status = _g(ns, 'offline', None, 'status').lower()
                version = _g(ns, 'unknown', None, 'version').replace(' ', '_').lower()
                storm_host = _g(ns, 'unknown', None, 'host')
                tags = [
                    'stormClusterEnvironment:{}'.format(environment),
                    'stormVersion:{}'.format(version),
                    'stormHost:{}'.format(storm_host),
                    'stormStatus:{}'.format(nimbus_status)
                ]

                if nimbus_status == 'offline':
                    numOffline += 1
                elif nimbus_status == 'leader':
                    numLeaders += 1
                elif nimbus_status == 'dead':
                    numDead += 1
                else:
                    numFollowers += 1

                self.report_gauge('storm.nimbus.upTimeSeconds', _get_long(ns, 0, 'nimbusUpTimeSeconds'),
                                  tags=tags, additional_tags=self.additional_tags)
            tags = ['stormClusterEnvironment:{}'.format(environment)]
            self.report_gauge('storm.nimbus.numDead', numDead,
                              tags=tags, additional_tags=self.additional_tags)
            self.report_gauge('storm.nimbus.numFollowers', numFollowers,
                              tags=tags, additional_tags=self.additional_tags)
            self.report_gauge('storm.nimbus.numLeaders', numLeaders,
                              tags=tags, additional_tags=self.additional_tags)
            self.report_gauge('storm.nimbus.numOffline', numOffline,
                              tags=tags, additional_tags=self.additional_tags)

    def process_supervisor_stats(self, supervisor_stats):
        """ Process Supervisor Stats Response

        :param supervisor_stats: Supervisor stats response
        :type supervisor_stats: dict
        :return: Extracted supervisor stats metrics
        :rtype: dict
        """
        if len(supervisor_stats) > 0:
            for ss in supervisor_stats.get('supervisors', []):
                host = _g(ss, 'unknown', None, 'host')
                version = _g(ss, 'unknown', None, 'version').replace(' ', '_').lower()
                storm_id = _g(ss, 'unknown', None, 'id')
                tags = ['stormHost:{}'.format(host), 'stormVersion:{}'.format(version),
                        'stormSupervisorId:{}'.format(storm_id)]
                # longs
                for metric_name in ['slotsTotal', 'slotsUsed', 'uptimeSeconds']:
                    self.report_gauge('storm.supervisor.{}'.format(metric_name), _get_long(ss, 0, metric_name),
                                      tags=tags, additional_tags=self.additional_tags)
                # floats
                for metric_name in ['totalCpu', 'totalMem', 'usedCpu', 'usedMem']:
                    self.report_gauge('storm.supervisor.{}'.format(metric_name), _get_float(ss, 0, metric_name),
                                      tags=tags, additional_tags=self.additional_tags)

    def process_topology_stats(self, topology_stats, interval):
        """ Process Topology Stats Response

        :param topology_stats: Supervisor stats response
        :type topology_stats: dict
        :param interval: Interval of metrics reported
        :type interval: int
        """
        def _mts(metric_name):
            return 'storm.topologyStats.last_{}.{}'.format(interval, metric_name)

        if len(topology_stats) > 0:
            name = _g(topology_stats, 'unknown', None, 'name').replace('.', '_').replace(':', '_')
            debug_mode = _g(topology_stats, False, bool, 'debug')
            tags = ['topology:{}'.format(name)]

            self.report_histogram(_mts('acked'), _get_long(topology_stats, 0, 'topologyStats', 0, 'acked'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('assignedCpu'), _get_float(topology_stats, 0.0, 'assignedCpu'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('assignedMemOffHeap'), _get_long(topology_stats, 0, 'assignedMemOffHeap'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('assignedMemOnHeap'), _get_long(topology_stats, 0, 'assignedMemOnHeap'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('assignedTotalMem'), _get_long(topology_stats, 0, 'assignedTotalMem'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('completeLatency'),
                                  _get_float(topology_stats, 0.0, 'topologyStats', 0, 'completeLatency'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('debug'), 1 if debug_mode else 0,
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('emitted'), _get_long(topology_stats, 0, 'topologyStats', 0, 'emitted'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('executorsTotal'), _get_long(topology_stats, 0, 'executorsTotal'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('failed'), _get_long(topology_stats, 0, 'topologyStats', 0, 'failed'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('msgTimeout'), _get_long(topology_stats, 0, 'msgTimeout'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('numBolts'), _get_length(topology_stats, 0, 'bolts'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('numSpouts'), _get_length(topology_stats, 0, 'spouts'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('replicationCount'), _get_long(topology_stats, 0, 'replicationCount'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('requestedCpu'), _get_float(topology_stats, 0.0, 'requestedCpu'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('requestedMemOffHeap'), _get_float(topology_stats, 0.0, 'requestedMemOffHeap'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('requestedMemOnHeap'), _get_float(topology_stats, 0.0, 'requestedMemOnHeap'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('samplingPct'), _get_float(topology_stats, 0.0, 'samplingPct'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('tasksTotal'), _get_long(topology_stats, 0, 'tasksTotal'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('transferred'), _get_long(topology_stats, 0, 'topologyStats', 0, 'transferred'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('uptimeSeconds'), _get_long(topology_stats, 0, 'uptimeSeconds'),
                                  tags=tags, additional_tags=self.additional_tags)
            self.report_histogram(_mts('workersTotal'), _get_long(topology_stats, 0, 'workersTotal'),
                                  tags=tags, additional_tags=self.additional_tags)

            # Bolt Stats
            def _mb(metric_name):
                return 'storm.bolt.last_{}.{}'.format(interval, metric_name)

            for b in _g(topology_stats, [], None, 'bolts'):
                bolt_name = _g(b, 'unknown', None, 'boltId').replace('.', '_').replace(':', '_')
                bolt_tags = tags + ['bolt:{}'.format(bolt_name)]

                # Longs:
                for metric_name in ['acked', 'emitted', 'executed', 'executors', 'failed',
                                    'requestedMemOffHeap', 'requestedMemOnHeap', 'tasks', 'transferred']:
                    self.report_histogram(_mb(metric_name), _get_long(b, 0, metric_name),
                                          tags=bolt_tags, additional_tags=self.additional_tags)
                # Floats
                for metric_name in ['capacity', 'executeLatency', 'processLatency', 'requestedCpu']:
                    self.report_histogram(_mb(metric_name), _get_float(b, 0, metric_name),
                                          tags=bolt_tags, additional_tags=self.additional_tags)

                self.report_histogram(_mb('errorLapsedSecs'), _get_float(b, 1E10, 'errorLapsedSecs'),
                                      tags=bolt_tags, additional_tags=self.additional_tags)

            # Process Spout stats
            def _ms(metric_name):
                return 'storm.spout.last_{}.{}'.format(interval, metric_name)

            for s in _g(topology_stats, [], None, 'spouts'):
                spout_name = _g(s, 'unknown', None, 'spoutId').replace('.', '_').replace(':', '_')
                spout_tags = tags + ['spout:{}'.format(spout_name)]

                # Longs:
                for metric_name in ['acked', 'emitted', 'executors', 'failed', 'requestedMemOffHeap',
                                    'requestedMemOnHeap', 'tasks', 'transferred']:
                    self.report_histogram(_ms(metric_name), _get_long(s, 0, metric_name),
                                          tags=spout_tags, additional_tags=self.additional_tags)
                # Floats
                for metric_name in ['completeLatency', 'requestedCpu']:
                    self.report_histogram(_ms(metric_name), _get_float(s, 0, metric_name),
                                          tags=spout_tags, additional_tags=self.additional_tags)

                self.report_histogram(_ms('errorLapsedSecs'), _get_float(s, 1E10, 'errorLapsedSecs'),
                                      tags=spout_tags, additional_tags=self.additional_tags)

            # Process worker stats
            def _mw(metric_name):
                return 'storm.worker.last_{}.{}'.format(interval, metric_name)

            for w in _g(topology_stats, [], None, 'workers'):
                worker_stat = {}
                host = _g(w, 'unknown', None, 'host')
                port = _g(w, 0, _long, 'port')
                supervisor_id = _g(w, 'unknown', None, 'supervisorId')
                worker_tags = tags + ['worker:{}:{}'.format(host, port), 'supervisor:{}'.format(supervisor_id)]

                self.report_histogram(_mw('assignedCpu'), _get_float(w, 0, 'assignedCpu'),
                                      tags=worker_tags, additional_tags=self.additional_tags)
                self.report_histogram(_mw('assignedMemOffHeap'), _get_long(w, 0, 'assignedMemOffHeap'),
                                      tags=worker_tags, additional_tags=self.additional_tags)
                self.report_histogram(_mw('assignedMemOnHeap'), _get_long(w, 0, 'assignedMemOnHeap'),
                                      tags=worker_tags, additional_tags=self.additional_tags)
                self.report_histogram(_mw('executorsTotal'), _get_long(w, 0, 'executorsTotal'),
                                      tags=worker_tags, additional_tags=self.additional_tags)
                self.report_histogram(_mw('uptimeSeconds'), _get_long(w, 0, 'uptimeSeconds'),
                                      tags=worker_tags, additional_tags=self.additional_tags)

                worker_stat[_mw('componentNumTasks')] = []
                for cn, cv in _g(w, {}, None, 'componentNumTasks').items():
                    worker_component_tags = worker_tags + ['component:{}'.format(cn)]
                    self.report_histogram(_mw('componentNumTasks'), _long(cv or 0),
                                          tags=worker_component_tags, additional_tags=self.additional_tags)

    def process_topology_metrics(self, topology_name, topology_stats, interval):
        """ Process Topology Metrics Stats Response

        :param topology_name: Topology Name
        :type topology_name: str
        :param topology_stats: Supervisor stats response
        :type topology_stats: dict
        :param interval: Interval in seconds for reported metrics
        :type interval: int
        """
        if len(topology_stats) > 0:
            name = topology_name.replace('.', '_').replace(':', '_')
            tags = ['topology:{}'.format(name)]
            r = {'bolts': [], 'spouts': []}
            for k in r.keys():
                for s in _g(topology_stats, [], None, k):
                    k_name = _g(s, 'unknown', None, 'id').replace('.', '_').replace(':', '_')
                    k_tags = tags + ['{}:{}'.format(k, k_name)]
                    for sc in ['acked', 'complete_ms_avg', 'emitted', 'executed', 'executed_ms_avg', 'failed',
                               'process_ms_avg', 'transferred']:
                        for ks in _g(s, [], None, sc):
                            stream_id = _g(ks, 'unknown', None, 'stream_id')
                            ks_tags = k_tags + ['stream:{}'.format(stream_id)]
                            component_id = _g(ks, None, None, 'component_id')
                            if component_id:
                                ks_tags.append('component:{}'.format(component_id))

                            component_value = _g(ks, 0.0, _float, 'value')
                            if component_value is not None:
                                # will make stats like these two examples
                                # storm.topologyStats.metrics.spouts.last_60.emitted
                                # storm.topologyStatus.metrics.bolts.last_60.acked
                                self.report_histogram(
                                    'storm.topologyStats.metrics.{}.last_{}.{}'.format(k, interval, sc),
                                    component_value,
                                    tags=ks_tags, additional_tags=self.additional_tags
                                )

    def report_gauge(self, metric, value, tags, additional_tags=list()):
        """ Report the Gauge Metric.

        :param metric:
        :param value:
        :param tags:
        :param additional_tags:
        :return:
        """
        all_tags = tags + [
            'env:{}'.format(self.environment_name),
            'environment:{}'.format(self.environment_name)] + additional_tags
        self.gauge(
            metric=metric,
            value=value,
            tags=all_tags
        )

    def report_histogram(self, metric, value, tags, additional_tags=list()):
        """ Report the Histogram Metric.

        :param metric:
        :param value:
        :param tags:
        :param additional_tags:
        :return:
        """
        all_tags = tags + [
            'env:{}'.format(self.environment_name),
            'environment:{}'.format(self.environment_name)] + additional_tags
        self.histogram(
            metric=metric,
            value=value,
            tags=all_tags
        )

    def update_from_config(self, instance):
        """ Update Configuration tunables from instance configuration.

        :param instance: Agent config instance.
        :return: None
        """
        self.nimbus_server = instance.get('server', self.init_config.get('server', 'http://localhost:9005'))
        self.environment_name = instance.get('environment', self.init_config.get('environment', 'dev'))
        self.additional_tags.extend(instance.get('tags', []))
        self.excluded_topologies.extend(instance.get('excluded', []))
        intervals = instance.get('intervals', self.init_config.get('intervals', [60]))

        if not isinstance(intervals, (list, tuple)) or len(intervals) < 1:
            raise AssertionError("Expected intervals to be a list of integers with at least 1 value")
        else:
            self.intervals.extend(intervals)

    def check(self, instance):
        """ Perform the agent check.

        :param instance: Agent instance.
        :return: None
        """
        # Setup
        self.update_from_config(instance)

        # Cluster Stats
        cluster_stats = self.get_storm_cluster_summary()
        self.process_cluster_stats(self.environment_name, cluster_stats)

        # Nimbus Stats
        nimbus_stats = self.get_storm_nimbus_summary()
        self.process_nimbus_stats(self.environment_name, nimbus_stats)

        # Supervisor Stats
        supervisor_stats = self.get_storm_supervisor_summary()
        self.process_supervisor_stats(supervisor_stats)

        # Topology Stats
        summary = self.get_storm_topology_summary()
        for topology in summary['topologies']:
            topology_id = topology.get('id')
            topology_name = _g(topology, 'unknown', None, 'name')
            topology_status = None
            if topology_name not in self.excluded_topologies:
                for interval in self.intervals:
                    stats = self.get_topology_info(topology_id=topology_id, interval=interval)
                    self.process_topology_stats(topology_stats=stats, interval=interval)
                    metric_stats = self.get_topology_metrics(topology_id=topology_id, interval=interval)
                    self.process_topology_metrics(topology_name, metric_stats, interval=interval)

                    # only report this once.
                    if topology_status is None and _g(stats, 'unknown', None, 'status') is not None:
                        topology_status = _g(stats, 'unknown', None, 'status').upper()
                        if topology_status != 'ACTIVE':
                            check_status = AgentCheck.CRITICAL
                            self.service_check(
                                'topology-check.{}'.format(topology_name),
                                status=check_status,
                                message='{} topology status marked as: {}'.format(topology_name, topology_status),
                                tags=['env:{}'.format(self.environment_name),
                                      'environment:{}'.format(self.environment_name)] + self.additional_tags
                            )
                        else:
                            check_status = AgentCheck.OK
                            self.service_check(
                                'topology-check.{}'.format(topology_name),
                                status=check_status,
                                message='{} topology is active'.format(topology_name),
                                tags=['env:{}'.format(self.environment_name),
                                      'environment:{}'.format(self.environment_name)] + self.additional_tags
                            )

