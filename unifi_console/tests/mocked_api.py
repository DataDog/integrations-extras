import json
import os

from tests.common import HERE

from datadog_checks.unifi_console.types import ControllerInfo, DeviceInfo


class MockedAPI(object):
    def __init__(self, config, http, log) -> None:
        self.config = config

    def connect(self):
        pass

    def status(self):
        with open(os.path.join(HERE, "fixtures", "status_valid.json")) as f:
            return ControllerInfo(json.load(f))

    def get_devices_metrics(self):
        with open(os.path.join(HERE, "fixtures", "device_metrics.json")) as f:

            resp = json.load(f)
            metrics = []
            for obj in resp["data"]:
                device = DeviceInfo(obj)
                metrics += device.metrics

            return metrics
