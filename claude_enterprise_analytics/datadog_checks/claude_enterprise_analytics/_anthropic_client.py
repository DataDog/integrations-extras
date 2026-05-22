# (C) Typeform Platform 2026-present
# Unofficial integration. Not affiliated with Anthropic, PBC.
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Thin client for the Anthropic Claude Enterprise Analytics API.

Docs: https://support.claude.com/en/articles/13703965
Base: https://api.anthropic.com/v1/organizations/analytics

Endpoint quirks (verified empirically 2026-05-21):
- `/summaries`            takes `starting_date` / `ending_date` (calendar dates,
                          strict-before). Response: {"summaries": [...]}.
- `/users`                takes `date` (single day). Response:
                          {"data": [...], "next_page": "..."}.
- `/usage_report`,        take `starting_at` / `ending_at` (RFC3339 timestamps).
  `/cost_report`,         Response: {"data": [{"results": [...]}], "has_more", "next_page"}.
- `/user_usage_report`,   take `starting_at` / `ending_at`. Response: flat
  `/user_cost_report`     {"data": [...rows w/ actor], "has_more", "next_page"}.

Pagination cursor token comes back as `next_page` and is sent as `?page=<token>`.
Uses the AgentCheck's `self.http` (a `requests`-compatible session) for transport
so it inherits proxy/TLS/auth configuration from the Datadog Agent.
"""

from datetime import datetime, timedelta, timezone
from datetime import time as dtime

ANTHROPIC_API_BASE = "https://api.anthropic.com/v1/organizations/analytics"

_RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
_MAX_RETRIES = 5
_BASE_BACKOFF_SECONDS = 1.0
_PAGE_SIZE = 1000


class AnthropicAnalyticsClient(object):
    """Synchronous client used inside the Agent check.

    The check passes in `self.http` (the AgentCheck-managed `requests.Session`)
    so we get its retries-around-this-layer behavior + DD Agent proxy support
    for free.
    """

    def __init__(self, http, api_key, log, timeout=30.0):
        self._http = http
        self._api_key = api_key
        self._log = log
        self._timeout = timeout

    def _headers(self):
        return {"x-api-key": self._api_key, "accept": "application/json"}

    def _get(self, path, params):
        # `self.http` already wraps connection retries; we add an extra layer
        # here only for 429/5xx with backoff, since those are application-level.
        import time as _time

        url = "{}{}".format(ANTHROPIC_API_BASE, path)
        last_resp = None
        for attempt in range(1, _MAX_RETRIES + 1):
            resp = self._http.get(url, params=params, headers=self._headers(), timeout=self._timeout)
            last_resp = resp
            if resp.status_code in _RETRYABLE_STATUSES:
                retry_after = resp.headers.get("retry-after")
                wait = (
                    float(retry_after)
                    if retry_after and retry_after.replace(".", "", 1).isdigit()
                    else _BASE_BACKOFF_SECONDS * (2 ** (attempt - 1))
                )
                self._log.warning(
                    "Anthropic %s -> %d (attempt %d/%d), sleeping %.1fs",
                    path,
                    resp.status_code,
                    attempt,
                    _MAX_RETRIES,
                    wait,
                )
                _time.sleep(wait)
                continue
            if resp.status_code >= 400:
                self._log.error("Anthropic %s -> %d: %s", path, resp.status_code, resp.text[:500])
            resp.raise_for_status()
            return resp.json()
        last_resp.raise_for_status()
        return last_resp.json()

    def _paginate_rows(self, path, params, rows_key="data"):
        page_params = dict(params)
        page_params["limit"] = _PAGE_SIZE
        while True:
            payload = self._get(path, page_params)
            for row in payload.get(rows_key) or []:
                yield row
            token = payload.get("next_page")
            has_more = payload.get("has_more")
            if not token or has_more is False:
                return
            page_params = dict(params)
            page_params["limit"] = _PAGE_SIZE
            page_params["page"] = token

    @staticmethod
    def _iso_date(d):
        return d.isoformat()

    @staticmethod
    def _iso_ts(d):
        return datetime.combine(d, dtime.min, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _next_day(d):
        return d + timedelta(days=1)

    # --- endpoint wrappers ---

    def summaries(self, day):
        payload = self._get(
            "/summaries",
            {
                "starting_date": self._iso_date(day),
                "ending_date": self._iso_date(self._next_day(day)),
            },
        )
        rows = payload.get("summaries") or []
        return rows[0] if rows else None

    def users(self, day):
        for row in self._paginate_rows("/users", {"date": self._iso_date(day)}):
            yield row

    def usage_report(self, day, group_by=None):
        for row in self._iter_report("/usage_report", day, group_by or ["model", "product"]):
            yield row

    def cost_report(self, day, group_by=None):
        for row in self._iter_report("/cost_report", day, group_by or ["model", "product"]):
            yield row

    def user_usage_report(self, day):
        params = {
            "starting_at": self._iso_ts(day),
            "ending_at": self._iso_ts(self._next_day(day)),
        }
        for row in self._paginate_rows("/user_usage_report", params):
            yield row

    def user_cost_report(self, day):
        params = {
            "starting_at": self._iso_ts(day),
            "ending_at": self._iso_ts(self._next_day(day)),
        }
        for row in self._paginate_rows("/user_cost_report", params):
            yield row

    def _iter_report(self, path, day, group_by):
        # /usage_report and /cost_report wrap rows under data[].results[].
        params = {
            "starting_at": self._iso_ts(day),
            "ending_at": self._iso_ts(self._next_day(day)),
        }
        gb = []
        for key in group_by:
            gb.append(key)
        if gb:
            params["group_by[]"] = gb

        page_params = dict(params)
        while True:
            payload = self._get(path, page_params)
            for outer in payload.get("data") or []:
                for row in outer.get("results") or []:
                    yield row
            token = payload.get("next_page")
            has_more = payload.get("has_more")
            if not token or has_more is False:
                return
            page_params = dict(params)
            page_params["page"] = token
