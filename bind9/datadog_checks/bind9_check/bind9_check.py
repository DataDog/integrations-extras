# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import urllib2
import time
import datetime
import xml.etree.ElementTree as ET
from datadog_checks.checks import AgentCheck
from datadog_checks.errors import CheckException

class bind9_check(AgentCheck) :
    BIND_SERVICE_CHECK = "BIND9 service check"
    Query_Array=["opcode","qtype","nsstat","zonestat","resstat","sockstat"]

    def check(self, instance) :
        dns_url = instance.get('url')

        if not dns_url :
            raise CheckException('The statistic channel URL must be specified in the configuration')

        self.service_check(self.BIND_SERVICE_CHECK, AgentCheck.OK,
                           message='Connection to %s was successful' % dns_url)

        root = self.getStatsFromUrl(dns_url)
        self.collectTimeMetric(root[0], 'boot-time')
        self.collectTimeMetric(root[0], 'config-time')
        self.collectTimeMetric(root[0], 'current-time')

        for counter in self.Query_Array :
            self.collectServerMetric(root[0],counter)


    def getStatsFromUrl(self, dns_url) :
        try:
            xmlStats = urllib2.urlopen(dns_url)
        except (urllib2.URLError, urllib2.HTTPError) as e:
            self.service_check(self.BIND_SERVICE_CHECK,AgentCheck.CRITICAL, message= "stats cannot be taken")
            raise
        return xmlStats.getCode()

    def DateTimeToEpoch(self, DateTime) :

        year=int(DateTime[0:4])
        month=int(DateTime[5:7])
        date=int(DateTime[8:10])
        hour =int(DateTime[11:13])
        minutes = int(DateTime[14:16])
        seconds =int(DateTime[17:19])
        return datetime.datetime(year,month,date,hour,minutes,seconds).strftime('%s')

    def collectTimeMetric(self, root, metricName) :
        for name in root.iter(metricName) :
            self.SendMetricsToAgent(metricName, self.DateTimeToEpoch(name.text))

    def collectServerMetric(self, root, queryType) :
        for counter in root.iter("counters") :
            if counter.get('type') == queryType :
                for query in counter :
                    self.SendMetricsToAgent(queryType +'_'+ query.get('name'), query.text)

    def SendMetricsToAgent(self,metricName,metricValue) :
        self.gauge(metricName,metricValue)
