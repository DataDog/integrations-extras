# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import requests

# project
from checks import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'storm'


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
        except:
            self.log.warning("Error retrieving Storm Cluster Summary from " + url)
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
        except:
            self.log.warning("Error retrieving Storm Nimbus Summary from " + url)
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
        except:
            self.log.warning("Error retrieving Storm Supervisor Summary from " + url)
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
        except:
            self.log.warning("Error retrieving Storm Topology Summary from " + url)
            return {}

    def get_topology_info(self, topology_id):
        url = self.http_prefix + self.nimbus_server + "/api/v1/topology/" + topology_id
        try:
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            data = resp.json()
            if 'error' in data:
                self.log.warning('Topology "' + topology_id + '" returned error')
                return {}
            return data
        except:
            self.log.warning("Error retrieving Storm Topology Info from " + url)
            return {}

    def try_float(self, v):
        try:
            return float(v)
        except:
            return 0.0

    def try_long(self, v):
        try:
            return long(v)
        except:
            return 0

    def process_cluster_stats(self, environment, cluster_stats):
        if len(cluster_stats) == 0:
            return {}
        else:
            version = cluster_stats.get('version', 'unknown') or 'unknown'
            tags = ['#stormClusterEnvironment:' + environment, '#stormVersion:' + version]
            return {
                'storm.cluster.executorsTotal': (cluster_stats['executorsTotal'] or 0, tags),
                'storm.cluster.slotsTotal': (cluster_stats['slotsTotal'] or 0, tags),
                'storm.cluster.slotsFree': (cluster_stats['slotsFree'] or 0, tags),
                'storm.cluster.topologies': (cluster_stats['topologies'] or 0, tags),
                'storm.cluster.supervisors': (cluster_stats['supervisors'] or 0, tags),
                'storm.cluster.tasksTotal': (cluster_stats['tasksTotal'] or 0, tags),
                'storm.cluster.slotsUsed': (cluster_stats['slotsUsed'] or 0, tags)
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
                nimbus_status = ns.get('status', 'offline').lower()
                version = ns.get('version', 'unknown') or 'unknown'
                storm_host = ns.get('host', 'unknown')
                tags = [
                    '#stormClusterEnvironment:' + environment,
                    '#stormVersion:' + version,
                    '#stormHost:' + storm_host,
                    '#stormStatus:' + nimbus_status
                ]

                if nimbus_status == 'offline':
                    numOffline += 1
                    continue
                elif nimbus_status == 'leader':
                    numLeaders += 1
                elif nimbus_status == 'dead':
                    numDead += 1
                else:
                    numFollowers += 1

                stats.append({'storm.nimbus.upTimeSeconds': (ns['nimbusUpTimeSeconds'] or 0, tags)})
            tags = ['#stormClusterEnvironment:' + environment]
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
                host = ss.get('host', 'unknown') or 'unknown'
                version = ss.get('version', 'unknown') or 'unknown'
                storm_id = ss.get('id', 'unknown') or 'unknown'
                tags = ['#stormHost:' + host, '#stormVersion:' + version, '#stormSupervisorId:' + storm_id]
                stat = {
                    'storm.supervisor.uptimeSeconds': (ss['uptimeSeconds'] or 0, tags),
                    'storm.supervisor.slotsTotal': (ss['slotsTotal'] or 0, tags),
                    'storm.supervisor.slotsUsed': (ss['slotsUsed'] or 0, tags),
                    'storm.supervisor.totalMem': (ss['totalMem'] or 0, tags),
                    'storm.supervisor.usedMem': (ss['usedMem'] or 0, tags),
                    'storm.supervisor.totalCpu': (ss['totalCpu'] or 0, tags),
                    'storm.supervisor.usedCpu': (ss['usedCpu'] or 0, tags)
                }
                r.append(stat)
            return r

    def process_topology_stats(self, topology_stats):
        if len(topology_stats) == 0:
            return {}
        else:
            name = topology_stats['name'].replace('.', '_').replace(':', '_')
            name_tag = '#topology:' + name
            r = {'topologyStats': {}, 'bolts': [], 'spouts': []}
            r['topologyStats']['storm.topologyStats.alltime.emitted'] = (topology_stats['topologyStats'][3]['emitted'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.alltime.transferred'] = (topology_stats['topologyStats'][3]['transferred'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.alltime.acked'] = (topology_stats['topologyStats'][3]['acked'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.alltime.failed'] = (topology_stats['topologyStats'][3]['failed'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.alltime.completeLatency'] = (self.try_float(topology_stats['topologyStats'][3]['completeLatency']), [name_tag])
            r['topologyStats']['storm.topologyStats.uptimeSeconds'] = (topology_stats['uptimeSeconds'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.executorsTotal'] = (topology_stats['executorsTotal'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.numBolts'] = (len(topology_stats.get('bolts', [])), [name_tag])
            for b in topology_stats.get('bolts', []):
                bolt_stat = {}
                bolt_name = b['boltId'].replace('.', '_').replace(':', '_')
                bolt_tag = '#bolt:' + bolt_name
                bolt_stat['storm.bolt.tasks'] = (b['tasks'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.executeLatency'] = (self.try_float(b['executeLatency']), [name_tag, bolt_tag])
                bolt_stat['storm.bolt.processLatency'] = (self.try_float(b['processLatency']), [name_tag, bolt_tag])
                bolt_stat['storm.bolt.capacity'] = (self.try_float(b['capacity']), [name_tag, bolt_tag])
                bolt_stat['storm.bolt.failed'] = (b['failed'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.emitted'] = (b['emitted'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.acked'] = (b['acked'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.transferred'] = (b['transferred'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.executed'] = (b['executed'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.executors'] = (b['executors'] or 0, [name_tag, bolt_tag])
                bolt_stat['storm.bolt.errorLapsedSecs'] = (self.try_long(b['errorLapsedSecs'] or 1E10), [name_tag, bolt_tag])
                r['bolts'].append(bolt_stat)
            r['topologyStats']['storm.topologyStats.replicationCount'] = (topology_stats['replicationCount'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.tasksTotal'] = (topology_stats['tasksTotal'] or 0, [name_tag])
            r['topologyStats']['storm.topologyStats.numSpouts'] = (len(topology_stats.get('spouts', [])), [name_tag])
            for s in topology_stats.get('spouts', []):
                spout_stat = {}
                spout_name = s['spoutId'].replace('.', '_').replace(':', '_')
                spout_tag = '#spout:' + spout_name
                spout_stat['storm.spout.tasks'] = (s['tasks'] or 0, [name_tag, spout_tag])
                spout_stat['storm.spout.completeLatency'] = (self.try_float(s['completeLatency']), [name_tag, spout_tag])
                spout_stat['storm.spout.failed'] = (s['failed'] or 0, [name_tag, spout_tag])
                spout_stat['storm.spout.acked'] = (s['acked'] or 0, [name_tag, spout_tag])
                spout_stat['storm.spout.transferred'] = (s['transferred'] or 0, [name_tag, spout_tag])
                spout_stat['storm.spout.emitted'] = (s['emitted'] or 0, [name_tag, spout_tag])
                spout_stat['storm.spout.executors'] = (s['executors'] or 0, [name_tag, spout_tag])
                spout_stat['storm.spout.errorLapsedSecs'] = (self.try_long(s['errorLapsedSecs'] or 1E10), [name_tag, spout_tag])
                r['spouts'].append(spout_stat)
            r['topologyStats']['storm.topologyStats.workersTotal'] = (topology_stats['workersTotal'] or 0, [name_tag])
            return r

    def report_guage(self, metric, value, tags, additional_tags=[]):
        self.gauge(
            metric=metric,
            value=value,
            tags=tags + ['#env:' + self.environment_name, '#environment:' + self.environment_name] + additional_tags
        )

    def check(self, instance):
        # Setup
        if instance.get('https', self.init_config.get('https', "False")).lower() in ['true', 't', '1']:
            self.http_prefix = 'https://'
        else:
            self.http_prefix = 'http://'
        self.nimbus_server = instance.get('server', self.init_config.get('server', 'localhost:9005'))
        self.environment_name = instance.get('environment', self.init_config.get('environment', 'dev'))
        additional_tags = instance.get('tags', [])

        # Cluster Stats
        cluster_stats = self.get_storm_cluster_summary()
        for k, v in self.process_cluster_stats(self.environment_name, cluster_stats).items():
            value = v[0]
            tags = v[1]
            self.report_guage(metric=k, value=value, tags=tags, additional_tags=additional_tags)

        # Nimbus Stats
        nimbus_stats = self.get_storm_nimbus_summary()
        for ns in self.process_nimbus_stats(self.environment_name, nimbus_stats):
            for k, v in ns.items():
                value = v[0]
                tags = v[1]
                self.report_guage(metric=k, value=value, tags=tags, additional_tags=additional_tags)

        # Supervisor Stats
        supervisor_stats = self.get_storm_supervisor_summary()
        for ss in self.process_supervisor_stats(supervisor_stats):
            for k, v in ss.items():
                value = v[0]
                tags = v[1]
                self.report_guage(metric=k, value=value, tags=tags, additional_tags=additional_tags)

        # Topology Stats
        summary = self.get_storm_topology_summary()
        excluded_topologies = instance.get('excluded', [])
        for topology in summary['topologies']:
            if topology['name'] not in excluded_topologies:
                stats = self.get_topology_info(topology_id=topology['id'])
                results = self.process_topology_stats(topology_stats=stats)
                if stats['status'] != 'ACTIVE':
                    check_status = AgentCheck.CRITICAL
                    self.service_check(
                        'topology-check.' + topology['name'],
                        status=check_status,
                        message=topology['name'] + ' topology is not active',
                        tags=['#env:' + self.environment_name,
                              '#environment:' + self.environment_name] + additional_tags
                    )
                else:
                    check_status = AgentCheck.OK
                    self.service_check(
                        'topology-check.' + topology['name'],
                        status=check_status,
                        message=topology['name'] + ' topology is active',
                        tags=['#env:' + self.environment_name,
                              '#environment:' + self.environment_name] + additional_tags
                    )

                if len(results) > 0:
                    for k, v in results['topologyStats'].items():
                        value = v[0]
                        tags = v[1]
                        self.report_guage(metric=k, value=value, tags=tags, additional_tags=additional_tags)

                    # Bolt stats
                    for stat in results['bolts']:
                        for k, v in stat.items():
                            value = v[0]
                            tags = v[1]
                            self.report_guage(metric=k, value=value, tags=tags, additional_tags=additional_tags)

                    # Spout stats
                    for stat in results['spouts']:
                        for k, v in stat.items():
                            value = v[0]
                            tags = v[1]
                            self.report_guage(metric=k, value=value, tags=tags, additional_tags=additional_tags)
