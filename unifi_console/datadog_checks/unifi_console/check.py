from typing import cast

from datadog_checks.base import AgentCheck
from datadog_checks.unifi_console.api import APIConnectionError, UnifiAPI
from datadog_checks.unifi_console.config import UnifiConfig
from datadog_checks.unifi_console.mertrics import Metric
from datadog_checks.unifi_console.types import Check, ControllerInfo


class UnifiConsoleCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = "unifi"

    def __init__(self, name, init_config, instances):
        super(UnifiConsoleCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        self._config = UnifiConfig(self.instance, self.init_config, self.log)
        self.api = UnifiAPI(self._config, self.http, self.log)

        # try to login a initialization to prevent login for every request
        self.check_initializations.append(self._initiate_api_connection)

    def _initiate_api_connection(self):
        try:
            self.log.debug(
                "Connecting to the Unifi Controller Api %s with username %s...",
                self._config.url,
                self._config.user,
            )
            self.api.connect()
            self.log.debug("Connected")
        except APIConnectionError:
            self.log.error("Cannot authenticate to Unifi Controller API. The check will not run.")
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self._config.tags,
                hostname=None,
            )
            raise

    def check(self, _):

        # Assert the health of the Unifi API by getting the status, and submit the service_check accordingly
        status = cast(ControllerInfo, None)
        try:
            status = self.api.status()
            print(status)

        except Exception:
            # Explicitly do not attach any host to the service checks.
            self.log.exception("The Unifi API is not responding. The check will not run.")
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                tags=self._config.tags,
                hostname=None,
            )
            raise
        else:
            self.service_check("can_connect", AgentCheck.OK, tags=self._config.tags, hostname=None)
        finally:
            self._submit_healthy_metrics(status, self._config.tags)

        # Collect devices metrics
        try:
            devices = self.api.get_devices_info()
        except Exception:
            self.log.exception("Exception raised during the get_devices_info.")
            raise
        else:
            for device in devices:
                self._submit_metrics(device.metrics)
                self._submit_checks(device.checks)

        # Collect clients metrics
        try:
            clients = self.api.get_clients_info()
        except Exception:
            self.log.exception("Exception raised during the get_clients_info.")
            raise
        else:
            for c in clients:
                self._submit_metrics(c.metrics)

    def _submit_healthy_metrics(self, controller_info: ControllerInfo, tags):
        health_status = AgentCheck.CRITICAL
        if isinstance(controller_info, ControllerInfo) and controller_info.up:
            health_status = AgentCheck.OK
        self.service_check("healthy", health_status, tags=tags)
        self.gauge("healthy", int(health_status == AgentCheck.OK), tags=tags)

    def _submit_metrics(self, metrics):
        for m in metrics:
            if not isinstance(m, Metric):
                continue
            tags = m.tags + self._config.tags
            if m.type == "gauge":
                self.gauge(m.name, m.value, tags=tags, hostname=None)
            elif m.type == "count":
                self.count(m.name, m.value, tags=tags, hostname=None)
            elif m.type == "rate":
                self.rate(m.name, m.value, tags=tags, hostname=None)

    def _submit_checks(self, checks):
        for c in checks:
            if isinstance(c, Check):
                self.service_check(c.name, c.value, tags=c.tags)
