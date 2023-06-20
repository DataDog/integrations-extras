import functools
import json
import logging
from typing import Callable, List, TypeVar, cast

import requests
from requests import HTTPError, Timeout
from urllib3.exceptions import InsecureRequestWarning

from datadog_checks.unifi_console.client import Client
from datadog_checks.unifi_console.config import UnifiConfig
from datadog_checks.unifi_console.device import Device
from datadog_checks.unifi_console.errors import APIConnectionError, Unauthorized
from datadog_checks.unifi_console.types import (
    APIClientPath,
    APIDevicePath,
    APILoginPath,
    APILoginPathNew,
    APIPrefixNew,
    APIStatusPath,
    ControllerInfo,
)
from datadog_checks.unifi_console.UAP import UAP
from datadog_checks.unifi_console.UDM import UDM
from datadog_checks.unifi_console.USG import USG
from datadog_checks.unifi_console.USW import USW
from datadog_checks.unifi_console.USX import USX

CallableT = TypeVar("CallableT", bound=Callable)


def smart_retry(f: Callable) -> CallableT:
    """A function decorated with this `@smart_retry` will trigger a new authentication if it fails. The function
    will then be retried.
    This is useful when the integration keeps a semi-healthy connection to the Controller API"""

    @functools.wraps(f)
    def wrapper(api_instance, *args, **kwargs):
        try:
            return f(api_instance, *args, **kwargs)
        except Unauthorized as e:

            api_instance.log.debug(
                "An exception occurred when executing %s: %s. Refreshing the connection to the Controller and retrying",
                f.__name__,
                e,
            )
            api_instance.login()
            return f(api_instance, *args, **kwargs)

        except Exception:
            raise

    return cast(CallableT, wrapper)


class Unifi:
    def __init__(self, config: UnifiConfig, http, log: logging.LoggerAdapter) -> None:
        self.config: UnifiConfig = config
        self.log: logging.LoggerAdapter = log
        self.http: requests = http
        self.csrf = ""
        self.fingerprints = []
        self.new = False

        self.__checkNewStyleAPI()

    def login(self):
        payload = json.dumps({"username": self.config.user, "password": self.config.password})
        headers = {"Content-Type": "application/json"}

        try:
            resp = self.http.post(
                self.config.url + self.__path(APILoginPath),
                data=payload,
                headers=headers,
            )
            resp.raise_for_status()
        except Exception as e:
            err_msg = "Connection to {} failed: {}".format(self.__path(APILoginPath), e)
            raise APIConnectionError(err_msg) from None

    def status(self) -> ControllerInfo:
        resp = self._get_json(APIStatusPath)
        return ControllerInfo(resp)

    @smart_retry
    def get_devices_info(self) -> List[Device]:
        resp = self._get_json(self.__path(APIDevicePath.format(self.config.site)))

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

    @smart_retry
    def get_clients_info(self) -> List[Client]:
        resp = self._get_json(self.__path(APIClientPath.format(self.config.site)))

        clients: List[Client] = []

        for cli in resp["data"]:
            clients.append(Client(cli))

        return clients

    def __checkNewStyleAPI(self):
        """This function runs when `Unifi()` is called to
        check if this is a newer controller or not. If it is, we set new to True.
        Setting new to True makes the __path() method return different (new) paths.

                Raises:
                    Unauthorized:
        """
        self.log.debug("Requesting %s/ to determine API paths", self.config.url)
        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            resp = requests.get(self.config.url + "/", verify=False, allow_redirects=False)
            resp.raise_for_status()
            if resp.status_code == 200:
                self.new = True
        except (HTTPError, ConnectionError) as e:
            self.log.warning(
                "Couldn't connect to URL: %s with exception: %s. Please verify the address is reachable",
                self.config.url,
                e,
            )
            if e.response.status_code == 401:
                raise Unauthorized()

            raise
        except Timeout as e:
            self.log.warning("Connection timeout when connecting to %s: %s", self.config.url, e)
            raise

    def __path(self, path: str) -> str:
        """returns the correct api path based on the new variable

        Args:
            path (str): the targeted API path

        Returns:
            str: the correct API path
        """
        if self.new:
            if path == APILoginPath:
                return APILoginPathNew

            if not path.startswith(APIPrefixNew) and path != APILoginPathNew:
                return APIPrefixNew + path

        return path

    def _get_json(self, path) -> dict:
        url = self.config.url + self.__path(path)
        try:
            resp = self.http.get(url)
            resp.raise_for_status()
            return resp.json()
        except (HTTPError, ConnectionError) as e:
            self.log.warning(
                "Couldn't connect to URL: %s with exception: %s. Please verify the address is reachable",
                url,
                e,
            )
            if e.response.status_code == 401:
                raise Unauthorized()

            raise
        except Timeout as e:
            self.log.warning("Connection timeout when connecting to %s: %s", url, e)
            raise
