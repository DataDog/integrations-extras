# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from datadog_checks.base import AgentCheck, ConfigurationError

EPOCH = datetime(1970, 1, 1)


class Bind9Check(AgentCheck):
    BIND_SERVICE_CHECK = "bind9.can_connect"
    QUERY_ARRAY = ["opcode", "qtype", "nsstat", "zonestat", "resstat", "sockstat"]

    def check(self, instance):
        # Always add the value of 'url' as a tag, and add all other instance tags to self
        self.tags = ["url:" + instance.get("url")] + [
            tag for tag in self.instance.get("tags", [])
        ]
        dns_url = instance.get("url")

        if not dns_url:
            raise ConfigurationError(
                "The statistic channel URL must be specified in the configuration"
            )

        root = self.getStatsFromUrl(dns_url)

        if root:
            self.service_check(
                self.BIND_SERVICE_CHECK,
                AgentCheck.OK,
                message="Connection to {} was successful".format(dns_url),
                tags=(self.tags),
            )
            self.collectTimeMetric(root, "boot-time")
            self.collectTimeMetric(root, "config-time")
            self.collectTimeMetric(root, "current-time")

            for counter in self.QUERY_ARRAY:
                self.collectServerMetric(root[0], counter)

    def getStatsFromUrl(self, dns_url):
        # Try to get timeout from init_config, otherwise default to 5 seconds
        timeout = self.init_config.get("timeout", str(5))

        try:
            response = requests.get(dns_url, timeout=timeout)
            response.raise_for_status()
        except:
            self.service_check(
                self.BIND_SERVICE_CHECK,
                AgentCheck.CRITICAL,
                message="Cannot connect to {} after {} seconds".format(
                    dns_url, timeout
                ),
                tags=(self.tags),
            )
            return None

        root = ET.fromstring(response.text)
        return root

    def DateTimeToEpoch(self, DateTime):
        # Ignore time zone
        DateTime = DateTime[:19]
        return int(
            (datetime.strptime(DateTime, "%Y-%m-%dT%H:%M:%S") - EPOCH).total_seconds()
        )

    def collectTimeMetric(self, root, metricName):
        for name in root.iter(metricName):
            self.SendMetricsToAgent(metricName, self.DateTimeToEpoch(name.text))

    def collectServerMetric(self, root, queryType):
        for counter in root.iter("counters"):
            if counter.get("type") == queryType:
                for query in counter:
                    self.SendMetricsToAgent(
                        "{}_{}".format(queryType, query.get("name")), query.text
                    )

    def SendMetricsToAgent(self, metricName, metricValue):
        self.gauge("bind9.{}".format(metricName), metricValue, tags=(self.tags))
