from datadog_checks.unifi_console.device import Device

tags = []

metrics = [
    {"key": "device.satisfaction", "metric": "satisfaction"},
    {"key": "device.tx_packets", "metric": "stat.ap.tx_packets"},
    {"key": "device.tx_bytes", "metric": "stat.ap.tx_bytes"},
    {"key": "device.tx_errors", "metric": "stat.ap.tx_errors"},
    {"key": "device.tx_dropped", "metric": "stat.ap.tx_dropped"},
    {"key": "device.tx_retries", "metric": "stat.ap.tx_retries"},
    {"key": "device.rx_packets", "metric": "stat.ap.rx_packets"},
    {"key": "device.rx_bytes", "metric": "stat.ap.rx_bytes"},
    {"key": "device.rx_errors", "metric": "stat.ap.rx_errors"},
    {"key": "device.rx_dropped", "metric": "stat.ap.rx_dropped"},
]


class USW(Device):
    """USW represents all the data from the Ubiquiti Controller for a Unifi Switch."""

    def __init__(self, device_info: dict) -> None:
        self.custom_tags = tags
        self.custom_metrics = metrics

        super().__init__(device_info)
