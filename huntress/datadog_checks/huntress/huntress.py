import base64
import gzip
import hashlib
import json
import time
from datetime import datetime, timedelta, timezone

import requests
from datadog_checks.base import AgentCheck, ConfigurationError

CHECK_NAME = "huntress"


class HuntressCheck(AgentCheck):
    """Datadog Agent check: polls Huntress SIEM via ES|QL and forwards logs."""

    HUNTRESS_SIEM_ENDPOINT = "/v1/siem/query"
    HUNTRESS_ACCOUNT_ENDPOINT = "/v1/account"
    HUNTRESS_ORGS_ENDPOINT = "/v1/accounts/{account_id}/organizations"

    CHECKPOINT_CACHE_KEY_PREFIX = "huntress_last_collected_at_"
    ORG_CACHE_KEY_PREFIX = "huntress_org_cache_"

    MAX_LOGS_PER_BATCH = 1000
    MAX_BATCH_SIZE_BYTES = 4 * 1024 * 1024  # 4 MB headroom under 5 MB limit

    DEFAULT_BASE_URL = "https://api.huntress.io"
    DEFAULT_MIN_COLLECTION_INTERVAL = 900
    DEFAULT_MAX_PAGES_PER_RUN = 100
    DEFAULT_ORG_CACHE_TTL = 3600

    SERVICE_CHECK_NAME = "huntress.siem.check_status"

    def check(self, instance):
        start_time = time.time()

        # Reset per-run rate limit state
        self._last_api_call_limit = None
        self._last_api_call_remaining = None

        api_key = instance.get("huntress_api_key", "").strip()
        secret_key = instance.get("huntress_secret_key", "").strip()
        esql_query = instance.get("esql_query", "").strip()
        base_url = instance.get("huntress_base_url", self.DEFAULT_BASE_URL).rstrip("/")
        max_pages = int(instance.get("max_pages_per_run", self.DEFAULT_MAX_PAGES_PER_RUN))
        min_interval = int(instance.get("min_collection_interval", self.DEFAULT_MIN_COLLECTION_INTERVAL))
        enrich_orgs = instance.get("enrich_with_org_tags", True)
        org_ttl = int(instance.get("org_cache_ttl_seconds", self.DEFAULT_ORG_CACHE_TTL))
        extra_tags = list(instance.get("tags", []))

        if not api_key:
            raise ConfigurationError("huntress_api_key is required")
        if not secret_key:
            raise ConfigurationError("huntress_secret_key is required")
        if not esql_query:
            raise ConfigurationError("esql_query is required")
        if not esql_query.lower().lstrip().startswith("from logs"):
            raise ConfigurationError("esql_query must begin with 'FROM logs' (case-insensitive)")

        instance_hash = self._instance_hash(instance)
        headers = self._get_auth_header(api_key, secret_key)

        # Org enrichment
        org_cache = None
        if enrich_orgs:
            org_cache = self._get_or_refresh_org_cache(
                base_url, headers, instance_hash, org_ttl
            )

        # Checkpoint
        range_start = self._load_checkpoint(instance_hash)
        now = datetime.now(timezone.utc)
        range_end = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        if range_start is None:
            default_start = now - timedelta(seconds=min_interval)
            range_start = default_start.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        else:
            # Add 1ms offset to avoid re-fetching the last millisecond from previous run
            try:
                dt = datetime.fromisoformat(range_start.replace("Z", "+00:00"))
                dt = dt + timedelta(milliseconds=1)
                range_start = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            except Exception:
                pass

        self.log.debug(
            "Huntress SIEM collection: range_start=%s range_end=%s", range_start, range_end
        )

        page_token = None
        total_logs = 0
        pages_fetched = 0
        hit_page_cap = False
        success = False

        try:
            while True:
                logs, next_token = self._query_page(
                    base_url, headers, esql_query, range_start, range_end, page_token
                )

                if logs:
                    service_tag = self._extract_service(extra_tags)
                    batch = []
                    for raw in logs:
                        org_tags = self._get_org_tags(raw, org_cache) if org_cache else []
                        all_tags = extra_tags + org_tags
                        payload = self._transform_log(raw, all_tags, service_tag)
                        batch.append(payload)
                        if len(batch) >= self.MAX_LOGS_PER_BATCH:
                            self._send_logs_batch(batch)
                            batch = []
                    if batch:
                        self._send_logs_batch(batch)

                total_logs += len(logs)
                pages_fetched += 1

                if next_token and pages_fetched < max_pages:
                    page_token = next_token
                else:
                    if next_token and pages_fetched >= max_pages:
                        hit_page_cap = True
                        self.log.warning(
                            "Huntress SIEM: hit max_pages_per_run=%d cap; "
                            "remaining pages will be collected next run",
                            max_pages,
                        )
                    break

            if not hit_page_cap:
                self._save_checkpoint(instance_hash, range_end)

            success = True

        except Exception as exc:
            self.log.error("Huntress SIEM run failed: %s", exc)
            self.count(
                "huntress.siem.errors",
                1,
                tags=extra_tags + ["error_type:run_failure"],
            )
            self.service_check(self.SERVICE_CHECK_NAME, self.CRITICAL, tags=extra_tags)
            raise

        finally:
            duration = time.time() - start_time
            self.gauge("huntress.siem.run_duration_seconds", duration, tags=extra_tags)
            self.gauge("huntress.siem.logs_collected", total_logs, tags=extra_tags)
            self.gauge("huntress.siem.pages_fetched", pages_fetched, tags=extra_tags)
            if self._last_api_call_limit is not None:
                self.gauge("huntress.siem.api_call_limit", self._last_api_call_limit, tags=extra_tags)
            if self._last_api_call_remaining is not None:
                self.gauge("huntress.siem.api_call_remaining", self._last_api_call_remaining, tags=extra_tags)

        if success:
            self.service_check(self.SERVICE_CHECK_NAME, self.OK, tags=extra_tags)

    # ------------------------------------------------------------------ #
    # Auth                                                                  #
    # ------------------------------------------------------------------ #

    def _get_auth_header(self, api_key, secret_key):
        token = base64.b64encode(f"{api_key}:{secret_key}".encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _parse_rate_limit_headers(self, resp):
        """Parse x-huntress-api-call-limit / x-huntress-api-call-remaining headers."""
        try:
            limit = resp.headers.get("x-huntress-api-call-limit")
            if limit is not None:
                self._last_api_call_limit = int(limit)
        except (ValueError, TypeError, AttributeError):
            pass
        try:
            remaining = resp.headers.get("x-huntress-api-call-remaining")
            if remaining is not None:
                self._last_api_call_remaining = int(remaining)
                if self._last_api_call_remaining < 10:
                    self.log.warning(
                        "Huntress API rate limit nearly exhausted: %d/%d requests remaining this minute",
                        self._last_api_call_remaining,
                        self._last_api_call_limit or 60,
                    )
        except (ValueError, TypeError, AttributeError):
            pass

    # ------------------------------------------------------------------ #
    # SIEM query                                                            #
    # ------------------------------------------------------------------ #

    def _query_page(self, base_url, headers, esql, range_start, range_end, page_token=None):
        """POST /v1/siem/query; return (logs_list, next_page_token | None)."""
        url = base_url + self.HUNTRESS_SIEM_ENDPOINT
        body = {"esql": esql, "range_start": range_start, "range_end": range_end}
        if page_token:
            body["page_token"] = page_token

        response = self._request_with_retry(
            method="POST",
            url=url,
            headers=headers,
            json_body=body,
        )

        data = response.json()
        logs = data.get("logs", [])
        pagination = data.get("pagination", {})
        next_token = pagination.get("next_page_token")
        return logs, next_token

    # ------------------------------------------------------------------ #
    # HTTP with retry / error handling                                       #
    # ------------------------------------------------------------------ #

    def _request_with_retry(self, method, url, headers, json_body=None, params=None):
        """Execute an HTTP request with retry logic per PRD §7."""
        max_retries_5xx = 3
        max_retries_408 = 2
        backoff_5xx = [5, 10, 20]
        backoff_408 = [2, 4]

        attempt = 0
        last_exc = None

        while True:
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=headers,
                    json=json_body,
                    params=params,
                    timeout=30,
                )

                if resp.status_code == 200:
                    self._parse_rate_limit_headers(resp)
                    return resp

                if resp.status_code == 400:
                    self.count(
                        "huntress.siem.errors", 1,
                        tags=["error_type:bad_request"]
                    )
                    raise Exception(
                        f"Huntress API 400 Bad Request: {resp.text}"
                    )

                if resp.status_code == 401:
                    self.count(
                        "huntress.siem.errors", 1,
                        tags=["error_type:auth_failure"]
                    )
                    raise Exception(
                        "Huntress API 401 Unauthorized — check huntress_api_key and huntress_secret_key"
                    )

                if resp.status_code == 404:
                    raise Exception(
                        "Huntress API 404 — SIEM feature may not be enabled on this account"
                    )

                if resp.status_code == 408:
                    if attempt < max_retries_408:
                        wait = backoff_408[attempt]
                        self.log.warning(
                            "Huntress API 408 Query Timeout; retrying in %ds (attempt %d/%d)",
                            wait, attempt + 1, max_retries_408,
                        )
                        time.sleep(wait)
                        attempt += 1
                        continue
                    self.count(
                        "huntress.siem.errors", 1,
                        tags=["error_type:timeout"]
                    )
                    raise Exception("Huntress API 408 Query Timeout — query may be too broad")

                if resp.status_code == 413:
                    raise Exception(
                        "Huntress API 413 Memory Limit — narrow the query with KEEP or WHERE clauses"
                    )

                if resp.status_code == 422:
                    self.count(
                        "huntress.siem.errors", 1,
                        tags=["error_type:invalid_query"]
                    )
                    raise Exception(
                        f"Huntress API 422 Invalid ES|QL query: {resp.text}"
                    )

                if resp.status_code == 429:
                    self.log.warning(
                        "Huntress API 429 Rate Limited — sleeping 60s then retrying"
                    )
                    time.sleep(60)
                    continue

                if 500 <= resp.status_code < 600:
                    if attempt < max_retries_5xx:
                        wait = backoff_5xx[attempt]
                        self.log.warning(
                            "Huntress API %d Server Error; retrying in %ds (attempt %d/%d)",
                            resp.status_code, wait, attempt + 1, max_retries_5xx,
                        )
                        time.sleep(wait)
                        attempt += 1
                        continue
                    self.count(
                        "huntress.siem.errors", 1,
                        tags=["error_type:server_error"]
                    )
                    raise Exception(
                        f"Huntress API {resp.status_code} Server Error after {max_retries_5xx} retries"
                    )

                raise Exception(
                    f"Huntress API unexpected status {resp.status_code}: {resp.text}"
                )

            except requests.exceptions.RequestException as exc:
                last_exc = exc
                if attempt < max_retries_5xx:
                    wait = backoff_5xx[attempt]
                    self.log.warning(
                        "Huntress API network error (%s); retrying in %ds (attempt %d/%d)",
                        exc, wait, attempt + 1, max_retries_5xx,
                    )
                    time.sleep(wait)
                    attempt += 1
                    continue
                self.count(
                    "huntress.siem.errors", 1,
                    tags=["error_type:connection_error"]
                )
                raise Exception(
                    f"Huntress API connection error after {max_retries_5xx} retries: {exc}"
                ) from exc

    # ------------------------------------------------------------------ #
    # Log transformation                                                    #
    # ------------------------------------------------------------------ #

    def _extract_service(self, tags):
        for tag in tags:
            if tag.startswith("service:"):
                return tag.split(":", 1)[1]
        return "huntress-siem"

    def _transform_log(self, raw_log, tags, service):
        message = (
            raw_log.get("log.original")
            or raw_log.get("message")
            or json.dumps(raw_log)
        )

        timestamp = raw_log.get("@timestamp")
        date_ms = None
        if timestamp:
            try:
                if isinstance(timestamp, (int, float)):
                    date_ms = int(timestamp)
                else:
                    dt = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
                    date_ms = int(dt.timestamp() * 1000)
            except Exception:
                pass

        payload = {
            "message": message,
            "ddsource": "huntress",
            "ddtags": ",".join(tags),
            "service": service,
        }
        if date_ms is not None:
            payload["date"] = date_ms

        # Preserve all ECS fields as top-level log attributes
        for key, value in raw_log.items():
            if key not in ("log.original", "message", "@timestamp"):
                payload[key] = value

        return payload

    # ------------------------------------------------------------------ #
    # Log sending                                                           #
    # ------------------------------------------------------------------ #

    def _send_logs_batch(self, logs_batch):
        """Send a batch of up to MAX_LOGS_PER_BATCH log payloads via self.send_log()."""
        for log_payload in logs_batch:
            self.send_log(log_payload)

    # ------------------------------------------------------------------ #
    # Checkpoint                                                            #
    # ------------------------------------------------------------------ #

    def _load_checkpoint(self, instance_hash):
        key = self.CHECKPOINT_CACHE_KEY_PREFIX + instance_hash
        raw = self.read_persistent_cache(key)
        if not raw:
            return None
        try:
            data = json.loads(raw)
            return data.get("last_collected_at")
        except Exception:
            return None

    def _save_checkpoint(self, instance_hash, timestamp_iso):
        key = self.CHECKPOINT_CACHE_KEY_PREFIX + instance_hash
        payload = json.dumps({"last_collected_at": timestamp_iso, "schema_version": 1})
        self.write_persistent_cache(key, payload)

    # ------------------------------------------------------------------ #
    # Org metadata enrichment                                               #
    # ------------------------------------------------------------------ #

    def _get_or_refresh_org_cache(self, base_url, headers, instance_hash, ttl_seconds):
        """Return the org cache dict, refreshing if stale or absent."""
        cached = self._load_org_cache(instance_hash)
        if cached:
            try:
                fetched_at_str = cached.get("fetched_at", "")
                fetched_at = datetime.fromisoformat(fetched_at_str.replace("Z", "+00:00"))
                age = (datetime.now(timezone.utc) - fetched_at).total_seconds()
                if ttl_seconds == 0 or age < ttl_seconds:
                    return cached
            except Exception:
                pass

        try:
            account_id = self._get_account_id(base_url, headers)
            orgs = self._fetch_org_cache(base_url, headers, account_id)
            cache_payload = {
                "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                "account_id": account_id,
                "orgs": orgs,
            }
            self._save_org_cache(instance_hash, cache_payload)
            return cache_payload
        except Exception as exc:
            self.log.warning(
                "Huntress: failed to fetch org metadata — logs will be collected without org tags: %s",
                exc,
            )
            return None

    def _get_account_id(self, base_url, headers):
        url = base_url + self.HUNTRESS_ACCOUNT_ENDPOINT
        resp = self._request_with_retry("GET", url, headers)
        data = resp.json()
        account = data.get("account", data)
        return account["id"]

    def _fetch_org_cache(self, base_url, headers, account_id):
        """Paginate /v1/accounts/{id}/organizations; return {org_id_str: {...}} dict."""
        orgs = {}
        page = 1
        while True:
            url = base_url + self.HUNTRESS_ORGS_ENDPOINT.format(account_id=account_id)
            resp = self._request_with_retry(
                "GET", url, headers, params={"limit": 500, "page": page}
            )
            data = resp.json()
            org_list = data.get("organizations", [])
            for org in org_list:
                orgs[str(org["id"])] = {
                    "name": org.get("name", ""),
                    "key": org.get("key", ""),
                    "account_id": account_id,
                }
            pagination = data.get("pagination", {})
            if pagination.get("next_page_token") or (
                pagination.get("current_page", 1) < pagination.get("total_pages", 1)
            ):
                page += 1
            else:
                break
        return orgs

    def _load_org_cache(self, instance_hash):
        key = self.ORG_CACHE_KEY_PREFIX + instance_hash
        raw = self.read_persistent_cache(key)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    def _save_org_cache(self, instance_hash, cache_payload):
        key = self.ORG_CACHE_KEY_PREFIX + instance_hash
        self.write_persistent_cache(key, json.dumps(cache_payload))

    def _get_org_tags(self, raw_log, org_cache):
        """Match a log record to an org in the cache; return list of tag strings."""
        if not org_cache:
            return []

        account_id = org_cache.get("account_id")
        orgs = org_cache.get("orgs", {})

        base_tags = []
        if account_id is not None:
            base_tags.append(f"huntress_account_id:{account_id}")

        # Strategy 1: match by organization.id
        org_id = raw_log.get("organization.id") or (
            raw_log.get("organization", {}).get("id") if isinstance(raw_log.get("organization"), dict) else None
        )
        if org_id is not None:
            org = orgs.get(str(org_id))
            if org:
                return base_tags + [
                    f"huntress_org_id:{org_id}",
                    f"huntress_org_name:{org['name']}",
                    f"huntress_org_key:{org['key']}",
                ]

        # Strategy 2: match by organization.name (reverse lookup)
        org_name = raw_log.get("organization.name") or (
            raw_log.get("organization", {}).get("name") if isinstance(raw_log.get("organization"), dict) else None
        )
        if org_name:
            for oid, org in orgs.items():
                if org.get("name") == org_name:
                    return base_tags + [
                        f"huntress_org_id:{oid}",
                        f"huntress_org_name:{org['name']}",
                        f"huntress_org_key:{org['key']}",
                    ]

        # Strategy 3: account-level tag only
        return base_tags

    # ------------------------------------------------------------------ #
    # Instance hash                                                         #
    # ------------------------------------------------------------------ #

    def _instance_hash(self, instance):
        key = f"{instance.get('huntress_api_key', '')}:{instance.get('esql_query', '')}"
        return hashlib.md5(key.encode()).hexdigest()[:12]
