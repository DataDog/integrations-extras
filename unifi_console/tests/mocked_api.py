import json
import os

from tests.common import HERE

from datadog_checks.unifi_console.client_info import ClientInfo
from datadog_checks.unifi_console.device_info import DeviceInfo
from datadog_checks.unifi_console.types import ControllerInfo


class MockedAPI(object):
    def __init__(self, config, http, log) -> None:
        self.config = config

    def connect(self):
        pass

    def status(self):
        with open(os.path.join(HERE, "fixtures", "status_valid.json")) as f:
            return ControllerInfo(json.load(f))

    def get_devices_info(self):
        with open(os.path.join(HERE, "fixtures", "device_metrics.json")) as f:

            resp = json.load(f)
            devices = []
            for obj in resp["data"]:
                devices.append(DeviceInfo(obj))

            return devices

    def get_clients_info(self):
        with open(os.path.join(HERE, "fixtures", "client_metrics.json")) as f:

            resp = json.load(f)
            clients = []
            for obj in resp["data"]:
                clients.append(ClientInfo(obj))

            return clients
