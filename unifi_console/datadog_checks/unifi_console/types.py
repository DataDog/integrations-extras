from typing import List

from attr import dataclass


class APIConnectionError(Exception):
    pass


class ControllerInfo(object):
    def __init__(self, about_info) -> None:
        self.up = about_info["meta"]["up"]
        self.version = about_info["meta"]["server_version"]
        self.uuid = about_info["meta"]["uuid"]

        self.fullName = "Unifi Controller {} uuid: {}".format(self.version, self.uuid)


@dataclass
class Check:
    name: str
    value: float
    tags: List[str]
