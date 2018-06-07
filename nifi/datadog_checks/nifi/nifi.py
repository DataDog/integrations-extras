# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import requests
import time
from collections import namedtuple
from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException

# EndPoint information https://nifi.apache.org/docs/nifi-docs/rest-api/index.html
ENDPOINT = '/nifi-api/system-diagnostics'

GuageInfo = namedtuple('GuageInfo', ['type', 'metric'])


class NiFiCheck(AgentCheck):

    def check(self, instance):
        if 'host' not in instance:
            raise CheckException("No host defined for nifi instance")
        nifi = instance.get('host')
        instance_tags = instance.get('tags', [])
        self.log.info('Connecting to nifi instance')
        try:
            r = requests.get(nifi + ENDPOINT, timeout=10)
            r.raise_for_status()
        except requests.exception.Timeout as e:
            self.service_check('nifi.instance.http_check',
                               self.WARNING,
                               tags=instance_tags,
                               message=str(e))
            return
        except Exception as e:
            self.service_check('nifi.instance.http_check', self.CRITICAL,
                               tags=instance_tags)
            raise CheckException(e)
        self.service_check('nifi.instance.http_check', self.OK, tags=instance_tags)
        # Obtain all the key metrics from nifi to send to DataDog
        for point in NiFiCheck.getSystemMetrics(r.json()):
            try:
                v = float(point.metric)
                self.gauge(point.type, v, tags=instance_tags)
            except ValueError:
                self.rate(point.type, point.metric, tags=instance_tags)
            time.sleep(1)

    @staticmethod
    def getSystemMetrics(response):
        stats = []
        # Get NiFi system information
        point = GuageInfo('nifi.systemdiagnostics.aggregatesnapshot.freenonheap.bytes',
                          response['systemDiagnostics']['aggregateSnapshot']['freeNonHeapBytes'])
        stats.append(point)
        point = GuageInfo('nifi.systemdiagnostics.aggregatesnapshot.usedheap.bytes',
                          response['systemDiagnostics']['aggregateSnapshot']['usedHeapBytes'])
        stats.append(point)
        # Had to remove the percentage symbol given in the Json
        point = GuageInfo('nifi.systemdiagnostics.aggregatesnapshot.heaputilization.percentage',
                          response['systemDiagnostics']['aggregateSnapshot']['heapUtilization'][:-1])
        stats.append(point)
        point = GuageInfo('nifi.systemdiagnostics.aggregatesnapshot.processorloadaverage.percentage',
                          response['systemDiagnostics']['aggregateSnapshot']['processorLoadAverage'])
        return stats
