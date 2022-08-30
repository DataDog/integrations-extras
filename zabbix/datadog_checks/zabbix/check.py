import json

from datadog_checks.base import AgentCheck, ConfigurationError

from .metrics import METRICS


class ZabbixCheck(AgentCheck):

    SERVICE_CHECK_NAME = "zabbix.can_connect"

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

        # Get metrics value
        for item in zabbixitems:
            hostid = item['hostid']
            itemid = item['itemid']
            value_type = item['value_type']
            item_name = item['name']

            if item_name in METRICS:
                history = self.get_history(token, hostid, itemid, value_type, zabbix_api)
                mname = METRICS[item_name]

                # To avoid sending non-numeric values as gauge
                # https://www.zabbix.com/documentation/6.2/en/manual/api/reference/item/object?hl=value_typ#:~:text=ID%7D%2C%20%7BITEM.KEY%7D.-,value_type,-(required) # noqa: E501
                if value_type != '0' and value_type != '3':
                    self.log.debug("'{}' value is not numeric_float and numeric unsigned".format(item_name))
                    continue

                try:
                    dd_metricname = 'zabbix.' + mname
                    dd_metricvalue = history[0]['value']
                    dd_hostname = hostdic[hostid].replace(' ', '_')
                except Exception as e:
                    self.log.debug("Unable to get metric for item %s: %s", itemid, str(e))
                else:
                    self.gauge(dd_metricname, dd_metricvalue, tags=self.tags, hostname=dd_hostname, device_name=None)
            else:
                self.log.debug("Item name %s not found in metric mapping", item_name)

        # Revoke token
        result = self.logout(token, zabbix_api)
        self.log.debug("Logged out: %s", result)
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=self.tags)
