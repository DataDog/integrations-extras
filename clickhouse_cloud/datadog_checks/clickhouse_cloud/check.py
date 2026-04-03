"""
ClickHouse Cloud custom Datadog Agent check for log collection.

Collects query logs (system.query_log) and server logs (system.text_log)
from ClickHouse Cloud via the Cloud Query API and ships them to Datadog Logs.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from datadog_checks.base import AgentCheck

# ---------------------------------------------------------------------------
# SQL templates
# ---------------------------------------------------------------------------

QUERY_LOG_SQL = """
SELECT
    event_time,
    toUnixTimestamp64Micro(event_time_microseconds) AS cursor_us,
    query_id,
    user,
    query_duration_ms,
    memory_usage,
    read_rows,
    read_bytes,
    result_rows,
    written_rows,
    written_bytes,
    exception,
    exception_code,
    query,
    type,
    query_kind,
    current_database,
    arrayStringConcat(tables, ', ') AS tables,
    client_name
FROM system.query_log
WHERE type IN ('QueryFinish', 'ExceptionWhileProcessing', 'ExceptionBeforeStart')
  AND is_initial_query = 1
  AND event_time_microseconds > fromUnixTimestamp64Micro({last_cursor})
  AND query NOT LIKE '%system.query_log%'
  AND query NOT LIKE '%system.text_log%'
  {internal_user_filter}
ORDER BY event_time_microseconds ASC
LIMIT {batch_size}
"""

# Filter clause injected into QUERY_LOG_SQL when exclude_internal_users is True.
# ClickHouse Cloud runs health checks, backups, and observability queries under
# service accounts whose usernames follow several patterns:
#   1. "*-internal" suffix (monitoring-internal, operator-internal, backups-internal, etc.)
#   2. "clickhouse-cloud-*" prefix (clickhouse-cloud-monitor — the primary metrics scraper)
#   3. "prometheus-exporter" — Prometheus metrics collection
#   4. Empty string "" — internal system-level metrics queries (SELECT from
#      system.dimensional_metrics, system.histogram_metrics, etc.) that run
#      under a blank user and generate heavy query_log volume.
# Together these generate ~99% of query_log volume on an idle cluster with zero
# operational value for application teams.
INTERNAL_USER_FILTER = (
    "AND user NOT LIKE '%-internal'"
    " AND user NOT LIKE 'clickhouse-cloud-%'"
    " AND user != 'prometheus-exporter'"
    " AND user != ''"
)

TEXT_LOG_SQL = """
SELECT
    event_time,
    toUnixTimestamp64Micro(event_time_microseconds) AS cursor_us,
    level,
    logger_name,
    message,
    thread_id,
    query_id
FROM system.text_log
WHERE level IN ('Fatal', 'Critical', 'Error', 'Warning')
  AND event_time_microseconds > fromUnixTimestamp64Micro({last_cursor})
  AND logger_name NOT IN ('QueryProfiler', 'GlobalProfiler')
ORDER BY event_time_microseconds ASC
LIMIT {batch_size}
"""

# ---------------------------------------------------------------------------
# Cursor cache keys
# ---------------------------------------------------------------------------

CURSOR_QUERY_LOG = "clickhouse_cloud.cursor.query_log"
CURSOR_TEXT_LOG = "clickhouse_cloud.cursor.text_log"

# ---------------------------------------------------------------------------
# ClickHouse query_log type names (returned as strings by the Cloud Query API)
# ---------------------------------------------------------------------------

TYPE_QUERY_FINISH = "QueryFinish"
TYPE_QUERY_EXCEPTION = "ExceptionWhileProcessing"
TYPE_QUERY_EXCEPTION_BEFORE_START = "ExceptionBeforeStart"

# ---------------------------------------------------------------------------
# Datadog metric / service-check names
# ---------------------------------------------------------------------------

SC_QUERY_LOG_CONNECT = "clickhouse_cloud.query_log.can_connect"
SC_TEXT_LOG_CONNECT = "clickhouse_cloud.text_log.can_connect"
GAUGE_QUERY_LOG_ROWS = "clickhouse_cloud.query_log.rows_collected"
GAUGE_TEXT_LOG_ROWS = "clickhouse_cloud.text_log.rows_collected"

# ---------------------------------------------------------------------------
# Datadog log level mappings for system.text_log
# ---------------------------------------------------------------------------

TEXT_LOG_LEVEL_MAP: dict[str, str] = {
    "Fatal": "critical",
    "Critical": "critical",
    "Error": "error",
    "Warning": "warning",
}

# ---------------------------------------------------------------------------
# Config validation bounds
# ---------------------------------------------------------------------------

MIN_BATCH_SIZE = 1
MAX_BATCH_SIZE = 10_000
MIN_SLOW_QUERY_MS = 0
MAX_SLOW_QUERY_MS = 3_600_000  # 1 hour
MIN_BACKFILL_MINUTES = 1
MAX_BACKFILL_MINUTES = 1440  # 24 hours
MIN_TIMEOUT_SECONDS = 5
MAX_TIMEOUT_SECONDS = 300


class ClickHouseCloudCheck(AgentCheck):
    """Datadog Agent check that collects logs from ClickHouse Cloud system tables."""

    def __init__(self, name: str, init_config: dict[str, Any], instances: list[dict[str, Any]]) -> None:
        super().__init__(name, init_config, instances)

        inst: dict[str, Any] = self.instance  # type: ignore[attr-defined]

        # Required credentials
        self.service_id: str = inst['service_id']
        self.key_id: str = inst['key_id']
        self.key_secret: str = inst['key_secret']

        # Feature toggles
        self.collect_query_logs: bool = inst.get('collect_query_logs', True)
        self.collect_text_logs: bool = inst.get('collect_text_logs', True)
        self.exclude_internal_users: bool = inst.get('exclude_internal_users', True)

        # Tuning — validate all numeric config to prevent SQL injection and
        # catch misconfiguration early (e.g. log_batch_size: "all").
        self.batch_size: int = self._validate_int(
            inst,
            'log_batch_size',
            default=1000,
            lo=MIN_BATCH_SIZE,
            hi=MAX_BATCH_SIZE,
        )
        self.slow_query_threshold_ms: int = self._validate_int(
            inst,
            'slow_query_threshold_ms',
            default=5000,
            lo=MIN_SLOW_QUERY_MS,
            hi=MAX_SLOW_QUERY_MS,
        )
        self.initial_backfill_minutes: int = self._validate_int(
            inst,
            'initial_backfill_minutes',
            default=60,
            lo=MIN_BACKFILL_MINUTES,
            hi=MAX_BACKFILL_MINUTES,
        )
        self.query_timeout_seconds: int = self._validate_int(
            inst,
            'query_timeout_seconds',
            default=30,
            lo=MIN_TIMEOUT_SECONDS,
            hi=MAX_TIMEOUT_SECONDS,
        )

        self.custom_tags: list[str] = inst.get('tags', [])

        # Cluster name → used as the Datadog "service" field on every log.
        # Defaults to "clickhouse" so logs are attributed even without config.
        self.cluster_name: str = inst.get('cluster_name', 'clickhouse')

        # HTTP session with automatic retries on transient failures
        self.base_url: str = f"https://queries.clickhouse.cloud/service/{self.service_id}/run"

        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[502, 503, 504],
            allowed_methods=['POST'],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)

        self._session = requests.Session()
        self._session.auth = (self.key_id, self.key_secret)
        self._session.headers.update({'Content-Type': 'application/json'})
        self._session.verify = True
        self._session.mount('https://', adapter)

    # ------------------------------------------------------------------
    # Config validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_int(inst: dict[str, Any], key: str, *, default: int, lo: int, hi: int) -> int:
        """Parse and clamp an integer config value within [lo, hi]."""
        raw = inst.get(key, default)
        try:
            value = int(raw)
        except (TypeError, ValueError):
            raise ValueError(f"{key} must be an integer, got {raw!r}") from None
        if value < lo or value > hi:
            raise ValueError(f"{key} must be between {lo} and {hi}, got {value}")
        return value

    # ------------------------------------------------------------------
    # Cursor management
    # ------------------------------------------------------------------

    def _get_cursor(self, key: str) -> int | None:
        """Retrieve the stored cursor (event_time_microseconds) from persistent cache."""
        cached = self.read_persistent_cache(key)
        if cached:
            return int(cached)
        return None

    def _set_cursor(self, key: str, value: int) -> None:
        """Persist the latest cursor value."""
        self.write_persistent_cache(key, str(value))

    def _default_cursor(self) -> int:
        """Return a microsecond timestamp for initial_backfill_minutes ago."""
        backfill_seconds = self.initial_backfill_minutes * 60
        # ClickHouse event_time_microseconds is a DateTime64(6) stored as UInt64 microseconds
        epoch_us = int((time.time() - backfill_seconds) * 1_000_000)
        return epoch_us

    def _timestamp_seconds(self, row: dict[str, Any]) -> float:
        """Return a Unix timestamp in seconds for Datadog's send_log API."""
        try:
            return int(row.get('cursor_us', 0)) / 1_000_000
        except (TypeError, ValueError):
            self.log.warning(
                "Could not parse cursor_us=%r from row, falling back to current time",
                row.get('cursor_us'),
            )
            return time.time()

    def _extract_cursor(self, rows: list[dict[str, Any]], source: str) -> int | None:
        """Safely extract the cursor value from the last row in a batch.

        Returns None (and logs a warning) when the field is missing or
        unparsable, so the caller can decide whether to update the stored
        cursor.
        """
        raw = rows[-1].get('cursor_us') if rows else None
        if raw is None:
            self.log.warning(
                "%s: last row missing cursor_us field, cursor will not advance",
                source,
            )
            return None
        try:
            return int(raw)
        except (TypeError, ValueError):
            self.log.warning(
                "%s: could not parse cursor_us=%r as integer, cursor will not advance",
                source,
                raw,
            )
            return None

    def _emit_log(self, log_entry: dict[str, Any]) -> None:
        """Send log entry using Agent APIs available in the current runtime.

        Newer Datadog Agent runtimes expose AgentCheck.send_log(). Older runtimes
        do not; in that case we write JSON to the check logger as a fallback so
        the check keeps running without raising AttributeError.
        """
        send_log = getattr(self, 'send_log', None)
        if callable(send_log):
            send_log(log_entry)
            return

        self.log.info(json.dumps(log_entry, separators=(',', ':')))

    # ------------------------------------------------------------------
    # ClickHouse HTTP interface
    # ------------------------------------------------------------------

    def _query_clickhouse(self, sql: str) -> list[dict[str, Any]]:
        """Execute a SQL query against ClickHouse Cloud via the Cloud Query API.

        Returns a list of dicts (one per row) using JSONEachRow format.
        The session is configured with automatic retries on 502/503/504.
        """
        params = {'format': 'JSONEachRow'}
        body = {'sql': sql}

        try:
            resp = self._session.post(
                self.base_url,
                params=params,
                json=body,
                timeout=self.query_timeout_seconds,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error("ClickHouse Cloud API query failed: %s", e)
            raise

        rows: list[dict[str, Any]] = []
        for line in resp.text.strip().splitlines():
            if line:
                rows.append(json.loads(line))
        return rows

    # ------------------------------------------------------------------
    # Unified log collection
    # ------------------------------------------------------------------

    def _collect_logs(
        self,
        sql_template: str,
        cursor_key: str,
        check_name: str,
        gauge_name: str,
        build_payload: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        """Fetch new rows from a ClickHouse system table and ship as Datadog logs.

        This is the shared pipeline used by both query-log and text-log collection.
        Duplicate delivery is preferred over log loss — if *_emit_log* fails for a
        single row the loop continues, and the cursor still advances to avoid
        re-fetching the entire batch on the next run.
        """
        cursor = self._get_cursor(cursor_key)
        if cursor is None:
            cursor = self._default_cursor()

        sql = sql_template.format(last_cursor=cursor, batch_size=self.batch_size)

        try:
            rows = self._query_clickhouse(sql)
        except Exception:
            self.service_check(check_name, AgentCheck.CRITICAL)
            return

        self.service_check(check_name, AgentCheck.OK)
        self.gauge(gauge_name, len(rows))
        self.log.debug("%s: fetched %d rows", cursor_key, len(rows))

        if not rows:
            return

        for row in rows:
            try:
                log_entry = build_payload(row)
                self._emit_log(log_entry)
            except Exception:
                self.log.exception(
                    "%s: failed to emit log for row cursor_us=%s",
                    cursor_key,
                    row.get('cursor_us', '?'),
                )

        # Advance the cursor so the next run picks up where we left off.
        # If the cursor field is missing/corrupt we intentionally do NOT
        # advance — the worst case is duplicate delivery on the next run,
        # which is acceptable (better than losing logs).
        new_cursor = self._extract_cursor(rows, cursor_key)
        if new_cursor is not None:
            self._set_cursor(cursor_key, new_cursor)

    # ------------------------------------------------------------------
    # Query log collection
    # ------------------------------------------------------------------

    def _collect_query_logs(self) -> None:
        """Fetch new rows from system.query_log and send as Datadog logs."""
        user_filter = INTERNAL_USER_FILTER if self.exclude_internal_users else ""
        sql = QUERY_LOG_SQL.replace("{internal_user_filter}", user_filter)
        self._collect_logs(
            sql_template=sql,
            cursor_key=CURSOR_QUERY_LOG,
            check_name=SC_QUERY_LOG_CONNECT,
            gauge_name=GAUGE_QUERY_LOG_ROWS,
            build_payload=self._build_query_log_payload,
        )

    def _build_query_log_payload(self, row: dict[str, Any]) -> dict[str, Any]:
        """Map a query_log row to a Datadog log entry."""
        query_type = row.get('type', '')

        # Determine log level
        if query_type in (TYPE_QUERY_EXCEPTION, TYPE_QUERY_EXCEPTION_BEFORE_START):
            level = 'error'
            type_label = 'exception'
        else:
            duration_ms = int(row.get('query_duration_ms', 0))
            level = 'warning' if duration_ms >= self.slow_query_threshold_ms else 'info'
            type_label = 'finish'

        return {
            'timestamp': self._timestamp_seconds(row),
            'message': row.get('query', ''),
            'ddsource': 'clickhouse',
            'ddtags': ','.join(self.custom_tags) if self.custom_tags else '',
            'service': self.cluster_name,
            'status': level,
            'clickhouse.query_id': row.get('query_id', ''),
            'clickhouse.user': row.get('user', ''),
            'clickhouse.duration_ms': int(row.get('query_duration_ms', 0)),
            'clickhouse.memory_bytes': int(row.get('memory_usage', 0)),
            'clickhouse.read_rows': int(row.get('read_rows', 0)),
            'clickhouse.read_bytes': int(row.get('read_bytes', 0)),
            'clickhouse.result_rows': int(row.get('result_rows', 0)),
            'clickhouse.written_rows': int(row.get('written_rows', 0)),
            'clickhouse.written_bytes': int(row.get('written_bytes', 0)),
            'clickhouse.exception': row.get('exception', ''),
            'clickhouse.exception_code': int(row.get('exception_code', 0)),
            'clickhouse.query_type': type_label,
            'clickhouse.query_kind': row.get('query_kind', ''),
            'clickhouse.database': row.get('current_database', ''),
            'clickhouse.tables': row.get('tables', ''),
            'clickhouse.client': row.get('client_name', ''),
        }

    # ------------------------------------------------------------------
    # Text log collection
    # ------------------------------------------------------------------

    def _collect_text_logs(self) -> None:
        """Fetch new rows from system.text_log and send as Datadog logs."""
        self._collect_logs(
            sql_template=TEXT_LOG_SQL,
            cursor_key=CURSOR_TEXT_LOG,
            check_name=SC_TEXT_LOG_CONNECT,
            gauge_name=GAUGE_TEXT_LOG_ROWS,
            build_payload=self._build_text_log_payload,
        )

    def _build_text_log_payload(self, row: dict[str, Any]) -> dict[str, Any]:
        """Map a text_log row to a Datadog log entry."""
        level = TEXT_LOG_LEVEL_MAP.get(row.get('level', ''), 'warning')

        return {
            'timestamp': self._timestamp_seconds(row),
            'message': row.get('message', ''),
            'ddsource': 'clickhouse',
            'ddtags': ','.join(self.custom_tags) if self.custom_tags else '',
            'service': self.cluster_name,
            'status': level,
            'clickhouse.logger': row.get('logger_name', ''),
            'clickhouse.thread_id': str(row.get('thread_id', '')),
            'clickhouse.query_id': row.get('query_id', ''),
        }

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def check(self, instance: dict[str, Any]) -> None:
        """Main check method called by the Datadog Agent on each run."""
        if self.collect_query_logs:
            self._collect_query_logs()

        if self.collect_text_logs:
            self._collect_text_logs()
