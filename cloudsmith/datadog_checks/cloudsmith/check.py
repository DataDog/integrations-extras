import time
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
from urllib.error import HTTPError
from urllib.parse import urlencode

from requests.exceptions import InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException

QUOTA = "/quota/"
AUDIT_LOG = "/audit-log/"
VULNERABILITIES = "/vulnerabilities/"
VULNERABILITY_POLICY_VIOLATION = "/vulnerability-policy-violation/"
LICENSE_POLICY_VIOLATION = "/license-policy-violation/"
MEMBERS = "/members/"
REPOSITORIES = "/repos/"
ANALYTICS_METRICS_CLIENT_TIME_SERIES = "/analytics/metrics/client/time-series/"
WARNING_QUOTA = 75
CRITICAL_QUOTA = 85

# Bandwidth analytics profile constants
VALID_INTERVALS = {
    "minute": 60,
    "five_minutes": 300,
    "fifteen_minutes": 900,
    "hour": 3600,
    "day": 86400,
    "week": 604800,
    "month": 2592000,
    "year": 31536000,
}
VALID_AGGREGATES = {"bytes_downloaded_sum", "request_count"}
VALID_FILTERS = [
    "repository",
    "repository_type",
    "broadcast_state",
    "package",
    "package_format",
    "user",
    "user_type",
    "entitlement_token",
    "ip_address",
    "country",
    "http_status",
    "edge_response",
]
LOOKBACK_INTERVALS = 3

LAST_VULNERABILITY_STAMP = 0
LAST_AUDIT_LOG_STAMP = 0
AUDIT_LOG_LAST_RUN = 0
VULNERABILITY_LAST_RUN = 0
LICENSE_VIOLATION_LAST_RUN = 0

# Mapping from aggregate name to Datadog metric suffix
AGGREGATE_METRIC_MAP = {
    "bytes_downloaded_sum": "cloudsmith.analytics.bytes_downloaded_sum",
    "request_count": "cloudsmith.analytics.request_count",
}

# Org-wide bandwidth metric names (no profile tag)
ORG_METRIC_MAP = {
    "bytes_downloaded_sum": "cloudsmith.bandwidth.bytes_downloaded",
    "request_count": "cloudsmith.bandwidth.request_count",
}


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

    def __init__(self, name, init_config, instances):
        super(CloudsmithCheck, self).__init__(name, init_config, instances)

        self.base_url = self.instance.get("url")
        self.api_key = self.instance.get("cloudsmith_api_key")
        self.org = self.instance.get("organization")

        # Track rate-limit quota from API response headers
        self._ratelimit_remaining = None
        self._pagination_page = None
        self._pagination_page_total = None

        self.validate_config()

        # Global bandwidth interval (used by both org-wide and profiles)
        self.bandwidth_interval = self.instance.get("bandwidth_interval", "five_minutes")
        if self.bandwidth_interval not in VALID_INTERVALS:
            raise ConfigurationError(
                "bandwidth_interval must be one of {}, got '{}'.".format(
                    list(VALID_INTERVALS.keys()), self.bandwidth_interval
                )
            )

        # Org-wide realtime bandwidth toggle
        self.enable_realtime_bandwidth = self.instance.get("enable_realtime_bandwidth", True)

        # Parse and validate bandwidth profiles
        self.bandwidth_profiles = self.instance.get("bandwidth_profiles", [])
        self._validate_bandwidth_profiles()

        # Track last submitted API timestamp per profile (epoch int) for dedup
        self._profile_last_ts = {}
        # Pre-compute tags per profile — emit tags for ALL configured filter keys
        self._profile_tags = {}
        for profile in self.bandwidth_profiles:
            pname = profile["name"]
            ptags = ["profile:{}".format(pname)]
            for key in VALID_FILTERS:
                values = profile.get(key)
                if values:
                    for v in values:
                        ptags.append("{}:{}".format(key, v))
            self._profile_tags[pname] = ptags

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

    def _validate_bandwidth_profiles(self):
        """Validate bandwidth_profiles configuration at init time."""
        seen_names = set()
        for i, profile in enumerate(self.bandwidth_profiles):
            if not isinstance(profile, dict):
                raise ConfigurationError("bandwidth_profiles[{}]: each profile must be a mapping.".format(i))
            name = profile.get("name")
            if not name or not isinstance(name, str):
                raise ConfigurationError("bandwidth_profiles[{}]: 'name' is required and must be a string.".format(i))
            if name in seen_names:
                raise ConfigurationError("bandwidth_profiles: duplicate profile name '{}'.".format(name))
            seen_names.add(name)

            # Per-profile interval is no longer supported — use bandwidth_interval
            if "interval" in profile:
                raise ConfigurationError(
                    "bandwidth_profiles[{}] ('{}'): per-profile 'interval' is no longer supported. "
                    "Use the top-level 'bandwidth_interval' setting instead.".format(i, name)
                )

            aggregate = profile.get("aggregate")
            if not aggregate or aggregate not in VALID_AGGREGATES:
                raise ConfigurationError(
                    "bandwidth_profiles[{}] ('{}'): 'aggregate' must be one of {}.".format(
                        i, name, sorted(VALID_AGGREGATES)
                    )
                )

            # Normalise list filter values — ensure single strings become lists
            for key in VALID_FILTERS:
                val = profile.get(key)
                if val is not None and not isinstance(val, list):
                    profile[key] = [val]

    def _build_analytics_base_url(self):
        """Build v2 analytics base URL from the configured v1 base URL."""
        base = self.base_url.rstrip("/")
        if base.endswith("/v1"):
            base = base[:-3] + "/v2"
        elif not base.endswith("/v2"):
            base = base + "/v2"
        return base + ANALYTICS_METRICS_CLIENT_TIME_SERIES + self.org + "/"

    def _build_analytics_url(self, aggregate, filters=None):
        """Build an analytics API URL.

        Args:
            aggregate: The aggregate type (e.g. 'bytes_downloaded_sum').
            filters: Optional dict-like object with filter keys from VALID_FILTERS.
                     When provided, matching key/value pairs are appended as query params.
        """
        base = self._build_analytics_base_url()
        interval_seconds = VALID_INTERVALS[self.bandwidth_interval]

        now_utc = datetime.now(timezone.utc)
        start_dt = now_utc - timedelta(seconds=LOOKBACK_INTERVALS * interval_seconds)
        start_str = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        params = [
            ("interval", self.bandwidth_interval),
            ("aggregate", aggregate),
            ("start_time", start_str),
        ]

        if filters:
            for key in VALID_FILTERS:
                values = filters.get(key)
                if values:
                    for v in values:
                        params.append((key, str(v)))

        return base + "?" + urlencode(params)

    def _process_timeseries(self, response_json, metric_name, tags, dedup_key, label):
        """Process an analytics time-series API response and submit the latest data point.

        Handles empty responses, incomplete-bucket trimming, API-settle trimming,
        and deduplication.  Submits a zero gauge when no actionable data is available
        so that Datadog doesn't interpolate stale values.

        Args:
            response_json: Parsed JSON from the analytics API (may be None).
            metric_name: The Datadog metric name to submit.
            tags: List of tags for the gauge.
            dedup_key: Key into ``_profile_last_ts`` for deduplication.
            label: Human-readable label for log messages (e.g. "profile 'prod'").
        """
        if response_json is None:
            return

        results = response_json.get("results", [])
        if not results:
            self.log.debug("No data for %s; submitting zero.", label)
            self.gauge(metric_name, 0.0, tags=tags)
            return

        series = results[0]
        timestamps = series.get("timestamps") or []
        values = series.get("values") or []

        if not timestamps or not values:
            self.log.debug("Empty time-series for %s; submitting zero.", label)
            self.gauge(metric_name, 0.0, tags=tags)
            return

        # Drop the last bucket if its interval window hasn't closed yet.
        interval_seconds = VALID_INTERVALS[self.bandwidth_interval]
        now_epoch = int(datetime.now(timezone.utc).timestamp())

        try:
            last_ts_epoch = self.convert_time(timestamps[-1])
        except ValueError:
            last_ts_epoch = 0

        if last_ts_epoch + interval_seconds > now_epoch:
            self.log.debug("%s: dropping incomplete bucket at %s.", label, timestamps[-1])
            timestamps = timestamps[:-1]
            values = values[:-1]

        if not timestamps or not values:
            self.log.debug("Only incomplete data for %s; submitting zero.", label)
            self.gauge(metric_name, 0.0, tags=tags)
            return

        latest_ts_str = timestamps[-1]
        latest_val = values[-1]

        if not latest_ts_str or latest_val is None:
            self.log.debug("Missing timestamp or value for %s; skipping.", label)
            return

        try:
            latest_ts_epoch = self.convert_time(latest_ts_str)
        except ValueError:
            self.log.warning("Could not parse timestamp '%s' for %s.", latest_ts_str, label)
            return

        # Dedup: only submit if this timestamp is newer than the last one we submitted.
        last_submitted = self._profile_last_ts.get(dedup_key, 0)
        if latest_ts_epoch <= last_submitted:
            self.log.debug("No new data for %s; submitting zero.", label)
            self.gauge(metric_name, 0.0, tags=tags)
            return

        self.gauge(metric_name, float(latest_val), tags=tags)
        self._profile_last_ts[dedup_key] = latest_ts_epoch
        self.log.debug("Submitted %s=%.2f for %s (ts=%s).", metric_name, float(latest_val), label, latest_ts_str)

    def _collect_bandwidth_profiles(self):
        """Fetch and submit metrics for all configured bandwidth profiles."""
        if not self.bandwidth_profiles:
            return

        for profile in self.bandwidth_profiles:
            pname = profile["name"]
            try:
                self._collect_single_profile(profile)
            except Exception as e:
                self.log.warning("Failed to collect bandwidth profile '%s': %s", pname, e)

    def _collect_org_bandwidth(self):
        """Fetch and submit org-wide bandwidth metrics (both aggregates, no filters)."""
        if not self.enable_realtime_bandwidth:
            return

        for aggregate, metric_name in ORG_METRIC_MAP.items():
            dedup_key = "_org_{}".format(aggregate)
            label = "org bandwidth '{}'".format(aggregate)
            url = self._build_analytics_url(aggregate)
            self.log.debug("%s requesting URL: %s", label, url)
            try:
                response_json = self.get_api_json(url)
                self._process_timeseries(response_json, metric_name, self.tags, dedup_key, label)
            except Exception as e:
                self.log.warning("Failed to collect %s: %s", label, e)

    def _collect_single_profile(self, profile):
        """Fetch analytics data for one profile and submit the latest new data point."""
        pname = profile["name"]
        metric_name = AGGREGATE_METRIC_MAP[profile["aggregate"]]
        profile_tags = self.tags + self._profile_tags.get(pname, [])
        label = "profile '{}'".format(pname)

        url = self._build_analytics_url(profile["aggregate"], filters=profile)
        self.log.debug("%s requesting URL: %s", label, url)
        response_json = self.get_api_json(url)
        self._process_timeseries(response_json, metric_name, profile_tags, pname, label)

    def convert_time(self, value):
        # Support timestamps with or without microseconds; raise if neither matches.
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return int(datetime.strptime(value, fmt).timestamp())
            except ValueError:
                pass
        raise ValueError(f"Invalid timestamp format: {value}")

    RATE_LIMIT_MAX_RETRIES = 3
    RATE_LIMIT_MAX_WAIT = 10

    def get_api_json(self, url):
        # Skip call if we already know quota is exhausted
        if self._ratelimit_remaining is not None and self._ratelimit_remaining <= 0:
            self.log.warning(
                "Skipping %s — rate-limit quota exhausted (remaining=0).",
                url,
            )
            return None

        for attempt in range(self.RATE_LIMIT_MAX_RETRIES + 1):
            try:
                key = self.api_key
                headers = {"X-Api-Key": key, "content-type": "application/json"}
                response = self.http.get(url, headers=headers, timeout=60)
            except Timeout as e:
                error_message = "Request timeout: {}, {}".format(url, e)
                self.log.warning(error_message)
                self.service_check(
                    "cloudsmith.can_connect",
                    AgentCheck.CRITICAL,
                    message=error_message,
                )
                raise

            except (HTTPError, InvalidURL, ConnectionError) as e:
                error_message = "Request failed: {}, {}".format(url, e)
                self.log.warning(error_message)
                self.service_check(
                    "cloudsmith.can_connect",
                    AgentCheck.CRITICAL,
                    message=error_message,
                )
                raise

            except JSONDecodeError as e:
                error_message = "JSON Parse failed: {}, {}".format(url, e)
                self.log.warning(error_message)
                self.service_check(
                    "cloudsmith.can_connect",
                    AgentCheck.CRITICAL,
                    message=error_message,
                )
                raise

            except ValueError as e:
                error_message = str(e)
                self.log.warning(error_message)
                self.service_check("cloudsmith.can_connect", AgentCheck.CRITICAL, message=error_message)
                raise

            # if status is 401 and url includes the words "audit-log" or "vulnerabilities", then return mock data
            if response.status_code == 401 and ("audit-log" in url or "vulnerabilities" in url):
                return None

            # Handle rate limiting (HTTP 429) using API response headers.
            if response.status_code == 429:
                wait = self._get_rate_limit_wait(response)
                remaining = response.headers.get("x-ratelimit-remaining")
                limit = response.headers.get("x-ratelimit-limit")
                self.log.warning(
                    "Rate limited (429) on %s (attempt %d/%d, limit=%s, remaining=%s, reset_wait=%.1fs).",
                    url,
                    attempt + 1,
                    self.RATE_LIMIT_MAX_RETRIES,
                    limit,
                    remaining,
                    wait,
                )
                # Only retry if we have attempts left AND the reset is soon
                # enough to be worth waiting for.  If the reset window is
                # beyond RATE_LIMIT_MAX_WAIT, retrying would just waste time
                # because the limit won't have cleared.
                if attempt < self.RATE_LIMIT_MAX_RETRIES and wait <= self.RATE_LIMIT_MAX_WAIT:
                    time.sleep(wait)
                    continue
                else:
                    reason = (
                        "retries exhausted"
                        if attempt >= self.RATE_LIMIT_MAX_RETRIES
                        else f"reset too far away ({wait:.0f}s > {self.RATE_LIMIT_MAX_WAIT}s cap)"
                    )
                    error_message = f"Rate limited (429) on {url}, {reason}. Skipping this endpoint for now."
                    self.log.warning(error_message)
                    self.service_check("cloudsmith.can_connect", AgentCheck.WARNING, message=error_message)
                    return None

            if response.status_code != 200:
                error_message = f"""Expected status code 200 for url {url}, but got status code:
                {response.status_code} check your config information"""
                self.log.warning(error_message)
                self.service_check("cloudsmith.can_connect", AgentCheck.CRITICAL, message=error_message)
                raise CheckException(error_message)
            else:
                self.service_check("cloudsmith.can_connect", AgentCheck.OK)

            # Track rate-limit headers from every successful response
            self._update_ratelimit_headers(response)
            self._update_pagination_headers(response)

            return response.json()

        return None

    def _update_ratelimit_headers(self, response):
        """Store rate-limit quota from response headers."""
        try:
            self._ratelimit_remaining = int(response.headers["x-ratelimit-remaining"])
        except (KeyError, ValueError, TypeError):
            pass

    def _update_pagination_headers(self, response):
        """Store pagination headers from the latest response, when available."""
        try:
            self._pagination_page = int(response.headers["x-pagination-page"])
        except (KeyError, ValueError, TypeError):
            self._pagination_page = None
        try:
            self._pagination_page_total = int(response.headers["x-pagination-pagetotal"])
        except (KeyError, ValueError, TypeError):
            self._pagination_page_total = None

    def _get_rate_limit_wait(self, response):
        """Return seconds to wait based on the X-RateLimit-Reset header."""
        value = response.headers.get("x-ratelimit-reset")
        if value is not None:
            try:
                return max(float(value) - time.time(), 1)
            except (ValueError, TypeError):
                pass
        return 5

    def get_usage_info(self):
        url = self.get_full_path(QUOTA)
        response_json = self.get_api_json(url)
        return response_json

    def get_audit_log_info(self):
        url = self.get_full_path(AUDIT_LOG)
        response_json = self.get_api_json(url)
        if not response_json:
            response_json = audit_log_resp_good()
        return response_json

    def get_vulnerabilities_info(self):
        url = self.get_full_path(VULNERABILITIES)
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

    def get_parsed_usage_info(self):
        response_json = self.get_usage_info()

        storage_used = -1
        bandwidth_used = -1
        storage_mark = self.UNKNOWN
        bandwidth_mark = self.UNKNOWN
        storage_used_bytes_val = -1
        storage_configured_bytes = -1
        storage_plan_limit_bytes = -1
        bandwidth_used_bytes = -1
        bandwidth_plan_limit_bytes = -1
        bandwidth_configured_bytes = -1

        if "usage" in response_json and "raw" in response_json["usage"]:
            # Extract raw bytes and plan limits
            storage_used_bytes_val = response_json["usage"]["raw"]["storage"].get("used", -1)
            storage_configured_bytes = response_json["usage"]["raw"]["storage"].get("configured", -1)
            storage_plan_limit_bytes = response_json["usage"]["raw"]["storage"].get("plan_limit", -1)
            bandwidth_used_bytes = response_json["usage"]["raw"]["bandwidth"].get("used", -1)
            bandwidth_plan_limit_bytes = response_json["usage"]["raw"]["bandwidth"].get("plan_limit", -1)
            bandwidth_configured_bytes = response_json["usage"]["raw"]["bandwidth"].get("configured", -1)

            if (
                "storage" in response_json["usage"]["raw"]
                and "percentage_used" in response_json["usage"]["raw"]["storage"]
            ):
                # compute storage_used below, but keep this for mark logic
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

        # Convert raw bytes to GB using Cloudsmith's convention (bytes * 1000 / 1024^4)
        storage_used_gb = round(storage_used_bytes_val * 1000 / (1024**4), 2) if storage_used_bytes_val != -1 else -1
        storage_plan_limit_gb = (
            round(storage_plan_limit_bytes * 1000 / (1024**4), 2) if storage_plan_limit_bytes != -1 else -1
        )
        bandwidth_used_gb = round(bandwidth_used_bytes * 1000 / (1024**4), 2) if bandwidth_used_bytes != -1 else -1
        bandwidth_plan_limit_gb = (
            round(bandwidth_plan_limit_bytes * 1000 / (1024**4), 2) if bandwidth_plan_limit_bytes != -1 else -1
        )
        # Configured values in GB
        storage_configured_gb = (
            round(storage_configured_bytes * 1000 / (1024**4), 2) if storage_configured_bytes != -1 else -1
        )
        bandwidth_configured_gb = (
            round(bandwidth_configured_bytes * 1000 / (1024**4), 2) if bandwidth_configured_bytes != -1 else -1
        )

        # Use API-provided percentage (consistent with how bandwidth_used is handled)
        if "usage" in response_json and "raw" in response_json["usage"] and "storage" in response_json["usage"]["raw"]:
            storage_used = response_json["usage"]["raw"]["storage"].get("percentage_used", -1)

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
            "storage_used_bytes": storage_used_bytes_val,
            "storage_plan_limit_bytes": storage_plan_limit_bytes,
            "bandwidth_used_bytes": bandwidth_used_bytes,
            "bandwidth_plan_limit_bytes": bandwidth_plan_limit_bytes,
            "storage_used_gb": storage_used_gb,
            "storage_plan_limit_gb": storage_plan_limit_gb,
            "bandwidth_used_gb": bandwidth_used_gb,
            "bandwidth_plan_limit_gb": bandwidth_plan_limit_gb,
            # Add configured bytes and GB
            "storage_configured_bytes": storage_configured_bytes,
            "bandwidth_configured_bytes": bandwidth_configured_bytes,
            "storage_configured_gb": storage_configured_gb,
            "bandwidth_configured_gb": bandwidth_configured_gb,
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

    def get_repositories_info(self):
        base_url = f"{self.base_url.rstrip('/')}{REPOSITORIES}{self.org}/"
        all_results = []
        page = 1
        page_size = 100

        while True:
            url = f"{base_url}?page={page}&page_size={page_size}"
            response_json = self.get_api_json(url)
            if not response_json:
                if page == 1:
                    self.log.warning("No repositories data found or API call failed.")
                break

            if isinstance(response_json, list):
                page_results = response_json
            elif isinstance(response_json, dict):
                page_results = response_json.get("results", [])
            else:
                self.log.warning("Unexpected response format for repositories endpoint.")
                break

            all_results.extend(page_results)

            if self._pagination_page is not None and self._pagination_page_total is not None:
                if self._pagination_page >= self._pagination_page_total:
                    break
            elif len(page_results) < page_size:
                break

            page += 1

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

    def get_parsed_repositories_info(self):
        response_json = self.get_repositories_info()
        parsed = []
        for item in response_json.get("results", []):
            repository = item.get("slug") or item.get("name") or "unknown"
            repository_type = (item.get("repository_type_str") or "unknown").lower()
            storage_region = item.get("storage_region") or "unknown"
            visibility = "private" if item.get("is_private") else "public" if item.get("is_public") else "unknown"

            parsed.append(
                {
                    "repository": repository,
                    "repository_type": repository_type,
                    "storage_region": storage_region,
                    "visibility": visibility,
                    "storage_bytes": item.get("size", 0) if isinstance(item.get("size"), (int, float)) else 0,
                    "package_count": (
                        item.get("package_count", 0) if isinstance(item.get("package_count"), (int, float)) else 0
                    ),
                    "download_count": (
                        item.get("num_downloads", 0) if isinstance(item.get("num_downloads"), (int, float)) else 0
                    ),
                }
            )

        return parsed

    def get_parsed_vuln_policy_violation_info(self):
        response_json = self.get_vuln_policy_violation_info()
        parsed = []
        for item in response_json.get("results", []):
            scan = item.get("vulnerability_scan_results")
            if not scan or not scan.get("has_vulnerabilities", False):
                continue

            parsed.append(
                {
                    "package": item["package"]["name"] if item.get("package") else "unknown",
                    "policy": item.get("policy", {}).get("name", "unknown"),
                    "violations": scan.get("num_vulnerabilities", 0),
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
            "storage_used_bytes": -1,
            "storage_plan_limit_bytes": -1,
            "bandwidth_used_bytes": -1,
            "bandwidth_plan_limit_bytes": -1,
            "storage_used_gb": -1,
            "storage_plan_limit_gb": -1,
            "bandwidth_used_gb": -1,
            "bandwidth_plan_limit_gb": -1,
            "storage_configured_bytes": -1,
            "bandwidth_configured_bytes": -1,
            "storage_configured_gb": -1,
            "bandwidth_configured_gb": -1,
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

        policy_violations_info = []
        license_violations_info = []
        members_info = []
        repositories_info = []

        global LAST_AUDIT_LOG_STAMP
        global LAST_VULNERABILITY_STAMP
        global AUDIT_LOG_LAST_RUN
        global VULNERABILITY_LAST_RUN

        try:
            usage_info = self.get_parsed_usage_info()
        except Exception as e:
            self.log.warning("Failed to collect usage info, continuing with defaults: %s", e)

        # Org-wide realtime bandwidth
        try:
            self._collect_org_bandwidth()
        except Exception as e:
            self.log.warning("Failed to collect org bandwidth: %s", e)

        # Bandwidth analytics profiles
        try:
            self._collect_bandwidth_profiles()
        except Exception as e:
            self.log.warning("Failed to collect bandwidth profiles: %s", e)

        try:
            repositories_info = self.get_parsed_repositories_info()
        except Exception as e:
            self.log.warning("Failed to collect repositories info, continuing: %s", e)

        # Only run audit log and vulnerability checks if the last check was more than 5 minutes ago
        # This will prevent the check from running too often and hitting the rate limit

        if (time.time() - AUDIT_LOG_LAST_RUN) > 300:
            try:
                audit_log_info = self.get_parsed_audit_log_info()
                AUDIT_LOG_LAST_RUN = time.time()
            except Exception as e:
                self.log.warning("Failed to collect audit log info, continuing with defaults: %s", e)

        if (time.time() - VULNERABILITY_LAST_RUN) > 300:
            try:
                vulnerabilities_info = self.get_parsed_vulnerabilities_info()
                VULNERABILITY_LAST_RUN = time.time()
            except Exception as e:
                self.log.warning("Failed to collect vulnerabilities info, continuing with defaults: %s", e)

        try:
            policy_violations_info = self.get_parsed_vuln_policy_violation_info()
        except Exception as e:
            self.log.warning("Failed to collect vulnerability policy violations, continuing: %s", e)
        for v in policy_violations_info[: self.MAX_EVENTS]:
            event = {
                "timestamp": v["last_detected"],
                "event_type": "vulnerability_policy_violation",
                "msg_title": f"{v['violations']} policy violations for {v['package']}",
                "msg_text": (
                    f"Package: {v['package']}\n"
                    f"Policy: `{v['policy']}`\n"
                    f"Violations: {v['violations']}\n"
                    f"Detected at: {datetime.fromtimestamp(v['last_detected'], tz=timezone.utc).isoformat()}"
                ),
                "aggregation_key": "vulnerability_policy_violation",
                "tags": self.tags + [f"package:{v['package']}", f"policy:{v['policy']}"],
                "host": self.hostname,
            }
            # Ensure tag and source_type_name
            if "tags" not in event or not isinstance(event["tags"], list):
                event["tags"] = self.tags + ["source:cloudsmith"]
            elif "source:cloudsmith" not in event["tags"]:
                event["tags"].append("source:cloudsmith")
            if "source_type_name" not in event:
                event["source_type_name"] = "cloudsmith"
            self.event(event)

        try:
            license_violations_info = self.get_parsed_license_policy_violation_info()
        except Exception as e:
            self.log.warning("Failed to collect license policy violations, continuing: %s", e)

        global LICENSE_VIOLATION_LAST_RUN
        current_time = int(time.time())
        if (current_time - LICENSE_VIOLATION_LAST_RUN) > 300:
            for v in license_violations_info[: self.MAX_EVENTS]:
                event = {
                    "timestamp": v["last_detected"],
                    "event_type": "license_policy_violation",
                    "msg_title": f"License policy violation for {v['package']}",
                    "msg_text": f"Policy `{v['policy']}` triggered a license violation.\nReason: {v['reason']}",
                    "aggregation_key": "license_policy_violation",
                    "tags": self.tags + [f"package:{v['package']}", f"policy:{v['policy']}"],
                }
                if "tags" not in event or not isinstance(event["tags"], list):
                    event["tags"] = self.tags + ["source:cloudsmith"]
                elif "source:cloudsmith" not in event["tags"]:
                    event["tags"].append("source:cloudsmith")
                if "source_type_name" not in event:
                    event["source_type_name"] = "cloudsmith"
                self.event(event)
            LICENSE_VIOLATION_LAST_RUN = current_time
        # Only send new vulnerabilities as events based on LAST_VULNERABILITY_STAMP

        if vulnerabilities_info and len(vulnerabilities_info) > 0:
            new_vulns = [v for v in vulnerabilities_info if v["created_at"] > LAST_VULNERABILITY_STAMP]
            for v in new_vulns[: self.MAX_EVENTS]:
                event = {
                    "timestamp": v["created_at"],
                    "event_type": "vulnerabilities",
                    "msg_title": "{} vulnerability found in package: {} Version: {}".format(
                        v["severity"], v["package_name"], v["package_version"]
                    ),
                    "msg_text": "Number of vulnerabilities: {}. Package URL: {}".format(
                        v["num_vulnerabilities"], v["package_url"]
                    ),
                    "aggregation_key": "vulnerabilities",
                    "tags": self.tags,
                }
                if "tags" not in event or not isinstance(event["tags"], list):
                    event["tags"] = self.tags + ["source:cloudsmith"]
                elif "source:cloudsmith" not in event["tags"]:
                    event["tags"].append("source:cloudsmith")
                if "source_type_name" not in event:
                    event["source_type_name"] = "cloudsmith"
                self.event(event)
            if new_vulns:
                max_created = max(v["created_at"] for v in new_vulns)
                LAST_VULNERABILITY_STAMP = max_created

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck

        self.gauge("cloudsmith.storage_used", usage_info["storage_used"], tags=self.tags)
        self.gauge("cloudsmith.bandwidth_used", usage_info["bandwidth_used"], tags=self.tags)
        self.gauge("cloudsmith.storage_used_bytes", usage_info["storage_used_bytes"], tags=self.tags)
        self.gauge(
            "cloudsmith.storage_plan_limit_bytes",
            usage_info["storage_plan_limit_bytes"],
            tags=self.tags,
        )
        self.gauge("cloudsmith.bandwidth_used_bytes", usage_info["bandwidth_used_bytes"], tags=self.tags)
        self.gauge(
            "cloudsmith.bandwidth_plan_limit_bytes",
            usage_info["bandwidth_plan_limit_bytes"],
            tags=self.tags,
        )
        self.gauge("cloudsmith.storage_used_gb", usage_info["storage_used_gb"], tags=self.tags)
        self.gauge("cloudsmith.storage_plan_limit_gb", usage_info["storage_plan_limit_gb"], tags=self.tags)
        self.gauge("cloudsmith.bandwidth_used_gb", usage_info["bandwidth_used_gb"], tags=self.tags)
        self.gauge(
            "cloudsmith.bandwidth_plan_limit_gb",
            usage_info["bandwidth_plan_limit_gb"],
            tags=self.tags,
        )
        # New: configured bytes and GB
        self.gauge("cloudsmith.storage_configured_bytes", usage_info["storage_configured_bytes"], tags=self.tags)
        self.gauge("cloudsmith.bandwidth_configured_bytes", usage_info["bandwidth_configured_bytes"], tags=self.tags)
        self.gauge("cloudsmith.storage_configured_gb", usage_info["storage_configured_gb"], tags=self.tags)
        self.gauge("cloudsmith.bandwidth_configured_gb", usage_info["bandwidth_configured_gb"], tags=self.tags)
        for repo in repositories_info:
            repository_tags = self.tags + [
                "repository:{}".format(repo["repository"]),
                "repository_type:{}".format(repo["repository_type"]),
                "storage_region:{}".format(repo["storage_region"]),
                "visibility:{}".format(repo["visibility"]),
            ]
            self.gauge("cloudsmith.repository.storage_bytes", repo["storage_bytes"], tags=repository_tags)
            self.gauge("cloudsmith.repository.package_count", repo["package_count"], tags=repository_tags)
            self.gauge("cloudsmith.repository.download_count", repo["download_count"], tags=repository_tags)

        # only create an event if the timestamp is newer than the last event
        # this is to prevent duplicate events as we pull down the entire audit log

        if LAST_AUDIT_LOG_STAMP < audit_log_info[0]["event_at"]:
            for a in audit_log_info[: self.MAX_EVENTS]:
                if a["event_at"] > LAST_AUDIT_LOG_STAMP:
                    event = {
                        "timestamp": a["event_at"],
                        "event_type": "audit logs",
                        "msg_title": "{} on Object: {} (Object Slug: {}".format(
                            a["event"], a["object"], a["object_slug_perm"]
                        ),
                        "msg_text": "Actor: {} ({}) from {}".format(a["actor"], a["actor_kind"], a["city"]),
                        "aggregation_key": "audit_log",
                        "tags": self.tags,
                    }
                    if "tags" not in event or not isinstance(event["tags"], list):
                        event["tags"] = self.tags + ["source:cloudsmith"]
                    elif "source:cloudsmith" not in event["tags"]:
                        event["tags"].append("source:cloudsmith")
                    if "source_type_name" not in event:
                        event["source_type_name"] = "cloudsmith"
                    self.event(event)
            LAST_AUDIT_LOG_STAMP = audit_log_info[0]["event_at"]

        else:
            pass

        storage_msg = "Percentage storage used: {}%".format(usage_info["storage_used"])
        self.service_check(
            "cloudsmith.storage",
            usage_info["storage_mark"],
            message=storage_msg if usage_info["storage_mark"] != AgentCheck.OK else "",
        )

        bandwith_msg = "Percentage bandwidth used: {}%".format(usage_info["bandwidth_used"])
        self.service_check(
            "cloudsmith.bandwidth",
            usage_info["bandwidth_mark"],
            message=bandwith_msg if usage_info["bandwidth_mark"] != AgentCheck.OK else "",
        )

        try:
            members_info = self.get_parsed_members_info()
        except Exception as e:
            self.log.warning("Failed to collect members info, continuing: %s", e)
        for m in members_info:
            self.gauge(
                "cloudsmith.member.active",
                1 if m["is_active"] else 0,
                tags=self.tags
                + [
                    f"user:{m['user']}",
                    f"role:{m['role']}",
                    f"2fa:{m['has_two_factor']}",
                ],
            )

        # Submit additional member metrics (role, login method, 2FA)
        # Initialize counters
        role_counts = {
            "owner": 0,
            "manager": 0,
            "admin": 0,
            "readonly": 0,
        }
        login_method_counts = {
            "saml": 0,
            "password": 0,
        }
        two_factor_enabled_count = 0

        for m in members_info:
            role = m.get("role", "").lower()
            login_method = m.get("last_login_method", "").lower()
            if role in role_counts:
                role_counts[role] += 1
            if login_method in login_method_counts:
                login_method_counts[login_method] += 1
            if m.get("has_two_factor"):
                two_factor_enabled_count += 1

        self.gauge("cloudsmith.member.has_2fa.count", two_factor_enabled_count, tags=self.tags)
        self.gauge("cloudsmith.member.owner.count", role_counts["owner"], tags=self.tags)
        self.gauge("cloudsmith.member.manager.count", role_counts["manager"], tags=self.tags)
        self.gauge("cloudsmith.member.admin.count", role_counts["admin"], tags=self.tags)
        self.gauge("cloudsmith.member.readonly.count", role_counts["readonly"], tags=self.tags)
        self.gauge("cloudsmith.member.saml.count", login_method_counts["saml"], tags=self.tags)
        self.gauge("cloudsmith.member.password.count", login_method_counts["password"], tags=self.tags)

        # Deduplicate by user (slug), not user_name or user_id
        unique_members = {m["user"]: m for m in members_info if "user" in m}.values()
        member_summary = "\n".join(
            f"{m.get('user_name', 'unknown')} ({m.get('role', 'unknown')}), "
            f"2FA: {m.get('has_two_factor', False)}, "
            f"Last Login: "
            f"{datetime.fromtimestamp(m.get('last_login_at', int(time.time())), tz=timezone.utc).isoformat()}, "
            f"Slug: {m.get('user', 'unknown')}"
            for m in unique_members
        )
        event = {
            "timestamp": int(time.time()),
            "event_type": "org_member_summary",
            "msg_title": f"Organization Member Summary ({len(unique_members)} members)",
            "msg_text": member_summary,
            "aggregation_key": "org_members",
            "tags": self.tags,
        }
        if "tags" not in event or not isinstance(event["tags"], list):
            event["tags"] = self.tags + ["source:cloudsmith"]
        elif "source:cloudsmith" not in event["tags"]:
            event["tags"].append("source:cloudsmith")
        if "source_type_name" not in event:
            event["source_type_name"] = "cloudsmith"
        self.event(event)

        # Add violation count gauges for license and vulnerability policy violations
        self.gauge("cloudsmith.license_policy_violation.count", len(license_violations_info), tags=self.tags)
        self.gauge("cloudsmith.vulnerability_policy_violation.count", len(policy_violations_info), tags=self.tags)
