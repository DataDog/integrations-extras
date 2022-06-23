from typing import List

from datadog_checks.base import AgentCheck
from datadog_checks.unifi_console.mertrics import Gauge, Metric
from datadog_checks.unifi_console.types import Check


class DeviceInfo(object):

    metrics: List[Metric] = []
    checks: List[Check] = []
    tags: List[str] = []

    def __init__(self, device_info) -> None:
        self._get_tags(device_info)

        self._get_base_metrics(device_info)

        # Stats
        self._get_stats(device_info)

        # Uplink
        self._get_uplink(device_info)

    def _get_tags(self, device_info) -> List[str]:
        tags = []
        tags.append("id:{}".format(device_info["_id"]))
        tags.append("architecture:{}".format(device_info["architecture"]))
        tags.append("kernel_version:{}".format(device_info["kernel_version"]))
        tags.append("model:{}".format(device_info["model"]))
        tags.append("device:{}".format(device_info["name"]))
        tags.append("device_version:{}".format(device_info["version"]))

        self.tags = tags

    def _get_base_metrics(self, device_info) -> List[Metric]:

        if device_info["state"] == 1:
            self.checks.append(Check('device', AgentCheck.OK, self.tags))
        else:
            self.checks.append(Check('device', AgentCheck.CRITICAL, self.tags))

        metrics: List[Metric] = []
        metrics.append(Gauge("device.status", device_info["state"], self.tags))
        metrics.append(Gauge("device.uptime", device_info["uptime"], self.tags))
        metrics.append(Gauge("device.clients", device_info["num_sta"], self.tags))
        metrics.append(Gauge("device.satisfaction", device_info["satisfaction"], self.tags))
        metrics.append(Gauge("device.system.cpu.pct", device_info["system-stats"]["cpu"], self.tags))
        metrics.append(
            Gauge(
                "device.system.mem.used",
                device_info["sys_stats"]["mem_used"],
                self.tags,
            )
        )
        metrics.append(
            Gauge(
                "device.system.mem.total",
                device_info["sys_stats"]["mem_total"],
                self.tags,
            )
        )
        metrics.append(
            Gauge(
                "device.system.mem.buffer",
                device_info["sys_stats"]["mem_buffer"],
                self.tags,
            )
        )
        metrics.append(Gauge("device.system.mem.pct", device_info["system-stats"]["mem"], self.tags))

        metrics.append(Gauge("device.guests", device_info["guest-num_sta"], self.tags))

        self.metrics += metrics

    def _get_stats(self, device_info) -> List[Metric]:
        stats: List[Metric] = []
        stats.append(Gauge("device.tx_packets", device_info["stat"]["ap"]["tx_packets"], self.tags))
        stats.append(Gauge("device.tx_bytes", device_info["stat"]["ap"]["tx_bytes"], self.tags))
        stats.append(Gauge("device.tx_errors", device_info["stat"]["ap"]["tx_errors"], self.tags))
        stats.append(Gauge("device.tx_dropped", device_info["stat"]["ap"]["tx_dropped"], self.tags))
        stats.append(Gauge("device.tx_retries", device_info["stat"]["ap"]["tx_retries"], self.tags))
        stats.append(Gauge("device.rx_packets", device_info["stat"]["ap"]["rx_packets"], self.tags))
        stats.append(Gauge("device.rx_bytes", device_info["stat"]["ap"]["rx_bytes"], self.tags))
        stats.append(Gauge("device.rx_errors", device_info["stat"]["ap"]["rx_errors"], self.tags))
        stats.append(Gauge("device.rx_dropped", device_info["stat"]["ap"]["rx_dropped"], self.tags))

        self.metrics += stats

    def _get_uplink(self, device_info) -> List[Metric]:
        # Uplink
        uplink_tags = []
        uplink_tags.append("uplink.name:{}".format(device_info["uplink"]["name"]))
        uplink_tags.append("uplink.speed:{}".format(device_info["uplink"]["speed"]))
        uplink_tags.append("uplink.max_speed:{}".format(device_info["uplink"]["max_speed"]))
        uplink_tags.append("uplink.type:{}".format(device_info["uplink"]["type"]))
        uplink_tags.append("uplink.uplink_source:{}".format(device_info["uplink"]["uplink_source"]))

        if device_info["uplink"]["up"]:
            self.checks.append(Check('device.uplink', AgentCheck.OK, uplink_tags + self.tags))
        else:
            self.checks.append(Check('device.uplink', AgentCheck.CRITICAL, uplink_tags + self.tags))

        up = int(device_info["uplink"]["up"] is True)
        uplink_metrics: List[Metric] = []
        uplink_metrics.append(Gauge("device.uplink.up", up, uplink_tags + self.tags))
        uplink_metrics.append(
            Gauge(
                "device.uplink.rx_bytes",
                device_info["uplink"]["rx_bytes"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.rx_dropped",
                device_info["uplink"]["rx_dropped"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.rx_errors",
                device_info["uplink"]["rx_errors"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.rx_packets",
                device_info["uplink"]["rx_packets"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.tx_bytes",
                device_info["uplink"]["tx_bytes"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.tx_dropped",
                device_info["uplink"]["tx_dropped"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.tx_errors",
                device_info["uplink"]["tx_errors"],
                uplink_tags + self.tags,
            )
        )
        uplink_metrics.append(
            Gauge(
                "device.uplink.tx_packets",
                device_info["uplink"]["tx_packets"],
                uplink_tags + self.tags,
            )
        )

        self.metrics += uplink_metrics
