import json
import os
from typing import List

from datadog_checks.unifi_console.client import Client
from datadog_checks.unifi_console.device import Device
from datadog_checks.unifi_console.types import ControllerInfo
from datadog_checks.unifi_console.UAP import UAP
from datadog_checks.unifi_console.UDM import UDM
from datadog_checks.unifi_console.USG import USG
from datadog_checks.unifi_console.USW import USW
from datadog_checks.unifi_console.USX import USX
from tests.common import HERE


class MockedAPI(object):
    def __init__(self, config, http, log) -> None:
        self.config = config

    def login(self):
        pass

    def status(self):
        with open(os.path.join(HERE, "fixtures", "status_valid.json")) as f:
            return ControllerInfo(json.load(f))

    def get_devices_info(self):
        with open(os.path.join(HERE, "fixtures", "device_metrics.json")) as f:

            resp = json.load(f)
            devices: List[Device] = []

            for dev in resp["data"]:
                assetType = dev["type"]

                if assetType == "uap":
                    devices.append(UAP(dev))
                elif assetType == "ugw" or assetType == "usg":  # in case they ever fix the name in the api.
                    devices.append(USG(dev))
                elif assetType == "usw":
                    devices.append(USW(dev))
                elif assetType == "udm":
                    devices.append(UDM(dev))
                elif assetType == "usx":
                    devices.append(USX(dev))

            return devices

    def get_clients_info(self) -> List[Client]:
        with open(os.path.join(HERE, "fixtures", "client_metrics.json")) as f:

            resp = json.load(f)
            clients: List[Client] = []

            for cli in resp["data"]:
                clients.append(Client(cli))

            return clients
