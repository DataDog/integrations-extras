import functools
import json
from typing import Any, Callable, List, TypeVar, cast

from requests import HTTPError, Timeout

from datadog_checks.unifi_console.client_info import ClientInfo
from datadog_checks.unifi_console.device_info import DeviceInfo
from datadog_checks.unifi_console.errors import Unauthorized
from datadog_checks.unifi_console.types import APIConnectionError, ControllerInfo

CallableT = TypeVar("CallableT", bound=Callable)


def smart_retry(f):
    # type: (Callable) -> CallableT
    """A function decorated with this `@smart_retry` will trigger a new authentication if it fails. The function
    will then be retried.
    This is useful when the integration keeps a semi-healthy connection to the vSphere API"""

    @functools.wraps(f)
    def wrapper(api_instance, *args, **kwargs):
        # type: (UnifiAPI, *Any, **Any) -> Any
        try:
            return f(api_instance, *args, **kwargs)
        except Unauthorized as e:

            api_instance.log.debug(
                "An exception occurred when executing %s: %s. Refreshing the connection to vCenter and retrying",
                f.__name__,
                e,
            )
            api_instance.connect()
            return f(api_instance, *args, **kwargs)

        except Exception:
            raise

    return cast(CallableT, wrapper)


class UnifiAPI(object):
    def __init__(self, config, http, log) -> None:
        self.config = config
        self.log = log
        self.http = http

    def connect(self) -> None:
        payload = json.dumps({"username": self.config.user, "password": self.config.password})
        headers = {"Content-Type": "application/json"}
        url = self.config.url + "/api/login"

        try:
            resp = self.http.post(url, data=payload, headers=headers)
            resp.raise_for_status()
        except Exception as e:
            err_msg = "Connection to {} failed: {}".format(self.config.url, e)
            raise APIConnectionError(err_msg)

    def status(self) -> ControllerInfo:
        url = self.config.url + "/status"

        resp = self._get_json(url)
        return ControllerInfo(resp)

    @smart_retry
    def get_devices_info(self) -> List[DeviceInfo]:
        url = "{}/api/s/{}/stat/device/".format(self.config.url, self.config.site)

        resp = self._get_json(url)

        devices: List[DeviceInfo] = []
        for obj in resp["data"]:
            devices.append(DeviceInfo(obj))

        return devices

    @smart_retry
    def get_clients_info(self) -> List[ClientInfo]:
        url = "{}/api/s/{}/stat/sta/".format(self.config.url, self.config.site)

        resp = self._get_json(url)

        clients: List[ClientInfo] = []
        for obj in resp["data"]:
            clients.append(ClientInfo(obj))

        return clients

    def _get_json(self, url):
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
