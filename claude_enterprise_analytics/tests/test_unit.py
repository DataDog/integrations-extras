# (C) Typeform Platform 2026-present
# Unofficial integration. Not affiliated with Anthropic, PBC.
# Licensed under a 3-clause BSD style license (see LICENSE)

from datetime import date
from typing import Any, Callable, Dict  # noqa: F401
from unittest import mock

import pytest

from datadog_checks.base import AgentCheck, ConfigurationError  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401

from datadog_checks.claude_enterprise_analytics import ClaudeEnterpriseAnalyticsCheck
from datadog_checks.claude_enterprise_analytics import _mappers as mappers


# ---------- mapper unit tests (pure functions, no I/O) ---------------------

def test_cents_to_usd_divides_by_100():
    assert mappers._cents_to_usd("131309.570280") == pytest.approx(1313.0957028)
    assert mappers._cents_to_usd(None) == 0.0
    assert mappers._cents_to_usd("") == 0.0


def test_summaries_emits_expected_metrics():
    row = {
        "daily_active_user_count": 95,
        "weekly_active_user_count": 135,
        "monthly_active_user_count": 143,
        "assigned_seat_count": 150,
        "pending_invite_count": 0,
        "daily_adoption_rate": 63.33,
        "weekly_adoption_rate": 90.0,
        "monthly_adoption_rate": 95.33,
    }
    out = list(mappers.from_summaries(row, date(2026, 5, 18)))
    names = {m for m, _, _ in out}
    assert "org.dau" in names
    assert "org.seats_assigned" in names
    assert "org.adoption_rate.daily" in names
    # report_date tag is on every entry
    for _, _, tags in out:
        assert "report_date:2026-05-18" in tags


def test_cost_report_divides_amount_by_100():
    rows = [
        {
            "model": "claude-opus-4-7",
            "product": "claude_code",
            "currency": "USD",
            "amount": "8164942.9775",
            "list_amount": "8164942.9775",
        }
    ]
    out = list(mappers.from_cost_report(rows, date(2026, 5, 18)))
    by_name = {name: value for name, value, _ in out}
    assert by_name["cost.amount_usd"] == pytest.approx(81649.429775)
    assert by_name["cost.list_amount_usd"] == pytest.approx(81649.429775)


# ---------- check-level integration test (mocked HTTP) ---------------------

def _empty_payload(rows_key="data"):
    return {rows_key: [], "next_page": None, "has_more": False}


def test_check_emits_metrics_and_service_check(dd_run_check, aggregator, instance):
    """End-to-end with AnthropicAnalyticsClient stubbed so no HTTP is made.

    Asserts the check reaches the `can_connect: OK` service check and emits at
    least the summary gauges with the expected `report_date` tag.
    """
    check = ClaudeEnterpriseAnalyticsCheck("claude_enterprise_analytics", {}, [instance])

    stub_client = mock.MagicMock()
    stub_client.summaries.return_value = {
        "daily_active_user_count": 95,
        "weekly_active_user_count": 135,
        "monthly_active_user_count": 143,
        "assigned_seat_count": 150,
        "pending_invite_count": 0,
        "daily_adoption_rate": 63.33,
        "weekly_adoption_rate": 90.0,
        "monthly_adoption_rate": 95.33,
    }
    # All other endpoints return empty iterators
    for name in ("users", "usage_report", "cost_report", "user_usage_report", "user_cost_report"):
        getattr(stub_client, name).return_value = iter([])

    with mock.patch(
        "datadog_checks.claude_enterprise_analytics.check.AnthropicAnalyticsClient",
        return_value=stub_client,
    ):
        dd_run_check(check)

    aggregator.assert_metric("claude_enterprise_analytics.org.dau", value=95)
    aggregator.assert_metric("claude_enterprise_analytics.org.seats_assigned", value=150)
    aggregator.assert_service_check(
        "claude_enterprise_analytics.can_connect", status=AgentCheck.OK
    )


def test_check_requires_api_key():
    with pytest.raises(ConfigurationError):
        ClaudeEnterpriseAnalyticsCheck("claude_enterprise_analytics", {}, [{}])
