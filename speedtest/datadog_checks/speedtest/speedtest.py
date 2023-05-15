import json
import subprocess
from typing import Any, Dict  # noqa: F401

from datadog_checks.base import AgentCheck, ConfigurationError

MEGABYTE_TO_MEBIBYTE = 1048576.0 / 1000000.0


class SpeedtestCheck(AgentCheck):
    def check(self, *args, **kwargs):
        # type: (Dict[str, Any]) -> None
        host = self.instance.get("host")
        ip = self.instance.get("ip")
        interface = self.instance.get("interface")
        server_id = self.instance.get("server_id")
        tags = self.instance.get("tags") or []

        # test config for only **one** of the following above options
        c = 0
        for opt in (host, ip, interface, server_id):
            c += int(opt not in [None, ""])  # trick, int(bool) returns 0 if False, 1 if True
        if c > 1:
            raise ConfigurationError("Only one of `host`, `ip`, `interface` or `server_id` may be configured.")

        # Build command
        cmd = self._build_command(host, ip, interface, server_id)

        # call to speedtest cli on the system path
        try:
            payload = self._call_command(cmd)
            self._submit_data(payload, tags)
            self.service_check("speedtest.run", self.OK)
        except Exception as e:
            # something went wrong with this command
            msg = (
                "Be sure to have the speedtest CLI installed https://www.speedtest.net/apps/cli\n"
                + "Also be sure to accept the license as the datadog-agent user!\n"
                + "\t Linux/Mac: sudo su -s /bin/bash - dd-agent speedtest\n"
                + "\t Windows: runas /user:dd-agent speedtest\n"
            )
            self.log.exception(msg, e)
            self.service_check("speedtest.run", self.CRITICAL, message=str(e))

    def _build_command(self, host, ip, interface, server_id):
        # Build command
        cmd = "speedtest -f json -p no -A -P 8 "
        if host:
            cmd += " --host={}".format(host)
        if ip:
            cmd += " --ip={}".format(ip)
        if interface:
            cmd += " --interface={}".format(interface)
        if server_id:
            cmd += " --server-id={}".format(server_id)

        return cmd

    def _call_command(self, cmd):
        # we keep this private so we can mock this in tests
        result = subprocess.check_output(cmd, shell=True)
        payload = json.loads(result.strip())
        return payload

    def _submit_data(self, payload, tags):
        """
        submits data from json payload

        looks like:
        {
            "type": "result",
            "timestamp": <timestamp:ISO8601>,
            "ping":{
                "jitter": <float>,
                "latency": <float>,
            },
            "download":{
                "bandwidth": <float>,
                "bytes": <float>,
                "elapsed": <float>
            },
            "upload":{
                "bandwidth": <float>,
                "bytes": <float>,
                "elapsed": <float>
            },
            "packetLoss": <integer>,
            "isp": <string>,
            "interface":{
                "internalIp": <string>,
                "name": <string>,
                "macAddr": <string>,
                "isVpn": <boolean>,
                "externalIp": <string>
            },
            "server":{
                "id": <integer>,
                "name": <string>,
                "location": <string>,
                "country": <string>,
                "host": <string>,
                "port": <integer>,
                "ip": <string>
            },
            "result":{
                "id": <string>,
                "url": <string>
            }
        }
        """
        # log for debugging, there is nothing sensitive here
        self.log.debug("speedtest output: %s", payload)
        if payload.get("type") != "result":
            raise Exception("unexpected result type found: {}".format(payload.get("type")))

        result_data = payload.get("result")
        server_data = payload.get("server")
        interface_data = payload.get("interface")
        tags = (tags or []) + [
            "isp:{}".format(payload.get("isp")),  # this will be normalized per tag standards
            "interface_name:{}".format(interface_data.get("name")),
            "server_id:{}".format(server_data.get("id")),
            "server_name:{}".format(server_data.get("name")),
            "server_country:{}".format(server_data.get("country")),
            "server_host:{}".format(server_data.get("host")),
        ]

        event_msg = (
            "[Test Results {test_id}]({test_url})\n\nServer: {server_name}({server_id}) - "
            + "{server_location}, {server_country} at {server_host}:{server_port} ({server_ip}:{server_port})\n"
            + "ISP: {isp}"
        )

        self.event(
            {
                "msg_title": "Speedtest Run {}".format(result_data.get("id")),
                "msg_text": event_msg.format(
                    test_id=result_data.get("id"),
                    test_url=result_data.get("url"),
                    server_name=server_data.get("name"),
                    server_id=server_data.get("id"),
                    server_location=server_data.get("location"),
                    server_country=server_data.get("country"),
                    server_host=server_data.get("host"),
                    server_port=server_data.get("port"),
                    server_ip=server_data.get("ip"),
                    isp=payload.get("isp"),
                ),
                "tags": tags,
            }
        )

        # ping data
        ping_data = payload.get("ping")
        self.gauge("speedtest.ping.jitter", float(ping_data.get("jitter")), tags)
        self.gauge("speedtest.ping.latency", float(ping_data.get("latency")), tags)

        download_data = payload.get("download")
        self.gauge("speedtest.download.bandwidth", float(download_data.get("bandwidth")) * MEGABYTE_TO_MEBIBYTE, tags)
        self.gauge("speedtest.download.bytes", float(download_data.get("bytes")), tags)
        self.gauge("speedtest.download.elapsed", float(download_data.get("elapsed")), tags)

        upload_data = payload.get("upload")
        self.gauge("speedtest.upload.bandwidth", float(upload_data.get("bandwidth")) * MEGABYTE_TO_MEBIBYTE, tags)
        self.gauge("speedtest.upload.bytes", float(upload_data.get("bytes")), tags)
        self.gauge("speedtest.upload.elapsed", float(upload_data.get("elapsed")), tags)

        self.gauge("speedtest.packet_loss", float(payload.get("packetLoss", 0)), tags)
