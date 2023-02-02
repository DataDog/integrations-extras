import time
from datetime import datetime
from json import JSONDecodeError
from urllib.error import HTTPError

from requests.exceptions import InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException

METRIC = "/metrics/entitlements/"
QUOTA = "/quota/"
AUDIT_LOG = "/audit-log/"
VOUNDRABILITIES = "/vulnerabilities/"
WARNING_QUOTA = 75
CRITICAL_QUOTA = 85
LAST_VULNERABILITY_STAMP = 0
LAST_AUDIT_LOG_STAMP = 0
AUDIT_LOG_LAST_RUN = 0
VULNERABILITY_LAST_RUN = 0


class CloudsmithCheck(AgentCheck):
    __NAMESPACE__ = "cloudsmith"

    def __init__(self, name, init_config, instances):
        super(CloudsmithCheck, self).__init__(name, init_config, instances)

        self.base_url = self.instance.get("url")
        self.api_key = self.instance.get("cloudsmith_api_key")
        self.org = self.instance.get("organization")

        self.validate_config()

        self.log.debug("Cloudsmith monitoring starting on %s", self.base_url)

        self.tags = self.instance.get("tags", [])
        self.tags.append("base_url:{}".format(self.base_url))
        self.tags.append("cloudsmith_org:{}".format(self.org))

    def validate_config(self):
        if not self.api_key:
            raise ConfigurationError("Configuration error, please specify api token in conf.yaml.")

        if not self.org:
            raise ConfigurationError("Configuration error, please specify org in conf.yaml.")

        if not self.base_url:
            raise ConfigurationError("Configuration error, please specify Cloudsmith url in conf.yaml")

    def get_full_path(self, path):
        url = self.base_url.rstrip("/") + path + self.org
        return url

    def convert_time(self, time):
        return int(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())

    # Get stats from REST API as json
    def get_api_json(self, url):

        try:
            key = self.api_key
            headers = {"X-Api-Key": key, "content-type": "application/json"}
            response = self.http.get(url, headers=headers)
        except Timeout as e:
            error_message = "Request timeout: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            error_message = "Request failed: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
            )
            raise

        except JSONDecodeError as e:
            error_message = "JSON Parse failed: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
            )
            raise

        except ValueError as e:
            error_message = str(e)
            self.log.warning(error_message)
            self.service_check("can_connect", AgentCheck.CRITICAL, message=error_message)
            raise

        if response.status_code != 200:
            error_message = f"""Expected status code 200 for url {url}, but got status code:
            {response.status_code} check your config information"""
            self.log.warning(error_message)
            self.service_check("can_connect", AgentCheck.CRITICAL, message=error_message)
            raise CheckException(error_message)
        else:
            self.service_check("can_connect", AgentCheck.OK)

        return response.json()

    def get_usage_info(self):
        url = self.get_full_path(QUOTA)
        response_json = self.get_api_json(url)
        return response_json

    def get_entitlement_info(self):
        url = self.get_full_path(METRIC)
        response_json = self.get_api_json(url)
        return response_json

    def get_audit_log_info(self):
        url = self.get_full_path(AUDIT_LOG)
        response_json = self.get_api_json(url)
        return response_json

    def get_vulnerabilities_info(self):
        url = self.get_full_path(VOUNDRABILITIES)
        response_json = self.get_api_json(url)
        return response_json

    def get_parsed_entitlement_info(self):
        token_count = -1
        bandwidth_total = -1
        download_total = -1

        response_json = self.get_entitlement_info()

        if "tokens" in response_json:
            if "total" in response_json["tokens"]:
                token_count = response_json["tokens"]["total"]
            else:
                self.log.warning("Error when parsing JSON for total token usage")
            if (
                "bandwidth" in response_json["tokens"]
                and "total" in response_json["tokens"]["bandwidth"]
                and "value" in response_json["tokens"]["bandwidth"]["total"]
            ):
                bandwidth_total = response_json["tokens"]["bandwidth"]["total"]["value"]
            else:
                self.log.warning("Error when parsing JSON for total token bandwidth usage")
            if (
                "downloads" in response_json["tokens"]
                and "total" in response_json["tokens"]["downloads"]
                and "value" in response_json["tokens"]["downloads"]["total"]
            ):
                download_total = response_json["tokens"]["downloads"]["total"]["value"]
            else:
                self.log.warning("Error when parsing JSON for total token download usage")
        else:
            self.log.warning("Error when parsing JSON for tokens")

        entitlement_info = {
            "token_count": token_count,
            "token_bandwidth_total": bandwidth_total,
            "token_download_total": download_total,
        }
        return entitlement_info

    def get_parsed_usage_info(self):
        response_json = self.get_usage_info()

        storage_used = -1
        bandwidth_used = -1
        storage_mark = self.UNKNOWN
        bandwidth_mark = self.UNKNOWN

        if "usage" in response_json and "raw" in response_json["usage"]:
            if (
                "storage" in response_json["usage"]["raw"]
                and "percentage_used" in response_json["usage"]["raw"]["storage"]
            ):
                storage_used = response_json["usage"]["raw"]["storage"]["percentage_used"]
                storage_mark = self.OK
            else:
                self.log.warning("Error when parsing JSON for storage usage")
            if (
                "bandwidth" in response_json["usage"]["raw"]
                and "percentage_used" in response_json["usage"]["raw"]["bandwidth"]
            ):
                bandwidth_used = response_json["usage"]["raw"]["bandwidth"]["percentage_used"]
                bandwidth_mark = self.OK
            else:
                self.log.warning("Error when parsing JSON for bandwidth usage")
        else:
            self.log.warning("Error while parsing JSON for usage information")

        if storage_mark == self.OK:
            if storage_used >= CRITICAL_QUOTA:
                storage_mark = self.CRITICAL
            elif storage_used >= WARNING_QUOTA:
                storage_mark = self.WARNING

        if bandwidth_mark == self.OK:
            if bandwidth_used >= CRITICAL_QUOTA:
                bandwidth_mark = self.CRITICAL
            elif bandwidth_used >= WARNING_QUOTA:
                bandwidth_mark = self.WARNING

        usage_info = {
            "storage_mark": storage_mark,
            "storage_used": storage_used,
            "bandwidth_mark": bandwidth_mark,
            "bandwidth_used": bandwidth_used,
        }
        return usage_info

    def get_parsed_audit_log_info(self):
        response_json = self.get_audit_log_info()

        new_dict = []

        if len(response_json) == 0:
            self.log.warning("Error when parsing JSON for audit log information")
        else:
            for i in response_json:
                new_dict.append(
                    {
                        "actor": i["actor"],
                        "actor_kind": i["actor_kind"],
                        "city": i["actor_location"]["city"],
                        "event": i["event"],
                        "event_at": self.convert_time(i["event_at"]),
                        "object": i["object"],
                        "object_slug_perm": i["object_slug_perm"],
                    }
                )

        return new_dict

    def filter_vulnerabilities(self, response_json, severity_list):
        filtered_results = []
        for result in response_json:
            if "max_severity" in result and result["max_severity"] in severity_list:
                filtered_results.append(result)
                response_json = filtered_results
        return response_json

    def get_parsed_vulnerabilities_info(self):
        # only show high or critical vulnerabilities
        response_json = self.filter_vulnerabilities(self.get_vulnerabilities_info(), ["High", "Critical"])

        new_dict = []

        if len(response_json) == 0:
            self.log.warning("Error when parsing JSON for vulnerabilities information")
        else:
            for i in response_json:
                new_dict.append(
                    {
                        "package_name": i["package"]["name"],
                        "package_version": i["package"]["version"],
                        "package_url": i["package"]["url"],
                        "severity": i["max_severity"],
                        "num_vulnerabilities": i["num_vulnerabilities"],
                        "created_at": self.convert_time(i["created_at"]),
                    }
                )

        return new_dict

    def check(self, _):

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/

        usage_info = {
            "storage_mark": CloudsmithCheck.UNKNOWN,
            "storage_used": -1,
            "bandwidth_mark": CloudsmithCheck.UNKNOWN,
            "bandwidth_used": -1,
        }
        entitlement_info = {
            "token_count": -1,
            "token_bandwidth_total": -1,
            "token_download_total": -1,
        }

        audit_log_info = [
            {
                "actor": CloudsmithCheck.UNKNOWN,
                "actor_kind": CloudsmithCheck.UNKNOWN,
                "city": CloudsmithCheck.UNKNOWN,
                "event": CloudsmithCheck.UNKNOWN,
                "event_at": -1,
                "object": CloudsmithCheck.UNKNOWN,
                "object_slug_perm": CloudsmithCheck.UNKNOWN,
            }
        ]

        vulnerabilities_info = [
            {
                "package_name": CloudsmithCheck.UNKNOWN,
                "package_version": CloudsmithCheck.UNKNOWN,
                "package_url": CloudsmithCheck.UNKNOWN,
                "severity": CloudsmithCheck.UNKNOWN,
                "num_vulnerabilities": -1,
                "created_at": -1,
            }
        ]

        global LAST_AUDIT_LOG_STAMP
        global LAST_VULNERABILITY_STAMP
        global AUDIT_LOG_LAST_RUN
        global VULNERABILITY_LAST_RUN

        usage_info = self.get_parsed_usage_info()
        entitlement_info = self.get_parsed_entitlement_info()

        # Only run audit log and vulnerability checks if the last check was more than 5 minutes ago
        # This will prevent the check from running too often and hitting the rate limit

        if (time.time() - AUDIT_LOG_LAST_RUN) > 300:
            audit_log_info = self.get_parsed_audit_log_info()
            AUDIT_LOG_LAST_RUN = time.time()

        if (time.time() - VULNERABILITY_LAST_RUN) > 300:
            vulnerabilities_info = self.get_parsed_vulnerabilities_info()
            VULNERABILITY_LAST_RUN = time.time()

        vulnerabilities_info = self.get_parsed_vulnerabilities_info()

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck

        self.gauge("storage_used", usage_info["storage_used"], tags=self.tags)
        self.gauge("bandwidth_used", usage_info["bandwidth_used"], tags=self.tags)
        self.gauge("token_count", entitlement_info["token_count"], tags=self.tags)
        self.gauge(
            "token_bandwidth_total",
            entitlement_info["token_bandwidth_total"],
            tags=self.tags,
        )
        self.gauge(
            "token_download_total",
            entitlement_info["token_download_total"],
            tags=self.tags,
        )

        # only create an event if the timestamp is newer than the last event
        # this is to prevent duplicate events as we pull down the entire audit log

        if LAST_AUDIT_LOG_STAMP < audit_log_info[0]["event_at"]:
            for a in audit_log_info:
                if a["event_at"] > LAST_AUDIT_LOG_STAMP:
                    self.event(
                        {
                            "timestamp": a["event_at"],
                            "event_type": "audit logs",
                            "api_key": self.api_key,
                            "msg_title": "{} on Object: {} (Object Slug: {}".format(
                                a["event"], a["object"], a["object_slug_perm"]
                            ),
                            "msg_text": "Actor: {} ({}) from {}".format(a["actor"], a["actor_kind"], a["city"]),
                            "aggregation_key": "audit_log",
                            "tags": self.tags,
                        }
                    )
            LAST_AUDIT_LOG_STAMP = audit_log_info[0]["event_at"]

        if LAST_VULNERABILITY_STAMP < vulnerabilities_info[0]["created_at"]:
            for v in vulnerabilities_info:
                if v["created_at"] > LAST_VULNERABILITY_STAMP:
                    self.event(
                        {
                            "timestamp": v["created_at"],
                            "event_type": "vulnerabilities",
                            "api_key": self.api_key,
                            "msg_title": "{} vulnerability found in package: {} Version: {}".format(
                                v["severity"], v["package_name"], v["package_version"]
                            ),
                            "msg_text": "Number of vulnerabilities: {}. Package URL: {}".format(
                                v["num_vulnerabilities"], v["package_url"]
                            ),
                            "aggregation_key": "vulnerabilities",
                            "tags": self.tags,
                        }
                    )
            LAST_VULNERABILITY_STAMP = vulnerabilities_info[0]["created_at"]

        storage_msg = "Percentage storage used: {}%".format(usage_info["storage_used"])
        self.service_check(
            "storage",
            usage_info["storage_mark"],
            message=storage_msg if usage_info["storage_mark"] != AgentCheck.OK else "",
        )

        bandwith_msg = "Percentage bandwidth used: {}%".format(usage_info["bandwidth_used"])
        self.service_check(
            "bandwidth",
            usage_info["bandwidth_mark"],
            message=bandwith_msg if usage_info["bandwidth_mark"] != AgentCheck.OK else "",
        )
