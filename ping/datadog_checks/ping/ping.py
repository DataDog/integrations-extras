# Licensed under Simplified BSD License (see LICENSE)

import platform
import re

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException
from datadog_checks.base.utils.subprocess_output import get_subprocess_output


class PingCheck(AgentCheck):
    SERVICE_CHECK_NAME = "network.ping.can_connect"

    def _load_conf(self, instance):
        # Fetch the configuration
        timeout = int(instance.get("timeout", 4))
        response_time = instance.get("collect_response_time", False)
        custom_tags = list(instance.get("tags", []))

        host = instance.get("host")
        if not host:
            raise CheckException("A valid host must be specified")

        return host, custom_tags, timeout, response_time

    def _exec_ping(self, timeout, target_host):
        precmd = []

        # Rough IPv6 format detection (keeping the original logic)
        try:
            split_url = target_host.split(":")
        except Exception:
            raise ConfigurationError(self.CONFIGURATION_ERROR_MSG.format(target_host, 'host', 'string'))

        # IPv6 address format: 2001:db8:85a3:8d3:1319:8a2e:370:7348
        if len(split_url) == 8:  # It may be an IPv6 address, let's verify the format
            for block in split_url:
                if len(block) != 4:
                    raise ConfigurationError(
                        self.CONFIGURATION_ERROR_MSG.format(target_host, 'IPv6 address', 'valid address')
                    )
            cmd = "ping6"
        else:
            cmd = "ping"

        if platform.system() == "Windows":  # pragma: nocover
            precmd = ["cmd", "/c", "chcp 437 &"]  # Set code page to English for non-US Windows
            countOption = "-n"
            timeoutOption = "-w"
            # The timeout option is in ms on Windows
            # https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping
            timeout = timeout * 1000
        elif platform.system() == "Darwin":
            countOption = "-c"
            if cmd == "ping":
                timeoutOption = "-W"  # Also in ms on Mac
                timeout = timeout * 1000
            else:
                # No timeout flag in Darwin's ping6; use -i (interval) as a neutral placeholder
                timeoutOption = "-i"
                timeout = 1
        else:
            # The timeout option is in seconds on Linux, leaving timeout as is
            # https://linux.die.net/man/8/ping
            countOption = "-c"
            timeoutOption = "-W"

        self.log.debug("Running: %s %s %s %s %s %s", cmd, countOption, "1", timeoutOption, timeout, target_host)

        # Allow empty stdout (avoid exception on timeout variants)
        lines, err, retcode = get_subprocess_output(
            precmd + [cmd, countOption, "1", timeoutOption, str(timeout), target_host],
            self.log,
            raise_on_empty_output=False,
        )
        self.log.debug("ping returned %s - stdout=%r - stderr=%r", retcode, lines, err)

        # Normalize text for error pattern matching
        text = "{} {}".format(lines or "", err or "")

        # Return structured result instead of raising on retcode==1
        if retcode == 0:
            return {"status": "ok", "output": lines or ""}

        # NEW: Detect name resolution / invalid address errors and raise an exception
        # even when retcode == 1. This is mainly intended for Windows environments.
        name_resolution_patterns = [
            "could not find host",
            "Name or service not known",
            "Temporary failure in name resolution",
            "unknown host",
            "invalid numeric address",
        ]

        if retcode == 1:
            # Treat unreachable / timeout as logical failure (no exception)
            lowered = text.lower()
            # Detect errors caused by invalid IP address etc.
            if any(p.lower() in lowered for p in name_resolution_patterns):
                raise CheckException("ping returned {}: {}".format(retcode, err or lines or "").strip())

            return {"status": "unreachable", "output": lines or "", "error": err or ""}

        # Other non-zero return codes indicate an execution error (name resolution, permissions, etc.)
        raise CheckException("ping returned {}: {}".format(retcode, err or lines or "").strip())

    def check(self, instance):
        host, custom_tags, timeout, response_time = self._load_conf(instance)
        custom_tags.append(f"target_host:{host}")

        try:
            res = self._exec_ping(timeout, host)

            if res["status"] == "unreachable":
                # Logical failure (ping exit code 1): the check itself succeeds,
                # but the service check reports CRITICAL.
                self.log.info("%s is DOWN (ping exit 1: unreachable/timeout)", host)
                self.service_check(
                    self.SERVICE_CHECK_NAME,
                    AgentCheck.CRITICAL,
                    custom_tags,
                    message="host unreachable or timeout",
                )
                self.gauge(self.SERVICE_CHECK_NAME, 0, custom_tags)
                return

            # Successful ping: parse response time if available
            lines = res["output"]
            m = re.search(r"time[<=]([\d.]+)", lines)
            length = float(m.group(1)) if m else None

        except CheckException as e:
            # Real execution error (e.g. missing binary, permission, DNS failure)
            # The service check is marked UNKNOWN, and the check itself raises an error.
            self.log.info("%s check error (%s)", host, e)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.UNKNOWN, custom_tags, message=str(e))
            self.gauge(self.SERVICE_CHECK_NAME, 0, custom_tags)
            raise

        # Report response time (if collected)
        if response_time and length is not None:
            # The ping output time is usually in ms on both Linux and macOS
            self.gauge("network.ping.response_time", length, custom_tags)

        # Successful result: report OK and gauge=1
        self.log.debug("%s is UP", host)
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, custom_tags)
        self.gauge(self.SERVICE_CHECK_NAME, 1, custom_tags)
