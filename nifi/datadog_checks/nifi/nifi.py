# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import requests
import time
from collections import namedtuple

from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException

# EndPoint information https://nifi.apache.org/docs/nifi-docs/rest-api/index.html
ENDPOINT = 'nifi-api/system-diagnostics'

GaugeInfo = namedtuple('GaugeInfo', ['type', 'metric'])


class NiFiCheck(AgentCheck):

    def check(self, instance):
        service_check_metric_name = 'nifi.instance.http_check'
        timeout = 10

        if 'url' not in instance:
            raise CheckException("No url defined for Nifi instance")
        url = instance.get('url')
        url = "{0}/{1}".format(url, ENDPOINT)

        instance_tags = instance.get('tags', [])
        self.log.info('Connecting to Nifi instance {0}'.format(url))
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
        except requests.exceptions.Timeout as e:
            self.service_check(service_check_metric_name,  self.WARNING, tags=instance_tags, message=str(e))
            return
        except Exception as e:
            self.service_check(service_check_metric_name, self.CRITICAL, tags=instance_tags)
            raise CheckException(e)
        self.service_check(service_check_metric_name, self.OK, tags=instance_tags)
        # Obtain all the key metrics from Nifi to send to DataDog
        for point in NiFiCheck.get_system_metrics(r.json()):
            if type(point.metric) is int:
                self.rate(point.type, point.metric, tags=instance_tags)
            else:
                self.gauge(point.type, point.metric, tags=instance_tags)
            time.sleep(1)

    @staticmethod
    def get_system_metrics(response):
        stats = list()
        # Get NiFi system information
        stats.append(GaugeInfo('nifi.systemdiagnostics.aggregatesnapshot.freenonheap.bytes',
                               response['systemDiagnostics']['aggregateSnapshot']['freeNonHeapBytes']))
        stats.append(GaugeInfo('nifi.systemdiagnostics.aggregatesnapshot.usedheap.bytes',
                               response['systemDiagnostics']['aggregateSnapshot']['usedHeapBytes']))
        # Had to remove the percentage symbol given in the Json
        stats.append(GaugeInfo('nifi.systemdiagnostics.aggregatesnapshot.heaputilization.percentage',
                               response['systemDiagnostics']['aggregateSnapshot']['heapUtilization'][:-1]))
        stats.append(GaugeInfo('nifi.systemdiagnostics.aggregatesnapshot.processorloadaverage.percentage',
                               response['systemDiagnostics']['aggregateSnapshot']['processorLoadAverage']))
        return stats
