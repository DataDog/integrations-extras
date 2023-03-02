from datadog_checks.unifi_console.device import Device

tags = []

metrics = []


class USG(Device):
    """USG represents all the data from the Ubiquiti Controller for a Unifi Security Gateway."""

    def __init__(self, device_info: dict) -> None:
        self.custom_tags = tags
        self.custom_metrics = metrics

        super().__init__(device_info)
