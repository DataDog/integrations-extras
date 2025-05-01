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
VULNERABILITY_POLICY_VIOLATION = "/vulnerability-policy-violation/"
LICENSE_POLICY_VIOLATION = "/license-policy-violation/"
MEMBERS = "/members/"
WARNING_QUOTA = 75
CRITICAL_QUOTA = 85
LAST_VULNERABILITY_STAMP = 0
LAST_AUDIT_LOG_STAMP = 0
AUDIT_LOG_LAST_RUN = 0
VULNERABILITY_LAST_RUN = 0


def audit_log_resp_good():
    audit_log_resp_good = [
        {
            "actor": "test user",
            "actor_ip_address": "XXX.XXX.XXX.XXX",
            "actor_kind": "user",
            "actor_location": {
                "city": "XXX",
                "continent": "Europe",
                "country": "United Kingdom",
                "country_code": "GB",
                "latitude": "1",
                "longitude": "1",
                "postal_code": "BT11",
            },
            "actor_slug_perm": "msle0eeRYz0",
            "actor_url": "https://api.cloudsmith.io/v1/users/profile/test/",
            "context": "",
            "event": "action.login",
            "event_at": "2023-01-10T12:59:03.926729Z",
            "object": "test",
            "object_kind": "user",
            "object_slug_perm": "msle0eeRYz0",
            "uuid": "efb5b5b0-5b5b-5b5b-5b5b-5b5b5b5b5b5b",
            "target": "cloudsmith-test",
            "target_kind": "namespace",
            "target_slug_perm": "eqr0eeRYz0",
        }
    ]
    return audit_log_resp_good


def vulnerabilitiy_resp_json():
    vulnerabilitiy_resp_json = [
        {
            "identifier": "weqwqeqw",
            "created_at": "2023-02-06T18:18:39.546636Z",
            "package": {
                "identifier": "reqwqeqw",
                "name": "python",
                "version": "5135",
                "url": "https://api.cloudsmith.io/v1/packages/cloudsmith-test/test/tqetq/",
            },
            "scan_id": 1,
            "has_vulnerabilities": True,
            "num_vulnerabilities": 3,
            "max_severity": "Critical",
        }
    ]
    return vulnerabilitiy_resp_json


class CloudsmithCheck(AgentCheck):
    MAX_EVENTS = 100
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
            response = self.http.get(url, headers=headers, timeout=60)
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

        # if status is 401 and url includes the words "audit-log" or "vulnerabilities", then return mock data
        if response.status_code == 401 and ("audit-log" in url or "vulnerabilities" in url):
            return None

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
        if not response_json:
            response_json = audit_log_resp_good()
        return response_json

    def get_vulnerabilities_info(self):
        url = self.get_full_path(VOUNDRABILITIES)
        all_results = []
        while url:
            response_json = self.get_api_json(url)
            if not response_json:
                response_json = vulnerabilitiy_resp_json()
            if isinstance(response_json, list):
                all_results.extend(response_json)
                break
            else:
                all_results.extend(response_json.get("results", []))
                url = response_json.get("next")
        return all_results

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
        storage_used_bytes = -1
        storage_plan_limit_bytes = -1
        bandwidth_used_bytes = -1
        bandwidth_plan_limit_bytes = -1

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
            # New: extract raw bytes and plan limits
            storage_used_bytes = response_json["usage"]["raw"]["storage"].get("used", -1)
            storage_plan_limit_bytes = response_json["usage"]["raw"]["storage"].get("plan_limit", -1)
            bandwidth_used_bytes = response_json["usage"]["raw"]["bandwidth"].get("used", -1)
            bandwidth_plan_limit_bytes = response_json["usage"]["raw"]["bandwidth"].get("plan_limit", -1)
        else:
            self.log.warning("Error while parsing JSON for usage information")

        # Add GB values
        storage_used_gb = round(storage_used_bytes / (1024**3), 2) if storage_used_bytes != -1 else -1
        storage_plan_limit_gb = round(storage_plan_limit_bytes / (1024**3), 2) if storage_plan_limit_bytes != -1 else -1
        bandwidth_used_gb = round(bandwidth_used_bytes / (1024**3), 2) if bandwidth_used_bytes != -1 else -1
        bandwidth_plan_limit_gb = (
            round(bandwidth_plan_limit_bytes / (1024**3), 2) if bandwidth_plan_limit_bytes != -1 else -1
        )

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
            "storage_used_bytes": storage_used_bytes,
            "storage_plan_limit_bytes": storage_plan_limit_bytes,
            "bandwidth_used_bytes": bandwidth_used_bytes,
            "bandwidth_plan_limit_bytes": bandwidth_plan_limit_bytes,
            "storage_used_gb": storage_used_gb,
            "storage_plan_limit_gb": storage_plan_limit_gb,
            "bandwidth_used_gb": bandwidth_used_gb,
            "bandwidth_plan_limit_gb": bandwidth_plan_limit_gb,
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
                        "city": i["actor_location"]["city"] if i.get("actor_location") else None,
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
        # Get raw results first
        raw_results = self.get_vulnerabilities_info()

        filtered_results = [r for r in raw_results if r.get("package")]

        if not filtered_results:
            self.log.warning("No filtered vulnerabilities found, using unfiltered results.")
            filtered_results = raw_results

        # Sort by created_at descending to always get the latest first
        filtered_results.sort(key=lambda x: x["created_at"], reverse=True)

        parsed = []
        for i in filtered_results:
            if i.get("num_vulnerabilities", 0) > 0:
                parsed.append(
                    {
                        "package_name": i["package"]["name"],
                        "package_version": i["package"]["version"],
                        "package_url": i["package"]["url"],
                        "severity": i["max_severity"],
                        "num_vulnerabilities": i["num_vulnerabilities"],
                        "created_at": self.convert_time(i["created_at"]),
                    }
                )

        return parsed

    def get_vuln_policy_violation_info(self):
        base_url = f"{self.base_url.rstrip('/')}/orgs/{self.org}/vulnerability-policy-violation/"
        all_results = []
        url = base_url

        while url:
            response_json = self.get_api_json(url)
            if not response_json:
                self.log.warning("No policy violation data found or API call failed.")
                break

            all_results.extend(response_json.get("results", []))
            url = response_json.get("next")  # Follow pagination if there are more results

        return {"results": all_results}

    def get_license_policy_violation_info(self):
        base_url = f"{self.base_url.rstrip('/')}/orgs/{self.org}/license-policy-violation/"
        all_results = []
        url = base_url

        while url:
            response_json = self.get_api_json(url)
            if not response_json:
                self.log.warning("No license policy violation data found or API call failed.")
                break

            all_results.extend(response_json.get("results", []))
            url = response_json.get("next")  # Follow pagination if there are more results

        return {"results": all_results}

    def get_members_info(self):
        base_url = f"{self.base_url.rstrip('/')}/orgs/{self.org}{MEMBERS}"
        all_results = []
        url = base_url

        while url:
            response_json = self.get_api_json(url)
            if not response_json:
                self.log.warning("No members data found or API call failed.")
                break

            if isinstance(response_json, dict):
                all_results.extend(response_json.get("results", []))
                url = response_json.get("next")  # Handle pagination
            elif isinstance(response_json, list):
                all_results.extend(response_json)
                url = None
            else:
                self.log.warning("Unexpected response format for members endpoint.")
                url = None

        return {"results": all_results}

    def get_parsed_members_info(self):
        response_json = self.get_members_info()
        parsed = []
        for item in response_json.get("results", []):
            parsed.append(
                {
                    "user_name": item.get("user_name", "unknown"),
                    "user_id": item.get("user_id", "unknown"),
                    "user": item.get("user", "unknown"),
                    "email": item.get("email", "unknown"),
                    "role": item.get("role", "unknown"),
                    "is_active": item.get("is_active", False),
                    "has_two_factor": item.get("has_two_factor", False),
                    "last_login_at": (
                        self.convert_time(item["last_login_at"]) if item.get("last_login_at") else int(time.time())
                    ),
                    "joined_at": self.convert_time(item["joined_at"]) if item.get("joined_at") else int(time.time()),
                    "last_login_method": item.get("last_login_method", "unknown"),
                }
            )
        return parsed

    def get_parsed_vuln_policy_violation_info(self):
        response_json = self.get_vuln_policy_violation_info()
        parsed = []
        for item in response_json.get("results", []):
            parsed.append(
                {
                    "package": item["package"]["name"] if item.get("package") else "unknown",
                    "policy": item.get("policy", {}).get("name", "unknown"),
                    "violations": (
                        item["vulnerability_scan_results"]["num_vulnerabilities"]
                        if item.get("vulnerability_scan_results")
                        else 0
                    ),
                    "last_detected": (
                        self.convert_time(item.get("event_at")) if item.get("event_at") else int(time.time())
                    ),
                }
            )
        return parsed

    def get_parsed_license_policy_violation_info(self):
        response_json = self.get_license_policy_violation_info()
        parsed = []
        for item in response_json.get("results", []):
            parsed.append(
                {
                    "package": item["package"]["name"] if item.get("package") else "unknown",
                    "policy": item.get("policy", {}).get("name", "unknown"),
                    "violations": 1,
                    "reason": "; ".join(item.get("reasons", [])),
                    "last_detected": (
                        self.convert_time(item.get("event_at")) if item.get("event_at") else int(time.time())
                    ),
                }
            )
        return parsed

    def check(self, _):

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
        else:
            vulnerabilities_info = self.get_parsed_vulnerabilities_info()
        policy_violations_info = self.get_parsed_vuln_policy_violation_info()
        for v in policy_violations_info[: self.MAX_EVENTS]:
            self.event(
                {
                    "timestamp": v["last_detected"],
                    "event_type": "vulnerability_policy_violation",
                    "msg_title": f"{v['violations']} policy violations for {v['package']}",
                    "msg_text": f"Policy `{v['policy']}` triggered {v['violations']} violation(s).",
                    "aggregation_key": "vulnerability_policy_violation",
                    "tags": self.tags + [f"package:{v['package']}", f"policy:{v['policy']}"],
                }
            )
        license_violations_info = self.get_parsed_license_policy_violation_info()
        for v in license_violations_info[: self.MAX_EVENTS]:
            self.event(
                {
                    "timestamp": v["last_detected"],
                    "event_type": "license_policy_violation",
                    "msg_title": f"License policy violation for {v['package']}",
                    "msg_text": f"Policy `{v['policy']}` triggered a license violation.\nReason: {v['reason']}",
                    "aggregation_key": "license_policy_violation",
                    "tags": self.tags + [f"package:{v['package']}", f"policy:{v['policy']}"],
                }
            )
        # Only send new vulnerabilities as events based on LAST_VULNERABILITY_STAMP

        if vulnerabilities_info and len(vulnerabilities_info) > 0:
            new_vulns = [v for v in vulnerabilities_info if v["created_at"] > LAST_VULNERABILITY_STAMP]
            for v in new_vulns[: self.MAX_EVENTS]:
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
            if new_vulns:
                max_created = max(v["created_at"] for v in new_vulns)
                LAST_VULNERABILITY_STAMP = max_created

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck

        self.gauge("storage_used", usage_info["storage_used"], tags=self.tags)
        self.gauge("bandwidth_used", usage_info["bandwidth_used"], tags=self.tags)
        self.gauge("storage_used_bytes", usage_info["storage_used_bytes"], tags=self.tags)
        self.gauge("storage_plan_limit_bytes", usage_info["storage_plan_limit_bytes"], tags=self.tags)
        self.gauge("bandwidth_used_bytes", usage_info["bandwidth_used_bytes"], tags=self.tags)
        self.gauge("bandwidth_plan_limit_bytes", usage_info["bandwidth_plan_limit_bytes"], tags=self.tags)
        self.gauge("storage_used_gb", usage_info["storage_used_gb"], tags=self.tags)
        self.gauge("storage_plan_limit_gb", usage_info["storage_plan_limit_gb"], tags=self.tags)
        self.gauge("bandwidth_used_gb", usage_info["bandwidth_used_gb"], tags=self.tags)
        self.gauge("bandwidth_plan_limit_gb", usage_info["bandwidth_plan_limit_gb"], tags=self.tags)
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
            for a in audit_log_info[: self.MAX_EVENTS]:
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

        else:
            pass

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
        members_info = self.get_parsed_members_info()
        for m in members_info:
            self.gauge(
                "cloudsmith.member.active",
                1 if m["is_active"] else 0,
                tags=self.tags + [f"user:{m['user']}", f"role:{m['role']}", f"2fa:{m['has_two_factor']}"],
            )
        # Deduplicate by user (slug), not user_name or user_id
        unique_members = {m["user"]: m for m in members_info if "user" in m}.values()
        member_summary = "\n".join(
            f"{m.get('user_name', 'unknown')} ({m.get('role', 'unknown')}), 2FA: {m.get('has_two_factor', False)}, Last Login: {datetime.utcfromtimestamp(m.get('last_login_at', int(time.time()))).isoformat()}, Slug: {m.get('user', 'unknown')}"
            for m in unique_members
        )
        self.event(
            {
                "timestamp": int(time.time()),
                "event_type": "org_member_summary",
                "msg_title": f"Organization Member Summary ({len(unique_members)} members)",
                "msg_text": member_summary,
                "aggregation_key": "org_members",
                "tags": self.tags,
            }
        )
