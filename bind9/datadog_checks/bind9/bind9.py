# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import datetime

import requests
import xml.etree.ElementTree as ET

from datadog_checks.base import AgentCheck, ConfigurationError


class Bind9Check(AgentCheck):
    BIND_SERVICE_CHECK = "bind9.can_connect"
    QUERY_ARRAY = ["opcode", "qtype", "nsstat", "zonestat", "resstat", "sockstat"]

    def check(self, instance):
        dns_url = instance.get('url')

        if not dns_url:
            raise ConfigurationError('The statistic channel URL must be specified in the configuration')

        self.service_check(self.BIND_SERVICE_CHECK, AgentCheck.OK,
                           message='Connection to %s was successful' % dns_url)

        root = self.getStatsFromUrl(dns_url)
        self.collectTimeMetric(root, 'boot-time')
        self.collectTimeMetric(root, 'config-time')
        self.collectTimeMetric(root, 'current-time')

        for counter in self.QUERY_ARRAY:
            self.collectServerMetric(root[0], counter)

    def getStatsFromUrl(self, dns_url):
        try:
            response = requests.get(dns_url)
            response.raise_for_status()
        except Exception:
            self.service_check(self.BIND_SERVICE_CHECK, AgentCheck.CRITICAL, message="stats cannot be taken")
            raise

        root = ET.fromstring(response.text)
        return root

    def DateTimeToEpoch(self, DateTime):
        year = int(DateTime[0:4])
        month = int(DateTime[5:7])
        date = int(DateTime[8:10])
        hour = int(DateTime[11:13])
        minutes = int(DateTime[14:16])
        seconds = int(DateTime[17:19])
        return datetime.datetime(year, month, date, hour, minutes, seconds).strftime('%s')

    def collectTimeMetric(self, root, metricName):
        for name in root.iter(metricName):
            self.SendMetricsToAgent(metricName, self.DateTimeToEpoch(name.text))

    def collectServerMetric(self, root, queryType):
        for counter in root.iter("counters"):
            if counter.get('type') == queryType:
                for query in counter:
                    self.SendMetricsToAgent('{}_{}'.format(queryType, query.get('name')), query.text)

    def SendMetricsToAgent(self, metricName, metricValue):
        self.gauge('bind9.{}'.format(metricName), metricValue)
