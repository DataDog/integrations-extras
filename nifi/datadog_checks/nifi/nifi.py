# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from collections import namedtupple
import httplib

from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException


NiFiHost    = namedtupple('NiFiHost',['Host','Port'])
# EndPoint information https://nifi.apache.org/docs/nifi-docs/rest-api/index.html
ENDPOINTS   = '/nifi-api/system-diagnostics'

class NiFiCheck(AgentCheck):

    def check(self, instance):
        nifi = NiFiCheck.__GetNiFiHost(instance)
        con  = httplib.HTTPConnection(nifi.Host, nifi.Port, timeout=10)
        if 'ssl' in instance:
            ''' Add the NiFi P12 and Password to the Http Connection '''
            pass
        try:
            # The main business logic
        except httplib.HTTPException as e:
            self.service_check(self.CRITICAL, e)

    @staticmethod
    def __GetNiFiHost(instance):
        if not 'host' in instance:
            raise CheckException('No host defined for nifi instance')
        return NiFiHost(instance.get('host'), instance.get('port', '8080'))
