import json

from datadog_checks.base import AgentCheck, ConfigurationError


class ZabbixCheck(AgentCheck):

    SERVICE_CHECK_NAME = "zabbix.can_connect"
    METRICS = {
        "Number of processed numeric (float) values per second": "processed.floats_per_sec",
        "Number of processed values per second": "processed.per_sec",
        "Number of processed character values per second": "processed.characters_per_sec",
        "Number of processed log values per second": "processed.logs_per_sec",
        "Number of processed numeric (unsigned) values per second": "processed.unsigned_per_sec",
        "Number of processed text values per second": "processed.text_per_sec",
        "Number of processed not supported values per second": "processed.unsupported_per_sec",
        "Utilization of alerter internal processes, in %": "proccess.internal.alerter",
        "Utilization of configuration syncer internal processes, in %": "proccess.internal.config_sync",
        "Utilization of escalator internal processes, in %": "process.internal.escalator",
        "Utilization of history syncer internal processes, in %": "process.internal.history_sync",
        "Utilization of housekeeper internal processes, in %": "process.internal.housekeeper",
        "Utilization of discoverer data collector processes, in %": "process.data_collector.discoverer",
        "Utilization of http poller data collector processes, in %": "process.data_collector.http_poller",
        "Utilization of icmp pinger data collector processes, in %": "process.data_collector.icmp_pinger",
        "Utilization of ipmi poller data collector processes, in %": "process.data_collector.ipmi_poller",
        "Utilization of java poller data collector processes, in %": "process.data_collector.java_poller",
        "Utilization of poller data collector processes, in %": "process.data_collector.poller",
        "Utilization of proxy poller data collector processes, in %": "process.data_collector.proxy_poller",
        "Utilization of self-monitoring internal processes, in %": "process.internal.self_monitoring",
        "Utilization of snmp trapper data collector processes, in %": "process.data_collector.snmp_trapper",
        "Utilization of timer internal processes, in %": "process.internal.timer",
        "Utilization of trapper data collector processes, in %": "process.data_collector.trapper",
        "Utilization of unreachable poller data collector processes, in %": "process.data_collector.unreachable_poller",
        "Zabbix queue over 10 minutes": "queue.duration_10",
        "Zabbix queue": "queue.size",
        "Zabbix configuration cache, % used": "cache.config",
        "Zabbix history write cache, % used": "cache.write",
        "Zabbix history index cache, % used": "cache.index",
        "Zabbix trend write cache, % used": "cache.write_trend",
        "Zabbix agent ping": "agent.ping",
        "Utilization of vmware data collector processes, in %": "process.data_collector.vmware",
        "Zabbix value cache, % used": "cache.value",
        "Zabbix value cache hits": "cache.value.hits",
        "Zabbix value cache misses": "cache.value.misses",
        "Zabbix vmware cache, % used": "cache.vmware",
        "Zabbix value cache operating mode": "cache.operating_mode",
        "Utilization of task manager internal processes, in %": "process.internal.task_manager",
        "Utilization of ipmi manager internal processes, in %": "process.internal.ipmi_manager",
        "Utilization of alert manager internal processes, in %": "process.internal.alert_manager",
        "Utilization of preprocessing manager internal processes, in %": "process.internal.preprocessing_manager",
        "Utilization of preprocessing worker internal processes, in %": "process.internal.preprocessing_worker",
        "Zabbix preprocessing queue": "queue.preprocessing",
        "Zabbix LLD queue": "queue.lld",
        "Utilization of LLD manager internal processes, in %": "process.internal.lld_manager",
        "Utilization of LLD worker internal processes, in %": "process.internal.lld_worker",
        "Number of CPUs": "cpu.count",
        "CPU iowait time": "cpu.iowait_time",
        "Context switches per second": "context_switches_per_sec",
        "CPU guest nice time": "cpu.guest_nice_time",
        "CPU guest time": "cpu.guest_time",
        "CPU softirq time": "cpu.softirq_time",
        "CPU interrupt time": "cpu.interrupt_time",
        "CPU steal time": "cpu.steal_time",
        "CPU nice time": "cpu.nice_time",
        "Load average (1m avg)": "load.avg.1_min",
        "CPU user time": "cpu.user_time",
        "CPU system time": "cpu.system_time",
        "CPU idle time": "cpu.idle_time",
        "Load average (15m avg)": "load.avg.15_min",
        "Load average (5m avg)": "load.avg.5_min",
        "Interrupts per second": "interrupts_per_sec",
        "Available memory in %": "memory.avail_percent",
        "Total memory": "memory.total",
        "Available memory": "memory.avail",
        "Total swap space": "swap_space.total",
        "Free swap space": "swap_space.free",
        "Free swap space in %": "swap_space.free_percent",
        "System uptime": "system.uptime",
        "System boot time": "system.boot_time",
        "System local time": "system.local_time",
        "Number of logged in users": "user.logged_in",
        "Maximum number of open file descriptors": "open_fd.max",
        "Maximum number of processes": "processes_max",
        "Number of processes": "processes_count",
        "Number of running processes": "processes_running_count",
        "Checksum of /etc/passwd": "checksum",
        "CPU utilization": "cpu.used",
        "Zabbix agent availability": "agent.avail",
        "Utilization of alert syncer internal processes, in %": "process.internal.alert_sync",
        "Memory utilization": "memory.used"
    }

    def __init__(self, name, init_config, instances):
        super(ZabbixCheck, self).__init__(name, init_config, instances)
        self.tags = self.instance.get('tags', [])

    def request(self, zabbix_api, req_data):
        req_header = {
            'Content-Type': 'application/json-rpc',
        }

        try:
            res = self.http.post(zabbix_api, data=req_data.encode(), headers=req_header)
        except Exception as e:
            self.log.debug("Unable to get make request to api=%s with req_data=%s", zabbix_api, req_data)
            self.warning("Request failed: %s", str(e))
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags=self.tags)
            raise
        return res.json()

    def login(self, zabbix_user, zabbix_pass, zabbix_api):
        req_data = json.dumps(
            {
                'jsonrpc': '2.0',
                'method': 'user.login',
                'params': {'user': zabbix_user, 'password': zabbix_pass},
                'id': 1,
            }
        )
        self.log.debug("Logging in with params user=%s api=%s", zabbix_user, zabbix_api)
    
        response = self.request(zabbix_api, req_data)
        token = response.get('result')
        return token

    def logout(self, token, zabbix_api):
        req_data = json.dumps({'jsonrpc': '2.0', 'method': 'user.logout', 'params': {}, 'auth': token, 'id': 1})
        response = self.request(zabbix_api, req_data)
        self.log.debug("Logging out: %s", response)
        return response

    def get_hosts(self, token, zabbix_api, hosts=None):
        if hosts is not None:
            req_data = json.dumps(
                {
                    'jsonrpc': '2.0',
                    'method': 'host.get',
                    'params': {'filter': {'host': hosts}, 'output': ['hostid', 'host']},
                    'auth': token,
                    'id': 1,
                }
            )
        else:
            req_data = json.dumps(
                {
                    'jsonrpc': '2.0',
                    'method': 'host.get',
                    'params': {'output': ['hostid', 'host']},
                    'auth': token,
                    'id': 1,
                }
            )
        response = self.request(zabbix_api, req_data)
            
        result = response.get('result')
        self.log.debug("Getting zabbix items: %s", result)
        return result

    def get_items(self, token, hostids, zabbix_api, items=None):
        if items is not None:
            req_data = json.dumps(
                {
                    'jsonrpc': '2.0',
                    'method': 'item.get',
                    'params': {
                        'hostids': hostids,
                        'filter': {'name': items},
                        'output': ['itemid', 'name', 'hostid', 'value_type'],
                    },
                    'auth': token,
                    'id': 1,
                }
            )
        else:
            req_data = json.dumps(
                {
                    'jsonrpc': '2.0',
                    'method': 'item.get',
                    'params': {'hostids': hostids, 'output': ['itemid', 'name', 'hostid', 'value_type']},
                    'auth': token,
                    'id': 1,
                }
            )
        response = self.request(zabbix_api, req_data)
        return response.get('result')

    def get_history(self, token, hostid, itemid, value_type, zabbix_api):
        req_data = json.dumps(
            {
                'jsonrpc': '2.0',
                'method': 'history.get',
                'params': {
                    'hostids': hostid,
                    'itemids': itemid,
                    'output': ['itemid', 'value'],
                    'history': value_type,
                    'sortfield': 'clock',
                    'sortorder': 'DESC',
                    'limit': 1,
                },
                'auth': token,
                'id': 1,
            }
        )

        response = self.request(zabbix_api, req_data)
        result = response.get('result')

        return result

    def check(self, instance):
        zabbix_user = instance.get('zabbix_user')
        zabbix_pass = instance.get('zabbix_password')
        zabbix_api = instance.get('zabbix_api')

        if not zabbix_user:
            raise ConfigurationError('Configuration error, please specify zabbix_user.')

        if not zabbix_pass:
            raise ConfigurationError('Configuration error, please specify zabbix_pass.')

        if not zabbix_api:
            raise ConfigurationError('Configuration error, please specify zabbix_api.')

        hosts = instance.get('hosts')
        metrics = instance.get('metrics')

        # Get token
        token = self.login(zabbix_user, zabbix_pass, zabbix_api)
        self.log.debug(token)

        # Get hosts
        if hosts is not None:
            zabbixhosts = self.get_hosts(token, zabbix_api, hosts)
        else:
            zabbixhosts = self.get_hosts(token, zabbix_api)

        hostdic = {}
        hostids = []
        for host in zabbixhosts:
            hostdic[host['hostid']] = host['host']
            hostids.append(host['hostid'])

        # Get items
        if metrics is not None:
            zabbixitems = self.get_items(token, hostids, zabbix_api, metrics)
        else:
            zabbixitems = self.get_items(token, hostids, zabbix_api)

        self.log.debug(zabbixitems)

        # Get metrics value
        for item in zabbixitems:
            hostid = item['hostid']
            itemid = item['itemid']
            value_type = item['value_type']

            
            history = self.get_history(token, hostid, itemid, value_type, zabbix_api)
            self.log.debug("Getting history for item %s: %s", itemid, history)
            try:
                dd_metricname = 'zabbix.' + item['name'].replace(' ', '_')
                dd_metricvalue = history[0]['value']
                dd_hostname = hostdic[hostid].replace(' ', '_')
            except Exception as e:
                self.log.debug("Unable to get metric for item: %s", itemid)
            else:
                self.gauge(dd_metricname, dd_metricvalue, tags=self.tags, hostname=dd_hostname, device_name=None)

        # Revoke token
        result = self.logout(token, zabbix_api)
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=self.tags)

