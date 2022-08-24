from typing import List

from datadog_checks.unifi_console.mertrics import Gauge, Metric
from datadog_checks.unifi_console.types import Check


class ClientInfo(object):
    name: str = ""
    metrics: List[Metric] = []
    checks: List[Check] = []
    tags: List[str] = []

    def __init__(self, client_info) -> None:
        self.name = client_info["_id"]
        self._get_tags(client_info)
        self._get_metrics(client_info)

    def _get_tags(self, client_info) -> List[str]:
        tags = []
        wanted_tags = [
            {"key": "id", "value": "_id"},
            {"key": "radio_name", "value": "radio_name"},
            {"key": "channel", "value": "channel"},
            {"key": "radio", "value": "radio"},
            {"key": "radio_proto", "value": "radio_proto"},
            {"key": "oui", "value": "oui"},
        ]
        if "name" in client_info:
            tags.append("device:{}".format(client_info["name"]))
        elif "hostname" in client_info:
            tags.append("device:{}".format(client_info["hostname"]))

        for t in wanted_tags:
            if t["value"] in client_info:
                tags.append("{}:{}".format(t["key"], client_info[t["value"]]))

        self.tags = tags

    def _get_metrics(self, client_info) -> List[Metric]:
        metrics: List[Metric] = []
        metrics.append(Gauge("client.up", 1, self.tags))

        wanted_metrics = [
            "satisfaction",
            "signal",
            "noise",
            "uptime",
            "tx_bytes",
            "rx_bytes",
            "tx_packets",
            "rx_packets",
            "tx_retries",
            "tx_rate",
            "rx_rate",
        ]

        for m in wanted_metrics:
            if m in client_info:
                metrics.append(Gauge("client.{}".format(m), client_info[m], self.tags))

        self.metrics += metrics
