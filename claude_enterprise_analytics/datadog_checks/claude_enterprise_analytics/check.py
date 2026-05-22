# (C) Typeform Platform 2026-present
# Unofficial integration. Not affiliated with Anthropic, PBC.
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Datadog Agent Check for the Anthropic Claude Enterprise Analytics API.

Polls the six in-scope endpoints (summaries, users, usage_report, cost_report,
user_usage_report, user_cost_report) for a single report-date (default: today
minus the configured lag, which Anthropic itself sets at 3 days), maps each
row to gauges, and submits via `self.gauge()`.

Architectural note: Anthropic exposes only daily aggregates with a 3-day lag.
Every metric is submitted at agent wall-clock time and tagged with
`report_date:YYYY-MM-DD` representing the activity day. Dashboards must filter
on the `report_date` tag rather than rely on Datadog's wall-clock x-axis.
"""

from datetime import date, timedelta
from typing import Any  # noqa: F401

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.claude_enterprise_analytics import _mappers as mappers
from datadog_checks.claude_enterprise_analytics._anthropic_client import (
    AnthropicAnalyticsClient,
)

_SERVICE_CHECK_API = "can_connect"
_DEFAULT_LAG_DAYS = 3


class ClaudeEnterpriseAnalyticsCheck(AgentCheck):
    __NAMESPACE__ = "claude_enterprise_analytics"

    def __init__(self, name, init_config, instances):
        super(ClaudeEnterpriseAnalyticsCheck, self).__init__(name, init_config, instances)

        self._api_key = self.instance.get("anthropic_api_key")
        self._org_id = self.instance.get("org_id", "unknown")
        self._lag_days = int(self.instance.get("lag_days", _DEFAULT_LAG_DAYS))

        if not self._api_key:
            raise ConfigurationError(
                "anthropic_api_key is required. Generate one at claude.ai/analytics/api-keys "
                "with the `read:analytics` scope."
            )

    def check(self, _instance):
        report_date = date.today() - timedelta(days=self._lag_days)
        common_tags = [
            "source:anthropic_analytics",
            "org_id:{}".format(self._org_id),
        ]

        client = AnthropicAnalyticsClient(self.http, self._api_key, self.log)

        try:
            # /summaries -- single row (or None if not yet available)
            summary_row = client.summaries(report_date)
            self._emit(mappers.from_summaries(summary_row, report_date), common_tags)

            # /users -- paginated
            self._emit(mappers.from_users(client.users(report_date), report_date), common_tags)

            # /usage_report, /cost_report -- grouped by model+product
            self._emit(
                mappers.from_usage_report(client.usage_report(report_date), report_date),
                common_tags,
            )
            self._emit(
                mappers.from_cost_report(client.cost_report(report_date), report_date),
                common_tags,
            )

            # /user_usage_report, /user_cost_report -- per-user
            self._emit(
                mappers.from_user_usage_report(client.user_usage_report(report_date), report_date),
                common_tags,
            )
            self._emit(
                mappers.from_user_cost_report(client.user_cost_report(report_date), report_date),
                common_tags,
            )
        except Exception as e:
            self.log.exception("Failed to collect Claude Enterprise Analytics for %s", report_date)
            self.service_check(
                _SERVICE_CHECK_API,
                AgentCheck.CRITICAL,
                tags=common_tags,
                message=str(e)[:200],
            )
            raise

        self.service_check(_SERVICE_CHECK_API, AgentCheck.OK, tags=common_tags)

    def _emit(self, triples, common_tags):
        instance_tags = list(self.instance.get("tags") or [])
        for name, value, extra_tags in triples:
            self.gauge(name, value, tags=common_tags + instance_tags + list(extra_tags))
