from datetime import datetime, timedelta
import re
import json
import requests
from datadog_checks.base import AgentCheck, ConfigurationError


def parse_iso8601_timestamp(ts_str):
    # Convert '2025-08-11T23:03:34.983Z' to a datetime object
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'  # Replace 'Z' with '+00:00' for UTC
    return datetime.fromisoformat(ts_str)


class ScamalyticsCheck(AgentCheck):
    __NAMESPACE__ = 'scamalytics'
    CACHE_KEY = "scamalytics_last_timestamp"
    PROCESSED_KEY = "scamalytics_processed_records"

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)
        self.instance = instances[0]

        # Configuration validation (Unit Test Method)
        required_keys = [
            "scamalytics_api_key",
            "scamalytics_api_url",
            "customer_id",
            "dd_api_key",
            "dd_app_key",
        ]
        missing = [k for k in required_keys if not self.instance.get(k)]
        if missing:
            raise ConfigurationError(
                f"Missing required configuration key(s): {', '.join(missing)}"
            )

    def check(self, _):
        dd_api_key = self.instance.get("dd_api_key")
        dd_app_key = self.instance.get("dd_app_key")
        scam_key = self.instance.get("scamalytics_api_key")
        scam_api_url = self.instance.get("scamalytics_api_url")
        customer_id = self.instance.get("customer_id")
        dd_site = self.instance.get("dd_site", "datadoghq.com")

        last_timestamp_str = self.read_persistent_cache(self.CACHE_KEY)
        if not last_timestamp_str:
            from_time = None
            self.log.info(
                "First run detected: querying all matching logs without 'from' filter")
        else:
            try:
                last_timestamp_dt = parse_iso8601_timestamp(last_timestamp_str)
                from_time = last_timestamp_dt - \
                    timedelta(seconds=2)  # 2 sec overlap
            except Exception as e:
                self.log.error(
                    f"Failed parsing timestamp '{last_timestamp_str}': {e}")
                from_time = None

        logs_url = f"https://api.{dd_site}/api/v2/logs/events/search"
        headers = {
            "DD-API-KEY": dd_api_key,
            "DD-APPLICATION-KEY": dd_app_key,
            "Content-Type": "application/json"
        }

        filter_dict = {
            "to": "now",
            "query": "@network.ip.attributes.ip:* AND -source:scamalytics-ti AND -service:scamalytics"
        }
        if from_time:
            filter_dict["from"] = from_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        payload = {
            "filter": filter_dict,
            "page": {"limit": 1000}
        }

        try:
            resp = requests.post(logs_url, headers=headers,
                                 json=payload, timeout=10)
            resp.raise_for_status()
            logs = resp.json()
            self.log.info(
                f"Fetched {len(logs.get('data', []))} logs from Datadog")
        except Exception as e:
            self.log.error(f"Error fetching logs from Datadog API: {e}")
            return

        ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

        processed_cache_str = self.read_persistent_cache(self.PROCESSED_KEY)
        if processed_cache_str:
            processed_records = set(processed_cache_str.split(","))
        else:
            processed_records = set()

        new_processed_records = set()
        newest_timestamp = last_timestamp_str if last_timestamp_str else "1970-01-01T00:00:00Z"

        public_ips = set()

        for log_entry in logs.get("data", []):
            attributes = log_entry.get("attributes", {})
            ts = attributes.get("timestamp")
            if not ts:
                continue

            log_content = str(log_entry)
            for ip in ip_pattern.findall(log_content):
                if self._is_public_ip(ip):
                    unique_key = f"{ip}_{ts}"
                    if unique_key in processed_records:
                        continue
                    public_ips.add((ip, ts))
                    new_processed_records.add(unique_key)

                    if ts > newest_timestamp:
                        newest_timestamp = ts

        self.log.info(f"Found {len(public_ips)} new public IPs to process")

        processed_records.update(new_processed_records)
        if len(processed_records) > 1000:
            processed_records = set(list(processed_records)[-1000:])
        self.write_persistent_cache(
            self.PROCESSED_KEY, ",".join(processed_records))

        if not public_ips:
            return

        for ip, ts in public_ips:
            scam_url = scam_api_url + ip
            scam_headers = {
                "Authorization": f"Bearer {scam_key}",
                "Customer-id": f"{customer_id}"
            }
            try:
                scam_resp = requests.get(
                    scam_url, headers=scam_headers, timeout=10)
                scam_resp.raise_for_status()
                scam_data = scam_resp.json()
                self._send_to_logs(dd_api_key, dd_site, scam_data)
            except Exception as e:
                self.log.error(f"Error querying Scamalytics for {ip}: {e}")
                continue

        if new_processed_records:
            self.write_persistent_cache(self.CACHE_KEY, newest_timestamp)

    def _send_to_logs(self, dd_api_key, dd_site, scam_data):
        logs_url = f"https://http-intake.logs.{dd_site}/api/v2/logs"
        headers = {
            "DD-API-KEY": dd_api_key,
            "Content-Type": "application/json"
        }

        payload = [{
            "ddsource": "scamalytics-ti",
            "service": "scamalytics",
            "message": f"Scamalytics report for IP {scam_data.get('scamalytics', {}).get('ip', 'unknown')}",
            "attributes": scam_data
        }]

        try:
            resp = requests.post(logs_url, headers=headers,
                                 data=json.dumps(payload), timeout=10)
            resp.raise_for_status()
            self.log.info(
                f"Sent Scamalytics data for {scam_data.get('scamalytics', {}).get('ip', 'unknown')} to Logs"
            )
        except Exception as e:
            self.log.error(f"Error sending log to Datadog: {e}")

    def _is_public_ip(self, ip):
        private_ranges = [
            re.compile(r"^10\..*"),
            re.compile(r"^192\.168\..*"),
            re.compile(r"^172\.(1[6-9]|2[0-9]|3[0-1])\..*"),
            re.compile(r"^127\..*"),
            re.compile(r"^169\.254\..*")
        ]
        return not any(r.match(ip) for r in private_ranges)
