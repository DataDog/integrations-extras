from typing import List

from datadog_checks.unifi_console.mertrics import Gauge, Metric
from datadog_checks.unifi_console.types import Check


class ClientInfo(object):
    metrics: List[Metric] = []
    checks: List[Check] = []
    tags: List[str] = []

    def __init__(self, client_info) -> None:
        self._get_tags(client_info)
        self._get_metrics(client_info)

    def _get_tags(self, client_info) -> List[str]:
        tags = []
        tags.append("id:{}".format(client_info["_id"]))
        tags.append("radio_name:{}".format(client_info["radio_name"]))
        if "name" in client_info: 
            tags.append("device:{}".format(client_info["name"]))
        elif "hostname" in client_info:
            tags.append("device:{}".format(client_info["hostname"]))
        tags.append("channel:{}".format(client_info["channel"]))
        tags.append("radio:{}".format(client_info["radio"]))
        tags.append("radio_proto:{}".format(client_info["radio_proto"]))
        tags.append("oui:{}".format(client_info["oui"]))

        self.tags = tags

    def _get_metrics(self, client_info) -> List[Metric]:
        metrics: List[Metric] = []
        metrics.append(Gauge("client.up", 1, self.tags))
        metrics.append(Gauge("client.satisfaction", client_info["satisfaction"], self.tags))
        metrics.append(Gauge("client.signal", client_info["signal"], self.tags))
        metrics.append(Gauge("client.noise", client_info["noise"], self.tags))
        metrics.append(Gauge("client.uptime", client_info["uptime"], self.tags))
        metrics.append(Gauge("client.tx_bytes", client_info["tx_bytes"], self.tags))
        metrics.append(Gauge("client.rx_bytes", client_info["rx_bytes"], self.tags))
        metrics.append(Gauge("client.tx_packets", client_info["tx_packets"], self.tags))
        metrics.append(Gauge("client.rx_packets", client_info["rx_packets"], self.tags))
        metrics.append(Gauge("client.tx_retries", client_info["tx_retries"], self.tags))
        metrics.append(Gauge("client.tx_rate", client_info["tx_rate"], self.tags))
        metrics.append(Gauge("client.rx_rate", client_info["rx_rate"], self.tags))

        self.metrics += metrics
