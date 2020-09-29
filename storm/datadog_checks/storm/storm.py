# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import json

import requests
from six import PY3

from datadog_checks.base import AgentCheck

if PY3:
    long = int
    basestring = str

EVENT_TYPE = SOURCE_TYPE_NAME = 'storm'


def _g(stat_map, default, func, *components):
    """Helper method to return value, tag tuple from a stat map get.

    Note: This safely handles the odd cases where the API can return things like:
      {
        "key1": null,
        "key2": ""
      }

      Where we want `key1`, `key2`, and `key3` (absent) to be replaced with a `default` value.

    This method will also safely traverse a map for nested objects like:
      {
        "parent": [{"mykey": 1}, {"mykey": 2}]
      }
      When the `components` are `["parent", 1, "mykey"]` this will return `2`.
      When the `components` are `["parent", 1, "myotherkey"]` this will return the default value.


    :param stat_map: stat map
    :param default: default value
    :param func: function to apply after getting the value.
    :param components: components in order to traverse
    :return: stat value
    """
    value = stat_map
    for component in components:
        if isinstance(component, (int, long)):
            if isinstance(value, (list, tuple)) and len(value) > component:
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


def _bool(v):
    """Try to convert to a boolean

    :param v: value
    :rtype: bool
    """
    try:
        if isinstance(v, basestring):
            return v.lower() in ['t', 'true', '1']
        return bool(v)
    except Exception:
        return False


def _get_length(stat_map, default, *components):
    """Helper Function to safely get the length of an array type from the map.

    :param stat_map: stat map
    :param default: default length value
    :param components: components in order to traverse.
    :return: length of array or default value.
    :rtype: int
    """
    return _g(stat_map, default, len, *components)


def _get_long(stat_map, default, *components):
    """Helper Function to safely get the long value from the map.

    :param stat_map: stat map
    :param default: default length value
    :param components: components in order to traverse.
    :return: long of value or default value.
    :rtype: long
    """
    return _g(stat_map, default, _long, *components)


def _get_float(stat_map, default, *components):
    """Helper Function to safely get the float value from the map.

    :param stat_map: stat map
    :param default: default length value
    :param components: components in order to traverse.
    :return: float of value or default value.
    :rtype: float
    """
    return _g(stat_map, default, _float, *components)


def _get_string(stat_map, default, *components):
    """Helper Function to safely get the string value from the map.

    :param stat_map: stat map
    :param default: default string value
    :param components: components in order to traverse.
    :return: str of value or default value.
    :rtype: str
    """
    return _g(stat_map, default, str, *components)


def _get_bool(stat_map, default, *components):
    """Helper Function to safely get the boolean value from the map.

    :param stat_map: stat map
    :param default: default boolean value
    :param components: components in order to traverse.
    :return: bool of value or default value.
    :rtype: bool
    """
    return _g(stat_map, default, _bool, *components)


def _get_list(stat_map, *components):
    """Helper Function to safely get the list value from the map.

    :param stat_map: stat map
    :param components: components in order to traverse.
    :return: list of component
    :rtype: list
    """
    val = _g(stat_map, [], None, *components)
    if not val or not isinstance(val, list):
        return []

    return val


def _get_dict(stat_map, *components):
    """Helper Function to safely get the list value from the map.

    :param stat_map: stat map
    :param components: components in order to traverse.
    :return: dict of component
    :rtype: dict
    """
    val = _g(stat_map, {}, None, *components)

    if not val or not isinstance(val, dict):
        return {}

    return val


class StormCheck(AgentCheck):
    """
    Apache Storm 1.x.x Topology Execution Stats
    """

    DEFAULT_STORM_SERVER = 'http://localhost:9005'
    DEFAULT_STORM_ENVIRONMENT = 'dev'
    DEFAULT_STORM_INTERVALS = [60]

    class StormVersion(object):
        @classmethod
        def from_string(cls, version_string):
            """Returns a StormVersion from a given version string.

            :param version_string: Version string, like "1.2.0-RC1" or "1.2.0"
            :type version_string: str
            :return: Storm Version
            :rtype: StormCheck.StormVersion
            """
            parts = version_string.split(".")
            patch_parts = parts[2].split("-")
            try:
                classifier = patch_parts[1]
            except IndexError:
                classifier = None
            return cls(parts[0], parts[1], patch_parts[0], classifier=classifier)

        def __init__(self, major, minor, patch, classifier=None):
            self.major = major
            self.minor = minor
            self.patch = patch
            self.classifier = classifier

        def __lt__(self, other):
            """Check if this version is less than another version.

            Ignores classification.

            :param other: storm version
            :type other: StormCheck.StormVersion | str
            :return: < other version
            :rtype: bool
            """

            if isinstance(other, str):
                # convert first
                other = StormCheck.StormVersion.from_string(other)

            if not self.major < other.major:
                if not self.minor < other.minor:
                    return self.patch < other.patch
            return True

    def get_request_json(self, url_part, error_message, params=None):
        url = "{}{}".format(self.nimbus_server, url_part)
        try:
            self.log.debug("Fetching url %s", url)
            if params:
                self.log.debug("Request params: %s", params)
            resp = requests.get(url, params=params)
            resp.encoding = 'utf-8'
            data = resp.json()
            # Log response data exluding configuration section
            self.log.debug("Response data: %s", json.dumps({x: data[x] for x in data if x != 'configuration'}))
            if 'error' in data:
                self.log.warning("Error message returned in JSON response")
                raise Exception(data['error'])
            resp.raise_for_status()
            return data
        except requests.exceptions.ConnectionError as e:
            self.log.error("Unable to establish a connection to Storm UI [url:%s]", self.nimbus_server)
            raise e
        except Exception as e:
            self.log.warning("[url:%s] %s", url, error_message)
            self.log.exception(e)
            raise e

    def get_storm_cluster_summary(self):
        """Make the storm cluster summary metric request.

        :return: Cluster Summary Stats Response
        :rtype: dict
        """
        self.log.debug("Retrieving Cluster Summary Stats")
        return self.get_request_json("/api/v1/cluster/summary", "Error retrieving Storm Cluster Summary")

    def get_storm_nimbus_summary(self):
        """Make the storm nimbus summary metric request.

        :return: Nimbus Summary Stats Response
        :rtype: dict
        """
        self.log.debug("Retrieving Nimbus Summary Stats")
        return self.get_request_json("/api/v1/nimbus/summary", "Error retrieving Storm Nimbus Summary")

    def get_storm_supervisor_summary(self):
        """Make the storm supervisor summary metric request.

        :return: Supervisor Summary Stats Response
        :rtype: dict
        """
        self.log.debug("Retrieving Supervisor Summary Stats")
        return self.get_request_json("/api/v1/supervisor/summary", "Error retrieving Storm Supervisor Summary")

    def get_storm_topology_summary(self):
        """Make the storm topology summary metric request.

        :return: Topology Summary Stats Response
        :rtype: dict
        """
        self.log.debug("Retrieving Topology Summary Stats")
        return self.get_request_json("/api/v1/topology/summary", "Error retrieving Storm Topology Summary")

    def get_topology_info(self, topology_id, interval=60):
        """Make the topology info metric request.

        :param topology_id: Topology Id
        :type topology_id: str
        :return: Topology Info Response
        :rtype: dict
        """
        self.log.debug("Retrieving Topology Info. Id: %s", topology_id)
        params = {'window': interval}
        return self.get_request_json(
            "/api/v1/topology/{}".format(topology_id),
            "Error retrieving Storm Topology Info for topology:{}".format(topology_id),
            params=params,
        )

    def get_topology_metrics(self, topology_id, interval=60, storm_version=None):
        """Make the storm topology metrics request.

        :param topology_id: Topology Id
        :type topology_id: str
        :param interval: Interval in seconds
        :type interval: int|long
        :return: Topology Metrics Stats Response
        :rtype: dict
        """

        # try 1.2 by default
        endpoint = "/api/v1/topology/{}/metrics"
        if not storm_version or storm_version < '1.2.0':
            endpoint = "/api/v1/topology/{}"

        params = {'window': interval}
        return self.get_request_json(
            endpoint.format(topology_id),
            "Error retrieving Storm Topology Metrics for topology:{}".format(topology_id),
            params=params,
        )

    def process_cluster_stats(self, cluster_stats):
        """Process Cluster Stats Response

        :param cluster_stats: Cluster stats response
        :type cluster_stats: dict
        :return: Version info
        :rtype: StormCheck.StormVersion
        """
        if len(cluster_stats) >= 0:
            version = (
                _get_string(cluster_stats, _get_string(cluster_stats, 'unknown', 'stormVersion'), 'version')
                .replace(' ', '_')
                .lower()
            )
            storm_version = 'stormVersion:{}'.format(version)
            tags = [storm_version]
            if storm_version not in self.additional_tags:
                self.additional_tags.append(storm_version)

            # Longs
            for metric_name in [
                'executorsTotal',
                'slotsFree',
                'slotsTotal',
                'slotsUsed',
                'supervisors',
                'tasksTotal',
                'topologies',
            ]:
                self.report_gauge(
                    'storm.cluster.{}'.format(metric_name),
                    _get_long(cluster_stats, 0, metric_name),
                    tags=tags,
                    additional_tags=self.additional_tags,
                )
            # Floats
            for metric_name in [
                'availCpu',
                'availMem',
                'cpuAssignedPercentUtil',
                'memAssignedPercentUtil',
                'totalCpu',
                'totalMem',
            ]:
                self.report_gauge(
                    'storm.cluster.{}'.format(metric_name),
                    _get_float(cluster_stats, 0.0, metric_name),
                    tags=tags,
                    additional_tags=self.additional_tags,
                )
            return StormCheck.StormVersion.from_string(version)
        return StormCheck.StormVersion(0, 0, 0)

    def process_nimbus_stats(self, nimbus_stats):
        """Process Nimbus Stats Response

        :param nimbus_stats: Nimbus stats response
        :type nimbus_stats: dict
        :return: Extracted nimbus stats metrics
        :rtype: dict
        """
        if nimbus_stats:
            numLeaders = 0
            numFollowers = 0
            numDead = 0
            numOffline = 0
            for ns in nimbus_stats.get('nimbuses', []):
                nimbus_status = _get_string(ns, 'offline', 'status').lower()
                storm_host = _get_string(ns, 'unknown', 'host')
                tags = ['stormHost:{}'.format(storm_host), 'stormStatus:{}'.format(nimbus_status)]

                if nimbus_status == 'offline':
                    numOffline += 1
                elif nimbus_status == 'leader':
                    numLeaders += 1
                elif nimbus_status == 'dead':
                    numDead += 1
                else:
                    numFollowers += 1

                self.report_gauge(
                    'storm.nimbus.upTimeSeconds',
                    _get_long(ns, 0, 'nimbusUpTimeSeconds'),
                    tags=tags,
                    additional_tags=self.additional_tags,
                )
            self.report_gauge('storm.nimbus.numDead', numDead, tags=tags, additional_tags=self.additional_tags)
            self.report_gauge(
                'storm.nimbus.numFollowers', numFollowers, tags=tags, additional_tags=self.additional_tags
            )
            self.report_gauge('storm.nimbus.numLeaders', numLeaders, tags=tags, additional_tags=self.additional_tags)
            self.report_gauge('storm.nimbus.numOffline', numOffline, tags=tags, additional_tags=self.additional_tags)

    def process_supervisor_stats(self, supervisor_stats):
        """Process Supervisor Stats Response

        :param supervisor_stats: Supervisor stats response
        :type supervisor_stats: dict
        :return: Extracted supervisor stats metrics
        :rtype: dict
        """
        if supervisor_stats:
            for ss in _get_list(supervisor_stats, 'supervisors'):
                host = _get_string(ss, 'unknown', 'host')
                storm_id = _get_string(ss, 'unknown', 'id')
                tags = ['stormHost:{}'.format(host), 'stormSupervisorId:{}'.format(storm_id)]
                # longs
                for metric_name in ['slotsTotal', 'slotsUsed', 'uptimeSeconds']:
                    self.report_gauge(
                        'storm.supervisor.{}'.format(metric_name),
                        _get_long(ss, 0, metric_name),
                        tags=tags,
                        additional_tags=self.additional_tags,
                    )
                # floats
                for metric_name in ['totalCpu', 'totalMem', 'usedCpu', 'usedMem']:
                    self.report_gauge(
                        'storm.supervisor.{}'.format(metric_name),
                        _get_float(ss, 0, metric_name),
                        tags=tags,
                        additional_tags=self.additional_tags,
                    )

    def process_topology_stats(self, topology_stats, interval):
        """Process Topology Stats Response

        :param topology_stats: Supervisor stats response
        :type topology_stats: dict
        :param interval: Interval of metrics reported
        :type interval: int
        """

        def _mts(metric_name):
            return 'storm.topologyStats.last_{}.{}'.format(interval, metric_name)

        if topology_stats:
            name = _get_string(topology_stats, 'unknown', 'name').replace('.', '_').replace(':', '_')
            debug_mode = _get_bool(topology_stats, False, 'debug')
            tags = ['topology:{}'.format(name)]

            self.report_histogram(
                _mts('acked'),
                _get_long(topology_stats, 0, 'topologyStats', 0, 'acked'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('assignedCpu'),
                _get_float(topology_stats, 0.0, 'assignedCpu'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('assignedMemOffHeap'),
                _get_long(topology_stats, 0, 'assignedMemOffHeap'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('assignedMemOnHeap'),
                _get_long(topology_stats, 0, 'assignedMemOnHeap'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('assignedTotalMem'),
                _get_long(topology_stats, 0, 'assignedTotalMem'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('completeLatency'),
                _get_float(topology_stats, 0.0, 'topologyStats', 0, 'completeLatency'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('debug'), 1 if debug_mode else 0, tags=tags, additional_tags=self.additional_tags
            )
            self.report_histogram(
                _mts('emitted'),
                _get_long(topology_stats, 0, 'topologyStats', 0, 'emitted'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('executorsTotal'),
                _get_long(topology_stats, 0, 'executorsTotal'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('failed'),
                _get_long(topology_stats, 0, 'topologyStats', 0, 'failed'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('msgTimeout'),
                _get_long(topology_stats, 0, 'msgTimeout'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('numBolts'),
                _get_length(topology_stats, 0, 'bolts'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('numSpouts'),
                _get_length(topology_stats, 0, 'spouts'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('replicationCount'),
                _get_long(topology_stats, 0, 'replicationCount'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('requestedCpu'),
                _get_float(topology_stats, 0.0, 'requestedCpu'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('requestedMemOffHeap'),
                _get_float(topology_stats, 0.0, 'requestedMemOffHeap'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('requestedMemOnHeap'),
                _get_float(topology_stats, 0.0, 'requestedMemOnHeap'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('samplingPct'),
                _get_float(topology_stats, 0.0, 'samplingPct'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('tasksTotal'),
                _get_long(topology_stats, 0, 'tasksTotal'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('transferred'),
                _get_long(topology_stats, 0, 'topologyStats', 0, 'transferred'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('uptimeSeconds'),
                _get_long(topology_stats, 0, 'uptimeSeconds'),
                tags=tags,
                additional_tags=self.additional_tags,
            )
            self.report_histogram(
                _mts('workersTotal'),
                _get_long(topology_stats, 0, 'workersTotal'),
                tags=tags,
                additional_tags=self.additional_tags,
            )

            # Bolt Stats
            def _mb(metric_name):
                return 'storm.bolt.last_{}.{}'.format(interval, metric_name)

            for b in _get_list(topology_stats, 'bolts'):
                bolt_name = _get_string(b, 'unknown', 'boltId').replace('.', '_').replace(':', '_')
                bolt_tags = tags + ['bolt:{}'.format(bolt_name)]

                # Longs:
                for metric_name in [
                    'acked',
                    'emitted',
                    'executed',
                    'executors',
                    'failed',
                    'requestedMemOffHeap',
                    'requestedMemOnHeap',
                    'tasks',
                    'transferred',
                ]:
                    self.report_histogram(
                        _mb(metric_name),
                        _get_long(b, 0, metric_name),
                        tags=bolt_tags,
                        additional_tags=self.additional_tags,
                    )
                # Floats
                for metric_name in ['capacity', 'executeLatency', 'processLatency', 'requestedCpu']:
                    self.report_histogram(
                        _mb(metric_name),
                        _get_float(b, 0, metric_name),
                        tags=bolt_tags,
                        additional_tags=self.additional_tags,
                    )

                self.report_histogram(
                    _mb('errorLapsedSecs'),
                    _get_float(b, 1e10, 'errorLapsedSecs'),
                    tags=bolt_tags,
                    additional_tags=self.additional_tags,
                )

            # Process Spout stats
            def _ms(metric_name):
                return 'storm.spout.last_{}.{}'.format(interval, metric_name)

            for s in _get_list(topology_stats, 'spouts'):
                spout_name = _get_string(s, 'unknown', 'spoutId').replace('.', '_').replace(':', '_')
                spout_tags = tags + ['spout:{}'.format(spout_name)]

                # Longs:
                for metric_name in [
                    'acked',
                    'emitted',
                    'executors',
                    'failed',
                    'requestedMemOffHeap',
                    'requestedMemOnHeap',
                    'tasks',
                    'transferred',
                ]:
                    self.report_histogram(
                        _ms(metric_name),
                        _get_long(s, 0, metric_name),
                        tags=spout_tags,
                        additional_tags=self.additional_tags,
                    )
                # Floats
                for metric_name in ['completeLatency', 'requestedCpu']:
                    self.report_histogram(
                        _ms(metric_name),
                        _get_float(s, 0, metric_name),
                        tags=spout_tags,
                        additional_tags=self.additional_tags,
                    )

                self.report_histogram(
                    _ms('errorLapsedSecs'),
                    _get_float(s, 1e10, 'errorLapsedSecs'),
                    tags=spout_tags,
                    additional_tags=self.additional_tags,
                )

            # Process worker stats
            def _mw(metric_name):
                return 'storm.worker.last_{}.{}'.format(interval, metric_name)

            for w in _get_list(topology_stats, 'workers'):
                worker_stat = {}
                host = _get_string(w, 'unknown', 'host')
                port = _get_long(w, 0, 'port')
                supervisor_id = _get_string(w, 'unknown', 'supervisorId')
                worker_tags = tags + ['worker:{}:{}'.format(host, port), 'supervisor:{}'.format(supervisor_id)]

                self.report_histogram(
                    _mw('assignedCpu'),
                    _get_float(w, 0, 'assignedCpu'),
                    tags=worker_tags,
                    additional_tags=self.additional_tags,
                )
                self.report_histogram(
                    _mw('assignedMemOffHeap'),
                    _get_long(w, 0, 'assignedMemOffHeap'),
                    tags=worker_tags,
                    additional_tags=self.additional_tags,
                )
                self.report_histogram(
                    _mw('assignedMemOnHeap'),
                    _get_long(w, 0, 'assignedMemOnHeap'),
                    tags=worker_tags,
                    additional_tags=self.additional_tags,
                )
                self.report_histogram(
                    _mw('executorsTotal'),
                    _get_long(w, 0, 'executorsTotal'),
                    tags=worker_tags,
                    additional_tags=self.additional_tags,
                )
                self.report_histogram(
                    _mw('uptimeSeconds'),
                    _get_long(w, 0, 'uptimeSeconds'),
                    tags=worker_tags,
                    additional_tags=self.additional_tags,
                )

                worker_stat[_mw('componentNumTasks')] = []
                for cn, cv in _get_dict(w, 'componentNumTasks').items():
                    worker_component_tags = worker_tags + ['component:{}'.format(cn)]
                    self.report_histogram(
                        _mw('componentNumTasks'),
                        _long(cv or 0),
                        tags=worker_component_tags,
                        additional_tags=self.additional_tags,
                    )

    def process_topology_metrics(self, topology_name, topology_stats, interval):
        """Process Topology Metrics Stats Response

        :param topology_name: Topology Name
        :type topology_name: str
        :param topology_stats: Supervisor stats response
        :type topology_stats: dict
        :param interval: Interval in seconds for reported metrics
        :type interval: int
        """
        if topology_stats:
            name = topology_name.replace('.', '_').replace(':', '_')
            tags = ['topology:{}'.format(name)]
            for k in ('bolts', 'spouts'):
                for s in _get_list(topology_stats, k):
                    k_name = _get_string(s, 'unknown', 'id').replace('.', '_').replace(':', '_')
                    k_tags = tags + ['{}:{}'.format(k, k_name)]
                    for sc in [
                        'acked',
                        'complete_ms_avg',
                        'emitted',
                        'executed',
                        'executed_ms_avg',
                        'failed',
                        'process_ms_avg',
                        'transferred',
                    ]:
                        for ks in _get_list(s, sc):
                            stream_id = _get_string(ks, 'unknown', 'stream_id')
                            ks_tags = k_tags + ['stream:{}'.format(stream_id)]
                            component_id = ks.get('component_id')
                            if component_id:
                                ks_tags.append('component:{}'.format(component_id))

                            component_value = _get_float(ks, 0.0, 'value')
                            if component_value is not None:
                                # will make stats like these two examples
                                # storm.topologyStats.metrics.spouts.last_60.emitted
                                # storm.topologyStatus.metrics.bolts.last_60.acked
                                self.report_histogram(
                                    'storm.topologyStats.metrics.{}.last_{}.{}'.format(k, interval, sc),
                                    component_value,
                                    tags=ks_tags,
                                    additional_tags=self.additional_tags,
                                )

    def report_gauge(self, metric, value, tags, additional_tags):
        """Report the Gauge Metric.

        :param metric:
        :param value:
        :param tags:
        :param additional_tags:
        :return:
        """
        all_tags = set(tags)
        all_tags.add('stormEnvironment:{}'.format(self.environment_name))
        all_tags.update(additional_tags)
        self.gauge(metric, value=value, tags=all_tags)

    def report_histogram(self, metric, value, tags, additional_tags):
        """Report the Histogram Metric.

        :param metric:
        :param value:
        :param tags:
        :param additional_tags:
        :return:
        """
        all_tags = set(tags)
        all_tags.add('stormEnvironment:{}'.format(self.environment_name))
        all_tags.update(additional_tags)
        self.histogram(metric, value=value, tags=all_tags)

    def update_from_config(self, instance):
        """Update Configuration tunables from instance configuration.

        :param instance: Agent config instance.
        :return: None
        """
        self.nimbus_server = instance.get('server', self.init_config.get('server', StormCheck.DEFAULT_STORM_SERVER))
        self.environment_name = instance.get(
            'environment', self.init_config.get('environment', StormCheck.DEFAULT_STORM_ENVIRONMENT)
        )
        self.additional_tags = []
        self.additional_tags.extend(instance.get('tags', []))
        self.excluded_topologies = []
        self.excluded_topologies.extend(instance.get('excluded', []))
        self.intervals = []
        intervals = instance.get('intervals', self.init_config.get('intervals', StormCheck.DEFAULT_STORM_INTERVALS))

        if not isinstance(intervals, (list, tuple)) or not intervals:
            raise AssertionError("Expected intervals to be a list of integers with at least 1 value")
        self.intervals.extend(intervals)

    def check(self, instance):
        """Perform the agent check.

        :param instance: Agent instance.
        :return: None
        """
        # Setup
        self.update_from_config(instance)

        # Cluster Stats - these must query!
        cluster_stats = self.get_storm_cluster_summary()
        storm_version = self.process_cluster_stats(cluster_stats)

        # Nimbus Stats
        nimbus_stats = {}
        try:
            nimbus_stats = self.get_storm_nimbus_summary()
            self.process_nimbus_stats(nimbus_stats)
        except Exception:  # noqa
            self.log.exception("Error recording nimbus stats")

        # Supervisor Stats
        supervisor_stats = {}
        try:
            supervisor_stats = self.get_storm_supervisor_summary()
            self.process_supervisor_stats(supervisor_stats)
        except Exception:  # noqa
            self.log.exception("Error recording supervisor stats")

        # Topology Stats
        summary = self.get_storm_topology_summary()
        for topology in _get_list(summary, 'topologies'):
            topology_id = topology.get('id')
            if topology_id in (None, ''):
                self.log.warning("Ignoring topology without id.")
                continue
            topology_name = _get_string(topology, 'unknown', 'name')
            topology_status = None
            if topology_name not in self.excluded_topologies:
                for interval in self.intervals:
                    try:
                        stats = self.get_topology_info(topology_id=topology_id, interval=interval)
                        self.process_topology_stats(topology_stats=stats, interval=interval)
                        metric_stats = self.get_topology_metrics(
                            topology_id=topology_id, interval=interval, storm_version=storm_version
                        )
                        self.process_topology_metrics(topology_name, metric_stats, interval=interval)

                        # only report this once.
                        if topology_status is None:
                            topology_status = _get_string(stats, 'unknown', 'status').upper()
                            check_status = AgentCheck.CRITICAL if topology_status != 'ACTIVE' else AgentCheck.OK
                            self.service_check(
                                'topology_check.{}'.format(topology_name),
                                status=check_status,
                                message='{} topology status marked as: {}'.format(topology_name, topology_status),
                                tags=['stormEnvironment:{}'.format(self.environment_name)] + self.additional_tags,
                            )
                    except Exception:  # noqa
                        self.log.exception(
                            "unable to collect topology stats for topology_id:%s, topology_name:%s",
                            topology_id,
                            topology_name,
                        )
