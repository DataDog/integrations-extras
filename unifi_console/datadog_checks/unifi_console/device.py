from typing import List

from datadog_checks.unifi_console.common import get_by_path
from datadog_checks.unifi_console.types import Check, Gauge, Metric

tags = [
    {"key": "id", "value": "_id"},
    {"key": "model", "value": "model"},
    {"key": "device", "value": "name"},
    {"key": "device_version", "value": "version"},
    {"key": "type", "value": "type"},
]

metrics = [
    {"key": "device.status", "metric": "state"},
    {"key": "device.uptime", "metric": "uptime"},
    {"key": "device.clients", "metric": "num_sta"},
    {"key": "device.guests", "metric": "guest-num_sta"},
    {"key": "device.system.cpu.pct", "metric": "system-stats.cpu"},
    {"key": "device.system.mem.pct", "metric": "system-stats.mem"},
    {"key": "device.system.mem.used", "metric": "sys_stats.mem_used"},
    {"key": "device.system.mem.total", "metric": "sys_stats.mem_total"},
    {"key": "device.system.mem.buffer", "metric": "sys_stats.mem_buffer"},
]


class Device:
    name: str = ""
    metrics: List[Metric] = []
    checks: List[Check] = []
    tags: List[str] = []

    __requested_tags = []
    __requested_metrics = []
    custom_tags = []
    custom_metrics = []

    def __init__(self, device_info: dict) -> None:
        self.__requested_tags = [*tags, *self.custom_tags]
        self.__requested_metrics = [*metrics, *self.custom_metrics]

        self.tags = []
        self.metrics = []
        self.checks = []

        self.name = get_by_path(device_info, "_id")
        self._get_tags(device_info)
        self._get_metrics(device_info)
        self._get_uplink(device_info)
        self._get_checks(device_info)

    def _get_tags(self, device_info: dict) -> List[str]:
        for t in self.__requested_tags:
            tag_value = get_by_path(device_info, t["value"])
            if tag_value is not None:
                self.tags.append("{}:{}".format(t["key"], tag_value))

    def _get_metrics(self, device_info: dict) -> None:
        for m in self.__requested_metrics:
            value = get_by_path(device_info, m["metric"])
            if value is not None:
                self.metrics.append(Gauge(m["key"], float(value), self.tags))

    def _get_uplink(self, device_info: dict) -> None:

        if "uplink" not in device_info:
            self.checks.append(Check("device.uplink", 2, self.tags))
            return

        uplink_tags = []
        wanted_tags = [
            "uplink.name",
            "uplink.speed",
            "uplink.max_speed",
            "uplink.type",
            "uplink.uplink_source",
        ]

        wanted_metrics = [
            {"key": "device.uplink.rx_bytes", "metric": "uplink.rx_bytes"},
            {"key": "device.uplink.rx_dropped", "metric": "uplink.rx_dropped"},
            {"key": "device.uplink.rx_errors", "metric": "uplink.rx_errors"},
            {"key": "device.uplink.rx_packets", "metric": "uplink.rx_packets"},
            {"key": "device.uplink.tx_bytes", "metric": "uplink.tx_bytes"},
            {"key": "device.uplink.tx_dropped", "metric": "uplink.tx_dropped"},
            {"key": "device.uplink.tx_errors", "metric": "uplink.tx_errors"},
            {"key": "device.uplink.tx_packets", "metric": "uplink.tx_packets"},
        ]

        for t in wanted_tags:
            tag_value = get_by_path(device_info, t)
            if tag_value is not None:
                uplink_tags.append("{}:{}".format(t, tag_value))

        up = get_by_path(device_info, "uplink.up")
        if up is not None:
            self.metrics.append(Gauge("device.uplink.up", int(up is True), uplink_tags + self.tags))

            if up:
                self.checks.append(Check("device.uplink", 0, uplink_tags + self.tags))
            else:
                self.checks.append(
                    Check(
                        "device.uplink",
                        2,
                        uplink_tags + self.tags,
                    )
                )
        else:
            self.checks.append(Check("device.uplink", 1, uplink_tags + self.tags))

        for m in wanted_metrics:
            value = get_by_path(device_info, m["metric"])
            if value is not None:
                self.metrics.append(Gauge(m["key"], float(value), uplink_tags + self.tags))

    def _get_checks(self, device_info: dict) -> None:
        if device_info["state"] == 1:
            self.checks.append(Check("device", 0, self.tags))
        else:
            self.checks.append(Check("device", 2, self.tags))
