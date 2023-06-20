from datadog_checks.unifi_console.device import Device

tags = [
    {"key": "architecture", "value": "architecture"},
    {"key": "kernel_version", "value": "kernel_version"},
]

metrics = [
    {"key": "device.tx_packets", "metric": "stat.sw.tx_packets"},
    {"key": "device.tx_bytes", "metric": "stat.sw.tx_bytes"},
    {"key": "device.tx_errors", "metric": "stat.sw.tx_errors"},
    {"key": "device.tx_dropped", "metric": "stat.sw.tx_dropped"},
    {"key": "device.tx_retries", "metric": "stat.sw.tx_retries"},
    {"key": "device.rx_packets", "metric": "stat.sw.rx_packets"},
    {"key": "device.rx_bytes", "metric": "stat.sw.rx_bytes"},
    {"key": "device.rx_errors", "metric": "stat.sw.rx_errors"},
    {"key": "device.rx_dropped", "metric": "stat.sw.rx_dropped"},
]


class USX(Device):
    """UXG represents all the data from the Ubiquiti Controller for a UniFi 10Gb Gateway."""

    def __init__(self, device_info: dict) -> None:
        self.custom_tags = tags
        self.custom_metrics = metrics

        super().__init__(device_info)
