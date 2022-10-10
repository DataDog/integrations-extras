from typing import List

from attr import dataclass


class APIConnectionError(Exception):
    pass


class APIError(Exception):
    """API Error exceptions"""


class ControllerInfo(object):
    def __init__(self, about_info) -> None:
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
