# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from collections import namedtuple
import httplib


from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException

NiFiHost = namedtuple('NiFiHost', ['Host', 'Port'])
# EndPoint information https://nifi.apache.org/docs/nifi-docs/rest-api/index.html
EndPoints = ['system-diagnostics', 'flow/cluster/summary']
ENDPOINT = '/nifi-api/system-diagnostics'


class NiFiCheck(AgentCheck):

    def check(self, instance):
        nifi = NiFiCheck.__GetNiFiHost(instance)
        con = httplib.HTTPConnection(nifi.Host, nifi.Port, timeout=10)
        if 'ssl' in instance:
            ''' Add the NiFi P12 and Password to the Http Connection '''
            pass
        try:
            con.request("GET", ENDPOINT)
            req = con.getresponse()

            if req.status in [400, 401, 404, 403]:
                raise CheckException('Unable to connect to endpoint')
            data = req.read()
            print('Data I have is:', data)
        except httplib.HTTPException as e:
            self.service_check(self.CRITICAL, e)
        except Exception as e:
            print("I have done something wrong")
            self.service_check(self.CRITICAL, e)

    @staticmethod
    def __GetNiFiHost(instance):
        if 'host' not in instance:
            raise CheckException('No host defined for nifi instance')
        return NiFiHost(instance.get('host'), instance.get('port', '8080'))
