import base64
import gzip
import json
import re
import time
import zlib
from datetime import datetime, timedelta, timezone

import requests

from datadog_checks.base import AgentCheck, ConfigurationError

CHECK_NAME = "huntress"


class HuntressCheck(AgentCheck):
    """Datadog Agent check: polls Huntress SIEM via ES|QL and forwards logs."""

    HUNTRESS_SIEM_ENDPOINT = "/v1/siem/query"
    HUNTRESS_ACCOUNT_ENDPOINT = "/v1/account"
    HUNTRESS_ORGS_ENDPOINT = "/v1/accounts/{account_id}/organizations"
    HUNTRESS_AGENTS_ENDPOINT = "/v1/agents"

    CHECKPOINT_CACHE_KEY_PREFIX = "huntress_last_collected_at_"
    ORG_CACHE_KEY_PREFIX = "huntress_org_cache_"

    MAX_LOGS_PER_BATCH = 1000
    MAX_BATCH_SIZE_BYTES = 4 * 1024 * 1024  # 4 MB headroom under 5 MB limit

    DEFAULT_BASE_URL = "https://api.huntress.io"
    DEFAULT_REQUEST_TIMEOUT = 30
    DEFAULT_MIN_COLLECTION_INTERVAL = 900
    DEFAULT_MAX_PAGES_PER_RUN = 100
    DEFAULT_ORG_CACHE_TTL = 3600
    DEFAULT_AGENT_MAX_PAGES = 20  # 20 × 500/page = up to 10k agents

    SERVICE_CHECK_NAME = "huntress.siem.check_status"

    # Fields present in every response regardless of KEEP clause; logs containing
    # only these keys have no content because the query is missing a KEEP verb.
    _BARE_LOG_KEYS = frozenset({"uuid", "organization_id"})

    def check(self, instance):
        start_time = time.time()

        # Reset per-run rate limit state
        self._last_api_call_limit = None
        self._last_api_call_remaining = None

        api_key = instance.get("huntress_api_key", "").strip()
        secret_key = instance.get("huntress_secret_key", "").strip()
        base_url = instance.get("huntress_base_url", self.DEFAULT_BASE_URL).rstrip("/")
        max_pages = int(instance.get("max_pages_per_run", self.DEFAULT_MAX_PAGES_PER_RUN))
        min_interval = int(instance.get("min_collection_interval", self.DEFAULT_MIN_COLLECTION_INTERVAL))
        enrich_orgs = instance.get("enrich_with_org_tags", True)
        org_ttl = int(instance.get("org_cache_ttl_seconds", self.DEFAULT_ORG_CACHE_TTL))
        extra_tags = list(instance.get("tags", []))
        log_queries = instance.get("log_queries") or []

        metrics_config = instance.get("metrics") or {}
        agents_config = metrics_config.get("agents") or {}
        collect_agents = bool(agents_config.get("enabled", False))
        agents_max_pages = int(agents_config.get("max_pages", self.DEFAULT_AGENT_MAX_PAGES))

        if not api_key:
            raise ConfigurationError("huntress_api_key is required")
        if not secret_key:
            raise ConfigurationError("huntress_secret_key is required")
        if not log_queries and not collect_agents:
            raise ConfigurationError(
                "Configure at least one of: log_queries (for SIEM log collection) "
                "or metrics.agents.enabled: true (for agent metrics)"
            )

        instance_hash = self._instance_hash(instance)
        headers = self._get_auth_header(api_key, secret_key)

        # Org enrichment cache is shared across all queries for this instance
        org_cache = None
        if enrich_orgs and log_queries:
            org_cache = self._get_or_refresh_org_cache(base_url, headers, instance_hash, org_ttl)

        success = False
        run_summary = []

        try:
            for query_def in log_queries:
                query_name = query_def.get("name", "").strip()
                esql = query_def.get("esql_query", "").strip()
                query_tags = list(query_def.get("tags", []))

                if not query_name:
                    raise ConfigurationError("Each entry in log_queries must have a non-empty 'name'")
                if not esql:
                    raise ConfigurationError("Each entry in log_queries must have a non-empty esql_query")
                if not esql.lower().lstrip().startswith("from logs"):
                    raise ConfigurationError(f"esql_query must begin with 'FROM logs' (case-insensitive): {esql!r}")

                # Each query tracks its own checkpoint so queries are independently resumable
                checkpoint_key = instance_hash + "_" + self._query_hash(esql)
                all_tags = extra_tags + query_tags + [f"huntress_log_name:{query_name}"]
                query_metric_tags = extra_tags + [f"query_name:{query_name}"]

                logs, pages, q_start, q_end = self._run_query(
                    base_url, headers, esql, checkpoint_key, max_pages, min_interval, org_cache, all_tags
                )

                self.gauge("huntress.siem.logs_collected", logs, tags=query_metric_tags)
                self.gauge("huntress.siem.pages_fetched", pages, tags=query_metric_tags)
                run_summary.append(
                    f"query '{query_name}': {logs} log(s) collected, {pages} page(s) fetched [{q_start} → {q_end}]"
                )

            if collect_agents:
                agents_total, agents_pages = self._collect_agent_metrics(
                    base_url, headers, extra_tags, agents_max_pages
                )
                run_summary.append(f"agent metrics: {agents_total} agent(s), {agents_pages} page(s) fetched")

            success = True
            self.log.info(
                "Huntress check complete — %s", "; ".join(run_summary) if run_summary else "no data collected"
            )

        except Exception as exc:
            self.log.error("Huntress check run failed: %s", exc)
            self.count("huntress.siem.errors", 1, tags=extra_tags + ["error_type:run_failure"])
            self.service_check(self.SERVICE_CHECK_NAME, self.CRITICAL, tags=extra_tags)
            raise

        finally:
            duration = time.time() - start_time
            self.gauge("huntress.siem.run_duration_seconds", duration, tags=extra_tags)
            if self._last_api_call_limit is not None:
                self.gauge("huntress.siem.api_call_limit", self._last_api_call_limit, tags=extra_tags)
            if self._last_api_call_remaining is not None:
                self.gauge("huntress.siem.api_call_remaining", self._last_api_call_remaining, tags=extra_tags)

        if success:
            self.service_check(self.SERVICE_CHECK_NAME, self.OK, tags=extra_tags)

    # ------------------------------------------------------------------ #
    # Per-query SIEM execution                                              #
    # ------------------------------------------------------------------ #

    def _run_query(self, base_url, headers, esql, checkpoint_key, max_pages, min_interval, org_cache, all_tags):
        """Paginate a single ES|QL query. Returns (logs_collected, pages_fetched, range_start, range_end)."""
        range_start = self._load_checkpoint(checkpoint_key)
        now = datetime.now(timezone.utc)
        range_end = now.strftime("%Y-%m-%dT%H:%M:%S")

        if range_start is None:
            default_start = now - timedelta(seconds=min_interval)
            range_start = default_start.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            # Advance by 1 second so the boundary event isn't re-fetched next run
            try:
                dt = datetime.fromisoformat(range_start.replace("Z", "+00:00"))
                dt = dt + timedelta(seconds=1)
                range_start = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except Exception:
                pass

        self.log.debug(
            "Huntress SIEM query: esql=%r range_start=%s range_end=%s",
            esql[:80],
            range_start,
            range_end,
        )

        service_tag = self._extract_service(all_tags)
        page_token = None
        total_logs = 0
        pages_fetched = 0
        hit_page_cap = False

        while True:
            logs, next_token = self._query_page(base_url, headers, esql, range_start, range_end, page_token)

            if logs:
                if pages_fetched == 0 and all(set(raw.keys()) <= self._BARE_LOG_KEYS for raw in logs[:3]):
                    self.log.warning(
                        "Huntress SIEM query %r returned logs with no content fields "
                        "(only uuid and organization_id). The Huntress API requires an explicit "
                        "KEEP clause to return log fields. Add one to your esql_query, e.g.: "
                        "FROM logs | KEEP @timestamp, message, host.hostname, event.category, event.code, ...",
                        esql[:80],
                    )

                batch = []
                for raw in logs:
                    org_tags = self._get_org_tags(raw, org_cache) if org_cache else []
                    payload = self._transform_log(raw, all_tags + org_tags, service_tag)
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
                        "Huntress SIEM: hit max_pages_per_run=%d for query %r; remaining pages collected next run",
                        max_pages,
                        esql[:60],
                    )
                break

        if not hit_page_cap:
            self._save_checkpoint(checkpoint_key, range_end)

        return total_logs, pages_fetched, range_start, range_end

    # ------------------------------------------------------------------ #
    # Agent metrics                                                         #
    # ------------------------------------------------------------------ #

    def _collect_agent_metrics(self, base_url, headers, extra_tags, max_pages):
        """Fetch all agents and emit platform/status counts as Datadog metrics."""
        agents = []
        page_token = None
        pages_fetched = 0

        while True:
            params = {"limit": 500}
            if page_token:
                params["page_token"] = page_token

            url = base_url + self.HUNTRESS_AGENTS_ENDPOINT
            resp = self._request_with_retry("GET", url, headers, params=params)
            data = resp.json()
            batch = data.get("agents", [])
            agents.extend(batch)
            pages_fetched += 1

            pagination = data.get("pagination", {})
            next_token = pagination.get("next_page_token")
            if next_token and pages_fetched < max_pages:
                page_token = next_token
            else:
                if next_token and pages_fetched >= max_pages:
                    self.log.warning(
                        "Huntress agents: hit max_pages=%d; some agents may be excluded from this run's metrics",
                        max_pages,
                    )
                break

        by_platform = {}
        by_defender_status = {}
        by_firewall_status = {}

        for agent in agents:
            platform = (agent.get("platform") or "unknown").lower()
            by_platform[platform] = by_platform.get(platform, 0) + 1

            def_status = (agent.get("defender_status") or "unknown").lower().replace(" ", "_")
            by_defender_status[def_status] = by_defender_status.get(def_status, 0) + 1

            fw_status = (agent.get("firewall_status") or "unknown").lower().replace(" ", "_")
            by_firewall_status[fw_status] = by_firewall_status.get(fw_status, 0) + 1

        self.gauge("huntress.agents.total", len(agents), tags=extra_tags)
        self.gauge("huntress.agents.pages_fetched", pages_fetched, tags=extra_tags)

        for platform, count in by_platform.items():
            self.gauge("huntress.agents.count", count, tags=extra_tags + [f"platform:{platform}"])

        for status, count in by_defender_status.items():
            self.gauge("huntress.agents.defender_status", count, tags=extra_tags + [f"defender_status:{status}"])

        for status, count in by_firewall_status.items():
            self.gauge("huntress.agents.firewall_status", count, tags=extra_tags + [f"firewall_status:{status}"])

        return len(agents), pages_fetched

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

        response = self._request_with_retry(method="POST", url=url, headers=headers, json_body=body)
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
        timeout = self.init_config.get("request_timeout", self.DEFAULT_REQUEST_TIMEOUT)
        max_retries_5xx = 3
        max_retries_408 = 2
        max_retries_429 = 1
        backoff_5xx = [5, 10, 20]
        backoff_408 = [2, 4]

        attempt = 0
        attempt_429 = 0

        while True:
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=headers,
                    json=json_body,
                    params=params,
                    timeout=timeout,
                )

                if resp.status_code == 200:
                    self._parse_rate_limit_headers(resp)
                    return resp

                if resp.status_code == 400:
                    self.count("huntress.siem.errors", 1, tags=["error_type:bad_request"])
                    raise Exception(f"Huntress API 400 Bad Request: {resp.text}")

                if resp.status_code == 401:
                    self.count("huntress.siem.errors", 1, tags=["error_type:auth_failure"])
                    raise Exception("Huntress API 401 Unauthorized — check huntress_api_key and huntress_secret_key")

                if resp.status_code == 404:
                    raise Exception("Huntress API 404 — SIEM feature may not be enabled on this account")

                if resp.status_code == 408:
                    if attempt < max_retries_408:
                        wait = backoff_408[attempt]
                        self.log.warning(
                            "Huntress API 408 Query Timeout; retrying in %ds (attempt %d/%d)",
                            wait,
                            attempt + 1,
                            max_retries_408,
                        )
                        time.sleep(wait)
                        attempt += 1
                        continue
                    self.count("huntress.siem.errors", 1, tags=["error_type:timeout"])
                    raise Exception("Huntress API 408 Query Timeout — query may be too broad")

                if resp.status_code == 413:
                    raise Exception("Huntress API 413 Memory Limit — narrow the query with KEEP or WHERE clauses")

                if resp.status_code == 422:
                    self.count("huntress.siem.errors", 1, tags=["error_type:invalid_query"])
                    raise Exception(f"Huntress API 422 Invalid ES|QL query: {resp.text}")

                if resp.status_code == 429:
                    if attempt_429 < max_retries_429:
                        self.log.warning(
                            "Huntress API 429 Rate Limited — sleeping 60s then retrying (attempt %d/%d)",
                            attempt_429 + 1,
                            max_retries_429,
                        )
                        time.sleep(60)
                        attempt_429 += 1
                        continue
                    self.count("huntress.siem.errors", 1, tags=["error_type:rate_limited"])
                    raise Exception(
                        "Huntress API 429 Rate Limited after retry — reduce max_pages_per_run or increase min_collection_interval"
                    )

                if 500 <= resp.status_code < 600:
                    if attempt < max_retries_5xx:
                        wait = backoff_5xx[attempt]
                        self.log.warning(
                            "Huntress API %d Server Error; retrying in %ds (attempt %d/%d)",
                            resp.status_code,
                            wait,
                            attempt + 1,
                            max_retries_5xx,
                        )
                        time.sleep(wait)
                        attempt += 1
                        continue
                    self.count("huntress.siem.errors", 1, tags=["error_type:server_error"])
                    raise Exception(f"Huntress API {resp.status_code} Server Error after {max_retries_5xx} retries")

                raise Exception(f"Huntress API unexpected status {resp.status_code}: {resp.text}")

            except requests.exceptions.RequestException as exc:
                if attempt < max_retries_5xx:
                    wait = backoff_5xx[attempt]
                    self.log.warning(
                        "Huntress API network error (%s); retrying in %ds (attempt %d/%d)",
                        exc,
                        wait,
                        attempt + 1,
                        max_retries_5xx,
                    )
                    time.sleep(wait)
                    attempt += 1
                    continue
                self.count("huntress.siem.errors", 1, tags=["error_type:connection_error"])
                raise Exception(f"Huntress API connection error after {max_retries_5xx} retries: {exc}") from exc

    # ------------------------------------------------------------------ #
    # Log transformation                                                    #
    # ------------------------------------------------------------------ #

    def _extract_service(self, tags):
        for tag in tags:
            if tag.startswith("service:"):
                return tag.split(":", 1)[1]
        return "huntress-siem"

    def _transform_log(self, raw_log, tags, service):
        message = raw_log.get("log.original") or raw_log.get("message") or json.dumps(raw_log)

        timestamp = raw_log.get("@timestamp")
        ts_seconds = None
        if timestamp:
            try:
                if isinstance(timestamp, (int, float)):
                    ts_seconds = float(timestamp)
                else:
                    # Truncate sub-microsecond precision (e.g. nanoseconds) that fromisoformat rejects
                    ts_str = re.sub(r'(\.\d{6})\d+', r'\1', str(timestamp)).replace("Z", "+00:00")
                    dt = datetime.fromisoformat(ts_str)
                    ts_seconds = dt.timestamp()
            except Exception:
                pass

        payload = {
            "message": message,
            "ddsource": "huntress",
            "ddtags": ",".join(tags),
            "service": service,
        }
        if ts_seconds is not None:
            payload["timestamp"] = ts_seconds

        # Preserve all ECS fields as top-level log attributes
        for key, value in raw_log.items():
            if key not in ("log.original", "message", "@timestamp"):
                payload[key] = value

        return payload

    # ------------------------------------------------------------------ #
    # Log sending                                                           #
    # ------------------------------------------------------------------ #

    def _send_logs_batch(self, logs_batch):
        api_key = self.agentConfig.get('api_key') or self.agentConfig.get('dd_api_key')
        if not api_key:
            for log_payload in logs_batch:
                self.send_log(log_payload)
            return

        # Split into sub-batches that respect the 5MB uncompressed limit and 1000-entry cap
        sub_batch = []
        sub_batch_bytes = 0
        for log in logs_batch:
            log_bytes = len(json.dumps(log).encode('utf-8'))
            if sub_batch and sub_batch_bytes + log_bytes > self.MAX_BATCH_SIZE_BYTES:
                self._post_logs_to_intake(sub_batch, api_key)
                sub_batch = []
                sub_batch_bytes = 0
            sub_batch.append(log)
            sub_batch_bytes += log_bytes
        if sub_batch:
            self._post_logs_to_intake(sub_batch, api_key)

    def _post_logs_to_intake(self, logs_batch, api_key):
        site = self.agentConfig.get('site') or 'datadoghq.com'
        url = f'https://http-intake.logs.{site}/api/v2/logs'
        timeout = self.init_config.get('request_timeout', self.DEFAULT_REQUEST_TIMEOUT)
        body = gzip.compress(json.dumps(logs_batch).encode('utf-8'))

        for attempt in range(3):
            resp = requests.post(
                url,
                headers={
                    'DD-API-KEY': api_key,
                    'Content-Type': 'application/json',
                    'Content-Encoding': 'gzip',
                },
                data=body,
                timeout=timeout,
            )
            if resp.status_code in (200, 202):
                return
            if resp.status_code in (408, 429, 500, 503) and attempt < 2:
                wait = (attempt + 1) * 5
                self.log.warning(
                    "Datadog Logs intake HTTP %d — retrying in %ds (attempt %d/2)",
                    resp.status_code,
                    wait,
                    attempt + 1,
                )
                time.sleep(wait)
                continue
            raise Exception(f"Datadog Logs intake returned HTTP {resp.status_code}: {resp.text[:200]}")

    # ------------------------------------------------------------------ #
    # Checkpoint                                                            #
    # ------------------------------------------------------------------ #

    def _load_checkpoint(self, checkpoint_key):
        key = self.CHECKPOINT_CACHE_KEY_PREFIX + checkpoint_key
        raw = self.read_persistent_cache(key)
        if not raw:
            return None
        try:
            data = json.loads(raw)
            return data.get("last_collected_at")
        except Exception:
            return None

    def _save_checkpoint(self, checkpoint_key, timestamp_iso):
        key = self.CHECKPOINT_CACHE_KEY_PREFIX + checkpoint_key
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
            resp = self._request_with_retry("GET", url, headers, params={"limit": 500, "page": page})
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

        # Strategy 1: match by organization id (flat field from API, dot-notation, or nested)
        org_id = (
            raw_log.get("organization_id")
            or raw_log.get("organization.id")
            or (raw_log.get("organization", {}).get("id") if isinstance(raw_log.get("organization"), dict) else None)
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
    # Hashing                                                              #
    # ------------------------------------------------------------------ #

    def _instance_hash(self, instance):
        """Stable non-secret identifier for this Huntress instance."""
        key = instance.get("instance_id") or instance.get("huntress_base_url", self.DEFAULT_BASE_URL)
        return format(zlib.crc32(key.encode("utf-8")) & 0xFFFFFFFF, "08x")

    def _query_hash(self, esql_query):
        """Short non-cryptographic checksum for a per-query checkpoint key."""
        return format(zlib.crc32(esql_query.encode("utf-8")) & 0xFFFFFFFF, "08x")
