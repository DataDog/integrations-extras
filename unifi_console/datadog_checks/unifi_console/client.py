from typing import List

from datadog_checks.unifi_console.common import get_by_path
from datadog_checks.unifi_console.types import Check, Gauge, Metric

tags = [
    {"key": "id", "value": "_id"},
    {"key": "radio_name", "value": "radio_name"},
    {"key": "channel", "value": "channel"},
    {"key": "radio", "value": "radio"},
    {"key": "radio_proto", "value": "radio_proto"},
    {"key": "oui", "value": "oui"},
    {"key": "name", "value": "hostname"},
]

metrics = [
    {"key": "client.satisfaction", "metric": "satisfaction"},
    {"key": "client.signal", "metric": "signal"},
    {"key": "client.noise", "metric": "noise"},
    {"key": "client.uptime", "metric": "uptime"},
    {"key": "client.tx_bytes", "metric": "tx_bytes"},
    {"key": "client.rx_bytes", "metric": "rx_bytes"},
    {"key": "client.tx_packets", "metric": "tx_packets"},
    {"key": "client.rx_packets", "metric": "rx_packets"},
    {"key": "client.tx_retries", "metric": "tx_retries"},
    {"key": "client.tx_rate", "metric": "tx_rate"},
    {"key": "client.rx_rate", "metric": "rx_rate"},
]


class Client:
    name: str = ""
    metrics: List[Metric] = []
    checks: List[Check] = []
    tags: List[str] = []

    def __init__(self, client_info: dict) -> None:
        self.name = client_info["_id"]
        self._get_tags(client_info)
        self._get_metrics(client_info)

    def _get_tags(self, client_info: dict) -> List[str]:
        self.tags = []
        for t in tags:
            tag_value = get_by_path(client_info, t["value"])
            if tag_value is not None:
                self.tags.append("{}:{}".format(t["key"], tag_value))

    def _get_metrics(self, client_info: dict) -> None:
        self.metrics = []
        self.metrics.append(Gauge("client.up", 1.0, self.tags))
        for m in metrics:
            value = get_by_path(client_info, m["metric"])
            if value is not None:
                self.metrics.append(Gauge(m["key"], float(value), self.tags))
