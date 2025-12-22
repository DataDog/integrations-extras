import json
import re
from datetime import datetime, timedelta, timezone

import requests

from datadog_checks.base import ConfigurationError
from datadog_checks.base.checks.logs.crawler.base import LogCrawlerCheck
from datadog_checks.base.checks.logs.crawler.stream import LogRecord, LogStream


def parse_iso8601_timestamp(ts_str: str) -> datetime:
    """
    Convert ISO8601 timestamp string to an offset-aware datetime (UTC if 'Z').
    Examples:
      '2025-08-11T23:03:34.983Z' -> aware UTC
      '2025-08-11T23:03:34.983+00:00' -> aware UTC
    """
    if not ts_str:
        return None
    # Normalize trailing Z to +00:00
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'
    dt = datetime.fromisoformat(ts_str)
    if dt.tzinfo is None:
        # Make it explicit UTC if somehow naive
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


class ScamalyticsCheck(LogCrawlerCheck):
    __NAMESPACE__ = 'scamalytics'

    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)
        self.instance = instances[0] if instances else {}

        required_keys = [
            "scamalytics_api_key",
            "scamalytics_api_url",
            "customer_id",
            "dd_api_key",
            "dd_app_key",
        ]
        missing = [k for k in required_keys if not self.instance.get(k)]
        if missing:
            raise ConfigurationError(f"Missing required configuration key(s): {', '.join(missing)}")

    def get_log_streams(self):
        return [ScamalyticsLogStream(check=self, name="scamalytics_stream")]


class ScamalyticsLogStream(LogStream):
    """
    Crawl Datadog logs, extract public IPs, deduplicate per 24h via persistent cache,
    enrich new IPs with Scamalytics, and emit enriched logs through the crawler.
    """

    CACHE_KEY = "scamalytics_recent_ips"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In-memory per-run cache: {ip: bool processed_in_last_24h}
        self.session_recent_cache = {}
        # Persistent cache across runs: {ip: "ISO8601 UTC timestamp"}
        self.recent_cache = {}
        self._load_recent_cache()

        # Optional tunable window (hours) from config, default 24
        try:
            self.skip_window_hours = int(self.check.instance.get("skip_window_hours", 24))
        except Exception:
            self.skip_window_hours = 24

    def records(self, cursor=None):
        check = self.check
        dd_api_key = check.instance.get("dd_api_key")
        dd_app_key = check.instance.get("dd_app_key")
        scam_key = check.instance.get("scamalytics_api_key")
        scam_api_url = check.instance.get("scamalytics_api_url")
        customer_id = check.instance.get("customer_id")
        dd_site = check.instance.get("dd_site", "datadoghq.com")

        # Datadog Logs Search API
        logs_url = f"https://api.{dd_site}/api/v2/logs/events/search"
        headers = {
            "DD-API-KEY": dd_api_key,
            "DD-APPLICATION-KEY": dd_app_key,
            "Content-Type": "application/json",
        }

        # Cursor handling (ensure overlap with timezone-aware math)
        from_time = None
        if cursor and cursor.get("timestamp"):
            try:
                # 2s overlap for safety
                from_time = parse_iso8601_timestamp(cursor["timestamp"]) - timedelta(seconds=2)
            except Exception:
                from_time = None

        filter_dict = {
            "to": "now",
            "query": "@network.ip.attributes.ip:* AND -source:scamalytics-ti AND -service:scamalytics",
        }
        if from_time:
            # Always emit UTC Z format
            filter_dict["from"] = from_time.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        payload = {"filter": filter_dict, "page": {"limit": 1000}}

        try:
            resp = requests.post(logs_url, headers=headers, json=payload, timeout=15)
            resp.raise_for_status()
            logs = resp.json().get("data", [])
            check.log.info("SCAMALYTICS: fetched %s logs from Datadog", len(logs))
        except Exception as e:
            check.log.error("SCAMALYTICS: error fetching logs: %s", e)
            return

        ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
        
        # Initialize cursor tracking
        current_cursor_ts = cursor["timestamp"] if (cursor and cursor.get("timestamp")) else "1970-01-01T00:00:00Z"
        newest_timestamp = current_cursor_ts
        
        processed_ips_this_run = set()
        records_yielded_count = 0 

        for log_entry in logs:
            attributes = log_entry.get("attributes", {})
            ts_str = attributes.get("timestamp")
            if not ts_str:
                continue

            # Always track the newest timestamp seen
            if ts_str > newest_timestamp:
                newest_timestamp = ts_str

            # Extract any IPv4s
            log_content = str(log_entry)
            for ip in ip_pattern.findall(log_content):
                if not self._is_public_ip(ip):
                    continue
                if ip in processed_ips_this_run:
                    continue
                processed_ips_this_run.add(ip)

                # 1) Fast local session cache check
                if ip in self.session_recent_cache and self.session_recent_cache[ip] is True:
                    check.log.debug("SCAMALYTICS: SKIP %s (session cache <%sh)", ip, self.skip_window_hours)
                    continue

                # 2) Persistent cache check (authoritative)
                if self._processed_recently_local(ip):
                    check.log.info("SCAMALYTICS: SKIP %s (persistent cache <%sh)", ip, self.skip_window_hours)
                    self.session_recent_cache[ip] = True
                    continue

                # 3) Optional remote fallback (Datadog logs)
                if self._was_recently_processed_remote(ip):
                    check.log.info("SCAMALYTICS: SKIP %s (remote logs <%sh)", ip, self.skip_window_hours)
                    self._update_local_cache(ip)  # persist locally for next run
                    self.session_recent_cache[ip] = True
                    continue

                # 4) Query Scamalytics API and emit enriched log
                scam_url = f"{scam_api_url}{ip}"
                scam_headers = {
                    "Authorization": f"Bearer {scam_key}",
                    "Customer-id": f"{customer_id}",
                }

                try:
                    scam_resp = requests.get(scam_url, headers=scam_headers, timeout=10)
                    scam_resp.raise_for_status()
                    scam_data = scam_resp.json()
                except Exception as e:
                    check.log.error("SCAMALYTICS: Scamalytics API error for %s: %s", ip, e)
                    continue

                # Emit enriched record via crawler
                records_yielded_count += 1
                yield LogRecord(
                    data={
                        "message": f"Scamalytics report for IP {ip}",
                        "ddsource": "scamalytics-ti",
                        "service": "scamalytics",
                        "attributes": scam_data,
                    },
                    cursor={"timestamp": ts_str},
                )

                # Mark as processed now (both caches)
                self._update_local_cache(ip)
                self.session_recent_cache[ip] = True

        # === CHECKPOINT FIX ===
        # If we fetched logs but skipped ALL of them (because they were cached),
        # we must yield a dummy record to force the Agent to update the cursor.
        if len(logs) > 0 and records_yielded_count == 0:
            if newest_timestamp > current_cursor_ts:
                check.log.info("SCAMALYTICS: Batch completely skipped (cached). Emitting checkpoint to advance cursor.")
                yield LogRecord(
                    data={
                        "message": "Scamalytics Checkpoint: Batch Skipped",
                        "ddsource": "scamalytics-ti",
                        "service": "scamalytics",
                        "attributes": {
                            "checkpoint": True,
                            "info": "All IPs in this batch were cached. Advancing cursor."
                        }
                    },
                    cursor={"timestamp": newest_timestamp}
                )

        # Persist cache, prune expired, and advance cursor
        self._prune_expired_cache()
        self._save_recent_cache()

    @staticmethod
    def _is_public_ip(ip: str) -> bool:
        private_ranges = [
            re.compile(r"^10\..*"),
            re.compile(r"^192\.168\..*"),
            re.compile(r"^172\.(1[6-9]|2[0-9]|3[0-1])\..*"),
            re.compile(r"^127\..*"),
            re.compile(r"^169\.254\..*"),
        ]
        return not any(r.match(ip) for r in private_ranges)

    def _load_recent_cache(self) -> None:
        """Load persistent IP cache from Agent into self.recent_cache."""
        try:
            cache_str = self.check.read_persistent_cache(self.CACHE_KEY)
            if cache_str:
                self.recent_cache = json.loads(cache_str)
            else:
                self.recent_cache = {}
        except Exception as e:
            self.check.log.warning("SCAMALYTICS: failed to load persistent cache: %s", e)
            self.recent_cache = {}

    def _save_recent_cache(self) -> None:
        """Persist current cache to Agent store."""
        try:
            self.check.write_persistent_cache(self.CACHE_KEY, json.dumps(self.recent_cache))
        except Exception as e:
            self.check.log.warning("SCAMALYTICS: failed to save persistent cache: %s", e)

    def _update_local_cache(self, ip: str) -> None:
        """Mark IP as processed at current UTC time (aware, ISO8601 Z)."""
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.recent_cache[ip] = now_utc
        # Write-through so restarts keep the state
        self._save_recent_cache()

    def _processed_recently_local(self, ip: str) -> bool:
        """Return True if IP was processed within the configured window using persistent cache."""
        ts_str = self.recent_cache.get(ip)
        if not ts_str:
            return False
        try:
            last_dt = parse_iso8601_timestamp(ts_str)  # aware
            age = datetime.now(timezone.utc) - last_dt
            return age < timedelta(hours=self.skip_window_hours)
        except Exception:
            return False

    def _prune_expired_cache(self) -> None:
        """Remove entries older than the configured window."""
        now = datetime.now(timezone.utc)
        expiry = timedelta(hours=self.skip_window_hours)
        expired = []
        for ip, ts_str in self.recent_cache.items():
            try:
                seen_dt = parse_iso8601_timestamp(ts_str)
                if (now - seen_dt) > expiry:
                    expired.append(ip)
            except Exception:
                expired.append(ip)
        for ip in expired:
            del self.recent_cache[ip]

    def _was_recently_processed_remote(self, ip: str) -> bool:
        """
        Fallback: search Datadog logs for a Scamalytics entry in the last window.
        Returns True if found. Also seeds local cache if found.
        """
        if ip in self.session_recent_cache:
            return self.session_recent_cache[ip] is True

        check = self.check
        dd_api_key = check.instance.get("dd_api_key")
        dd_app_key = check.instance.get("dd_app_key")
        dd_site = check.instance.get("dd_site", "datadoghq.com")

        logs_url = f"https://api.{dd_site}/api/v2/logs/events/search"
        headers = {
            "DD-API-KEY": dd_api_key,
            "DD-APPLICATION-KEY": dd_app_key,
            "Content-Type": "application/json",
        }

        window = f"now-{self.skip_window_hours}h"

        filter_dict = {
            "from": window,
            "to": "now",
            "query": f"source:scamalytics-ti service:scamalytics @attributes.scamalytics.ip:{ip}",
        }
        payload = {"filter": filter_dict, "page": {"limit": 1}}

        try:
            resp = requests.post(logs_url, headers=headers, json=payload, timeout=10)
            resp.raise_for_status()
            found = len(resp.json().get("data", [])) > 0
            if found:
                self._update_local_cache(ip)
                self.session_recent_cache[ip] = True
            return found
        except Exception as e:
            check.log.warning("SCAMALYTICS: remote recent-check failed for %s: %s", ip, e)
            return False