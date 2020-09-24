import json

from datadog_checks.base import AgentCheck, ConfigurationError


class ZabbixCheck(AgentCheck):
    def request(self, zabbix_api, req_data):
        req_header = {
            'Content-Type': 'application/json-rpc',
        }
        res = self.http.post(zabbix_api, data=req_data.encode(), headers=req_header)
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
        response = self.request(zabbix_api, req_data)

        token = response.get('result')
        return token

    def logout(self, token, zabbix_api):
        req_data = json.dumps({'jsonrpc': '2.0', 'method': 'user.logout', 'params': {}, 'auth': token, 'id': 1})
        response = self.request(zabbix_api, req_data)
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
        return response.get('result')

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

            dd_metricname = 'zabbix.' + item['name'].replace(' ', '_')
            dd_metricvalue = history[0]['value']
            dd_hostname = hostdic[hostid].replace(' ', '_')

            self.gauge(dd_metricname, dd_metricvalue, tags=None, hostname=dd_hostname, device_name=None)

        # Revoke token
        result = self.logout(token, zabbix_api)
        self.log.debug(result)
