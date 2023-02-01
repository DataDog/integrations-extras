# APIRogueAP shows your neighbors' wifis.
from dataclasses import dataclass
from types import SimpleNamespace
from typing import List

APIRogueAP = "/api/s/{}/stat/rogueap"
# APIStatusPath shows Controller version.
APIStatusPath = "/status"
# APIEventPath contains UniFi Event data.
APIEventPath = "/api/s/{}/stat/event"
# APISiteList is the path to the api site list.
APISiteList = "/api/stat/sites"
# APISiteDPI is site DPI data.
APISiteDPI = "/api/s/{}/stat/sitedpi"
# APISiteDPI is site DPI data.
APIClientDPI = "/api/s/{}/stat/stadpi"
# APIClientPath is Unifi Clients API Path.
APIClientPath = "/api/s/{}/stat/sta"
# APIAllUserPath is Unifi Insight all previous Clients API Path.
APIAllUserPath = "/api/s/{}/stat/alluser"
# APINetworkPath is where we get data about Unifi networks.
APINetworkPath = "/api/s/{}/rest/networkconf"
# APIDevicePath is where we get data about Unifi devices.
APIDevicePath = "/api/s/{}/stat/device"
# APILoginPath is Unifi Controller Login API Path.
APILoginPath = "/api/login"
# APILoginPathNew is how we log into UDM 5.12.55+.
APILoginPathNew = "/api/auth/login"
# APILogoutPath is how we logout from UDM.
APILogoutPath = "/api/logout"
# APIEventPathIDS returns Intrusion Detection/Prevention Systems Events.
APIEventPathIDS = "/api/s/{}/stat/ips/event"
# APIEventPathAlarms contains the site alarms.
APIEventPathAlarms = "/api/s/{}/list/alarm"
# APIPrefixNew is the prefix added to the new API paths; except login. duh.
APIPrefixNew = "/proxy/network"
# APIAnomaliesPath returns site anomalies.
APIAnomaliesPath = "/api/s/{}/stat/anomalies"
APICommandPath = "/api/s/{}/cmd"
APIDevMgrPath = APICommandPath + "/devmgr"


class ControllerInfo(object):
    def __init__(self, about_info: SimpleNamespace) -> None:

        if "up" in about_info["meta"]:
            self.up = about_info["meta"]["up"]
        elif "rc" in about_info["meta"]:
            if about_info["meta"]["rc"] == 'ok':
                self.up = True
            else:
                self.up = False
        else:
            self.up = False

        if "server_version" in about_info["meta"]:
            self.version = about_info["meta"]["server_version"]
        else:
            self.version = ""

        if "uuid" in about_info["meta"]:
            self.uuid = about_info["meta"]["uuid"]
        else:
            self.uuid = ""

        self.fullName = "Unifi Controller {} uuid: {}".format(self.version, self.uuid)


@dataclass
class Check:
    name: str
    value: float
    tags: List[str]


@dataclass
class Metric:
    type: str
    name: str
    value: float
    tags: List[str]


def Gauge(name: str, value: float, tags: List[str]) -> Metric:
    return Metric("gauge", name, value, tags)


def Count(name: str, value: float, tags: List[str]) -> Metric:
    return Metric("count", name, value, tags)


def Rate(name: str, value: float, tags: List[str]) -> Metric:
    return Metric("rate", name, value, tags)
