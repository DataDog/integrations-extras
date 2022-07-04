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
        wanted_tags = [
            {"key": "id", "value": "_id"},
            {"key": "architecture", "value": "architecture"},
            {"key": "kernel_version", "value": "kernel_version"},
            {"key": "model", "value": "model"},
            {"key": "device", "value": "name"},
            {"key": "device_version", "value": "version"},
        ]
        for t in wanted_tags:
            if t["value"] in device_info:
                tags.append("{}:{}".format(t["key"], device_info[t["value"]]))

        self.tags = tags

    def _get_base_metrics(self, device_info) -> List[Metric]:

        if device_info["state"] == 1:
            self.checks.append(Check("device", AgentCheck.OK, self.tags))
        else:
            self.checks.append(Check("device", AgentCheck.CRITICAL, self.tags))

        metrics: List[Metric] = []
        wanted_metrics = [
            {"key": "device.status", "metric": "state"},
            {"key": "device.uptime", "metric": "uptime"},
            {"key": "device.clients", "metric": "num_sta"},
            {"key": "device.satisfaction", "metric": "satisfaction"},
            {"key": "device.guests", "metric": "guest-num_sta"},
        ]

        for m in wanted_metrics:
            if m["metric"] in device_info:
                metrics.append(
                    Gauge(
                        m["key"],
                        device_info[m["metric"]],
                        self.tags,
                    )
                )

        if "system-stats" in device_info:
            wanted_system_stats = [
                {"key": "device.system.cpu.pct", "metric": "cpu"},
                {"key": "device.system.mem.pct", "metric": "mem"},
            ]
            for m in wanted_system_stats:
                if m["metric"] in device_info["system-stats"]:
                    metrics.append(
                        Gauge(
                            m["key"],
                            device_info["system-stats"][m["metric"]],
                            self.tags,
                        )
                    )

        if "sys_stats" in device_info:
            wanted_sys_stats = [
                {"key": "device.system.mem.used", "metric": "mem_used"},
                {"key": "device.system.mem.total", "metric": "mem_total"},
                {"key": "device.system.mem.buffer", "metric": "mem_buffer"},
            ]
            for m in wanted_sys_stats:
                if m["metric"] in device_info["sys_stats"]:
                    metrics.append(
                        Gauge(
                            m["key"],
                            device_info["sys_stats"][m["metric"]],
                            self.tags,
                        )
                    )

        self.metrics += metrics

    def _get_stats(self, device_info) -> List[Metric]:
        stats: List[Metric] = []

        wanted_metrics = [
            "tx_packets",
            "tx_bytes",
            "tx_errors",
            "tx_dropped",
            "tx_retries",
            "rx_packets",
            "rx_bytes",
            "rx_errors",
            "rx_dropped",
        ]

        if "stat" in device_info and "ap" in device_info["stat"]:
            for m in wanted_metrics:
                if m in device_info["stat"]["ap"]:
                    stats.append(
                        Gauge(
                            "device.{}".format(m),
                            device_info["stat"]["ap"][m],
                            self.tags,
                        )
                    )

            self.metrics += stats

    def _get_uplink(self, device_info) -> List[Metric]:

        if "uplink" in device_info:

            uplink = device_info["uplink"]

            uplink_tags = []
            uplink_metrics: List[Metric] = []
            wanted_tags = ["name", "speed", "max_speed", "type", "uplink_source"]
            for t in wanted_tags:
                if t in uplink:
                    uplink_tags.append("uplink.{}:{}".format(t, uplink[t]))

            if "up" in uplink:
                up = int(device_info["uplink"]["up"] is True)
                uplink_metrics.append(Gauge("device.uplink.up", up, uplink_tags + self.tags))

                if device_info["uplink"]["up"]:
                    self.checks.append(Check("device.uplink", AgentCheck.OK, uplink_tags + self.tags))
                else:
                    self.checks.append(
                        Check(
                            "device.uplink",
                            AgentCheck.CRITICAL,
                            uplink_tags + self.tags,
                        )
                    )
            else:
                self.checks.append(Check("device.uplink", AgentCheck.WARNING, uplink_tags + self.tags))

            wanted_metrics = [
                "rx_bytes",
                "rx_dropped",
                "rx_errors",
                "rx_packets",
                "tx_bytes",
                "tx_dropped",
                "tx_errors",
                "tx_packets",
            ]
            for m in wanted_metrics:
                if m in uplink:
                    uplink_metrics.append(
                        Gauge(
                            "device.uplink.{}".format(m),
                            device_info["uplink"][m],
                            uplink_tags + self.tags,
                        )
                    )

            self.metrics += uplink_metrics
        else:
            self.checks.append(Check("device.uplink", AgentCheck.CRITICAL, self.tags))
