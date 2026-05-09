import base64
import json
import time
from datetime import datetime, timezone
from urllib.parse import urljoin

from datadog_checks.base import AgentCheck, ConfigurationError

SERVICE_CHECK_NAME = "eden.api.can_connect"
DEFAULT_RANGE_SECONDS = 300
DEFAULT_LIMIT = 5000
DEFAULT_TOKEN_REFRESH_WINDOW_SECONDS = 120
MAX_PAGES_PER_GROUP = 20

ALL_GROUPS = (
    "analytics",
    "eden",
    "iam",
    "endpoint",
    "metadata",
    "migration",
    "proxy",
    "snapshot",
    "workload",
)

INTERNAL_LABELS = frozenset({
    "positive_offset",
    "negative_offset",
    "scale",
    "zero_count",
    "bucket_bounds",
    "bucket_counts",
    "eden_node_uuid",
})


class EdenCheck(AgentCheck):
    def __init__(self, *args, **kwargs):
        super(EdenCheck, self).__init__(*args, **kwargs)
        self._auth_cache = {}

    def check(self, instance):
        url = instance.get("url")
        if not url:
            raise ConfigurationError("`url` is required in eden.yaml")

        groups = instance.get("metric_groups") or list(ALL_GROUPS)
        range_seconds = int(instance.get("range_seconds")
                            or DEFAULT_RANGE_SECONDS)
        limit = int(instance.get("limit") or DEFAULT_LIMIT)
        base_tags = list(instance.get("tags") or [])
        self._validate_robot_config(instance)

        endpoint = urljoin(url.rstrip("/") + "/", "api/v1/analytics/telemetry")
        cursor_key = self._cursor_key(instance, groups)
        last_seen = self._load_cursor(cursor_key)
        now_iso = datetime.now(timezone.utc).isoformat()

        try:
            token = self._get_token(instance)
            headers = {"Authorization": f"Bearer {token}",
                       "Accept": "application/json"}
            for group in groups:
                self._fetch_group(
                    endpoint,
                    headers,
                    instance,
                    group,
                    range_seconds,
                    limit,
                    last_seen,
                    now_iso,
                    base_tags,
                )
        except Exception as exc:
            self.service_check(
                SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=str(exc), tags=base_tags)
            return

        self.service_check(SERVICE_CHECK_NAME, AgentCheck.OK, tags=base_tags)
        self._save_cursor(cursor_key, now_iso)

    def _fetch_group(self, endpoint, headers, instance, group, range_seconds, limit, last_seen, now_iso, base_tags):
        offset = 0
        for _ in range(MAX_PAGES_PER_GROUP):
            params = {
                "signal": "metrics",
                "range": f"{range_seconds}s",
                "limit": str(limit),
                "offset": str(offset),
                "order": "asc",
            }
            if group:
                params["group"] = group
            if last_seen:
                params["from"] = last_seen
                params["to"] = now_iso

            response = self.http.get(
                endpoint, params=params, extra_headers=headers.copy())
            if getattr(response, "status_code", None) == 401:
                token = self._login(instance, force=True)
                headers["Authorization"] = f"Bearer {token}"
                response = self.http.get(
                    endpoint, params=params, extra_headers=headers.copy())
            response.raise_for_status()

            rows = response.json().get("rows", [])
            self._emit_rows(rows, base_tags)
            if len(rows) < limit:
                return
            offset += limit

    def _emit_rows(self, rows, base_tags):
        for row in rows:
            name = row.get("metric_name")
            if not name:
                continue
            tags = list(base_tags)
            tags.append(f"eden_group:{row.get('group', 'unknown')}")
            if row.get("service_name"):
                # `service` is a Datadog-reserved generic tag, so namespace under `eden_service`.
                tags.append(f"eden_service:{row['service_name']}")
            if row.get("node_uuid"):
                tags.append(f"eden_node_uuid:{row['node_uuid']}")
            if row.get("scope"):
                tags.append(f"scope:{row['scope']}")
            for key, value in (row.get("labels") or {}).items():
                if key in INTERNAL_LABELS:
                    continue
                tags.append(f"{key}:{value}")

            metric_name = self._metric_name(row)
            kind = (row.get("metric_kind") or "").lower()
            value = row.get("value")
            count = row.get("count")
            total = row.get("sum")

            if kind in ("counter", "sum"):
                delta = count if count is not None else value
                if delta is not None:
                    self.monotonic_count(metric_name, delta, tags=tags)
            elif kind == "histogram":
                if count is not None:
                    self.monotonic_count(
                        f"{metric_name}.count", count, tags=tags)
                if total is not None:
                    self.monotonic_count(
                        f"{metric_name}.sum", total, tags=tags)
                if count and total is not None:
                    self.gauge(f"{metric_name}.avg", total / count, tags=tags)
            elif kind == "exponential_histogram":
                if count is not None:
                    self.monotonic_count(
                        f"{metric_name}.count", count, tags=tags)
                if total is not None:
                    self.monotonic_count(
                        f"{metric_name}.sum", total, tags=tags)
                if count and total is not None:
                    self.gauge(f"{metric_name}.avg", total / count, tags=tags)
            elif value is not None:
                self.gauge(metric_name, value, tags=tags)

    def _metric_name(self, row):
        # Mirror DogStatsD naming: prefix is `scope`, body is `metric_name` with
        # the scope/group token stripped and `_` separators turned into `.`.
        name = row["metric_name"]
        scope = row.get("scope") or row.get("group") or ""
        group = row.get("group") or ""

        body = name
        for token in (scope, scope.replace(".", "_"), group, "eden." + group):
            if token and body.startswith(token + "_"):
                body = body[len(token) + 1:]
                break
            if token and body.startswith(token + "."):
                body = body[len(token) + 1:]
                break

        if scope and body:
            metric = f"{scope}.{body}"
        elif scope:
            metric = scope
        else:
            metric = body or name

        # Tile is registered with the `eden.` prefix in manifest.json; metrics not
        # already under that namespace are prefixed so they show up in the tile.
        # NOTE: this diverges from Eden's DogStatsD exporter, which emits some
        # metrics (proxy.*, workload.*, analytics.*) without the `eden.` prefix.
        # The two paths should be aligned -- see README "Known divergence with
        # DogStatsD direct export".
        if metric.startswith("eden.") or metric.startswith("eden_"):
            return metric
        return f"eden.{metric}"

    def _get_token(self, instance):
        self._validate_robot_config(instance)
        cache_key = self._auth_cache_key(instance)
        cached = self._auth_cache.get(cache_key) or {}
        now = time.time()
        refresh_window = int(instance.get(
            "token_refresh_window_seconds") or DEFAULT_TOKEN_REFRESH_WINDOW_SECONDS)
        expires_at = cached.get("expires_at")

        if cached.get("token") and (expires_at is None or expires_at - refresh_window > now):
            return cached["token"]

        return self._login(instance)

    def _login(self, instance, force=False):
        cache_key = self._auth_cache_key(instance)
        if force:
            self._auth_cache.pop(cache_key, None)

        url = instance["url"]
        headers = {"Accept": "application/json"}
        self._add_org_header(headers, instance)

        endpoint = urljoin(url.rstrip("/") + "/", "api/v1/auth/robots/login")
        response = self.http.post(
            endpoint,
            json={
                "username": instance["robot_username"],
                "api_key": instance["robot_api_key"],
            },
            extra_headers=headers,
        )
        response.raise_for_status()
        token = self._extract_token(response.json())
        self._auth_cache[cache_key] = {
            "token": token,
            "expires_at": self._token_expiry(token),
        }
        return token

    def _validate_robot_config(self, instance):
        if not (instance.get("org_id") or instance.get("org_uuid")):
            raise ConfigurationError(
                "`org_id` or `org_uuid` is required in eden.yaml")
        if not (instance.get("robot_username") and instance.get("robot_api_key")):
            raise ConfigurationError(
                "`robot_username` and `robot_api_key` are required in eden.yaml")

    def _auth_cache_key(self, instance):
        return (
            instance["url"].rstrip("/"),
            instance.get("org_id"),
            instance.get("org_uuid"),
            instance.get("robot_username"),
        )

    def _add_org_header(self, headers, instance):
        if instance.get("org_uuid"):
            headers["X-Org-Uuid"] = instance["org_uuid"]
        elif instance.get("org_id"):
            headers["X-Org-Id"] = instance["org_id"]

    def _extract_token(self, payload):
        token = payload.get("token")
        if not token:
            raise ConfigurationError(
                "Eden login response did not include a JWT token")
        return token

    def _token_expiry(self, token):
        try:
            payload = token.split(".")[1]
            payload += "=" * (-len(payload) % 4)
            claims = json.loads(base64.urlsafe_b64decode(
                payload.encode("ascii")).decode("utf-8"))
            return int(claims["exp"])
        except Exception:
            return None

    def _cursor_key(self, instance, groups):
        normalized_groups = ",".join(sorted(groups))
        return "::".join(
            [
                "eden_cursor",
                instance["url"].rstrip("/"),
                instance.get("org_id") or "",
                instance.get("org_uuid") or "",
                normalized_groups,
            ]
        )

    def _load_cursor(self, key):
        return self.read_persistent_cache(key) or None

    def _save_cursor(self, key, value):
        self.write_persistent_cache(key, value)
