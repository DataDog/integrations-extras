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
from datadog_checks.claude_enterprise_analytics._anthropic_client import AnthropicAnalyticsClient

REPORT_DATE = date(2026, 5, 18)


# ---------- mapper helper unit tests ---------------------------------------


def test_num_handles_string_none_and_invalid():
    assert mappers._num("1.5") == 1.5
    assert mappers._num(2) == 2.0
    assert mappers._num(None) == 0.0
    assert mappers._num("") == 0.0
    assert mappers._num("not-a-number") == 0.0


def test_cents_to_usd_divides_by_100():
    assert mappers._cents_to_usd("131309.570280") == pytest.approx(1313.0957028)
    assert mappers._cents_to_usd(None) == 0.0
    assert mappers._cents_to_usd("") == 0.0


def test_g_walks_nested_dicts_with_default():
    obj = {"a": {"b": {"c": 42}}}
    assert mappers._g(obj, "a", "b", "c") == 42
    assert mappers._g(obj, "a", "missing", default="x") == "x"
    assert mappers._g(None, "a") == 0
    assert mappers._g({"a": None}, "a", "b", default=7) == 7


def test_tag_normalizes_missing_values():
    assert mappers._tag("model", "claude-opus") == "model:claude-opus"
    assert mappers._tag("model", None) == "model:unknown"
    assert mappers._tag("model", "") == "model:unknown"


# ---------- mapper function tests ------------------------------------------


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
    out = list(mappers.from_summaries(row, REPORT_DATE))
    names = {m for m, _, _ in out}
    assert "org.dau" in names
    assert "org.seats_assigned" in names
    assert "org.adoption_rate.daily" in names
    for _, _, tags in out:
        assert "report_date:2026-05-18" in tags


def test_summaries_with_none_row_emits_nothing():
    assert list(mappers.from_summaries(None, REPORT_DATE)) == []


def test_users_emits_chat_claude_code_and_tool_action_metrics():
    rows = [
        {
            "user": {"email_address": "alice@example.com"},
            "chat_metrics": {
                "message_count": 12,
                "distinct_conversation_count": 3,
                "thinking_message_count": 1,
                "distinct_projects_used_count": 2,
                "distinct_projects_created_count": 1,
                "distinct_artifacts_created_count": 4,
                "distinct_skills_used_count": 0,
                "connectors_used_count": 0,
                "distinct_files_uploaded_count": 5,
            },
            "claude_code_metrics": {
                "core_metrics": {
                    "distinct_session_count": 22,
                    "commit_count": 3,
                    "pull_request_count": 1,
                    "lines_of_code": {"added_count": 1757, "removed_count": 669},
                },
                "tool_actions": {
                    "edit_tool": {"accepted_count": 90, "rejected_count": 2},
                    "write_tool": {"accepted_count": 11, "rejected_count": 0},
                    "broken": "ignored",
                },
            },
            "web_search_count": 7,
        }
    ]
    out = list(mappers.from_users(rows, REPORT_DATE))
    by_name_tags = {(m, tuple(sorted(t))): v for m, v, t in out}

    # Chat surface
    assert any(m == "user.chat.messages" and v == 12 for m, v, _ in out)
    assert any(m == "user.artifacts.created" and v == 4 for m, v, _ in out)
    assert any(m == "user.files.uploaded" and v == 5 for m, v, _ in out)

    # Claude Code core
    assert any(m == "user.claude_code.sessions" and v == 22 for m, v, _ in out)
    assert any(m == "user.claude_code.commits" and v == 3 for m, v, _ in out)
    assert any(m == "user.claude_code.lines_added" and v == 1757 for m, v, _ in out)
    assert any(m == "user.claude_code.lines_removed" and v == 669 for m, v, _ in out)

    # Tool actions are tagged by tool + outcome; `broken` (non-dict) is skipped.
    tool_metrics = [(m, v, t) for m, v, t in out if m == "user.claude_code.tool_actions"]
    assert len(tool_metrics) == 4  # 2 tools x 2 outcomes
    assert (
        "user.claude_code.tool_actions",
        90.0,
        ["report_date:2026-05-18", "user_email:alice@example.com", "tool:edit", "outcome:accepted"],
    ) in [(m, v, t) for m, v, t in tool_metrics]

    # Web search
    assert any(m == "user.web_search_count" and v == 7 for m, v, _ in out)

    # Every row carries user_email tag
    for _, _, tags in out:
        assert "user_email:alice@example.com" in tags

    # silence unused-var warning
    _ = by_name_tags


def test_users_handles_missing_optional_subdocs():
    rows = [{"user": {"email_address": "bob@example.com"}}]
    out = list(mappers.from_users(rows, REPORT_DATE))
    # Should still emit zero-valued metrics, not crash.
    assert any(m == "user.chat.messages" and v == 0 for m, v, _ in out)
    # No tool_actions yielded since the dict is missing.
    assert not any(m == "user.claude_code.tool_actions" for m, _, _ in out)


def test_usage_report_emits_seven_metrics_per_row():
    rows = [
        {
            "model": "claude-opus-4-7",
            "product": "claude_code",
            "context_window": None,
            "uncached_input_tokens": 10243631,
            "output_tokens": 7705210,
            "cache_read_input_tokens": 1746957745,
            "cache_creation": {
                "ephemeral_1h_input_tokens": 52015263,
                "ephemeral_5m_input_tokens": 21611713,
            },
            "server_tool_use": {"web_search_requests": 19},
            "requests": 21833,
        }
    ]
    out = list(mappers.from_usage_report(rows, REPORT_DATE))
    by_name = {m: v for m, v, _ in out}
    assert by_name["tokens.uncached_input"] == 10243631
    assert by_name["tokens.output"] == 7705210
    assert by_name["tokens.cache_read"] == 1746957745
    assert by_name["tokens.cache_write_1h"] == 52015263
    assert by_name["tokens.cache_write_5m"] == 21611713
    assert by_name["requests"] == 21833
    assert by_name["web_search_requests"] == 19
    # Tags include model + product + context_window
    for _, _, tags in out:
        assert "model:claude-opus-4-7" in tags
        assert "product:claude_code" in tags
        assert "context_window:unknown" in tags  # None -> 'unknown'


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
    out = list(mappers.from_cost_report(rows, REPORT_DATE))
    by_name = {name: value for name, value, _ in out}
    assert by_name["cost.amount_usd"] == pytest.approx(81649.429775)
    assert by_name["cost.list_amount_usd"] == pytest.approx(81649.429775)


def test_user_usage_report_emits_all_per_user_token_metrics():
    rows = [
        {
            "actor": {"email": "alice@example.com"},
            "total_tokens": 271849312,
            "uncached_input_tokens": 146848,
            "output_tokens": 447409,
            "cache_read_input_tokens": 268750070,
            "cache_creation": {
                "ephemeral_1h_input_tokens": 2192245,
                "ephemeral_5m_input_tokens": 312740,
            },
            "requests": 853,
        }
    ]
    out = list(mappers.from_user_usage_report(rows, REPORT_DATE))
    by_name = {m: v for m, v, _ in out}
    assert by_name["user.tokens_total"] == 271849312
    assert by_name["user.uncached_input_tokens"] == 146848
    assert by_name["user.output_tokens"] == 447409
    assert by_name["user.cache_read_tokens"] == 268750070
    assert by_name["user.cache_write_1h_tokens"] == 2192245
    assert by_name["user.cache_write_5m_tokens"] == 312740
    assert by_name["user.requests"] == 853
    # 7 metrics per user
    assert len(out) == 7


def test_user_cost_report_divides_per_user_amount_by_100():
    rows = [
        {
            "actor": {"email": "alice@example.com"},
            "currency": "USD",
            "amount": "1683895.6900",
            "list_amount": "1683895.6900",
        }
    ]
    out = list(mappers.from_user_cost_report(rows, REPORT_DATE))
    by_name = {m: v for m, v, _ in out}
    assert by_name["user.cost.amount_usd"] == pytest.approx(16838.956900)
    assert by_name["user.cost.list_amount_usd"] == pytest.approx(16838.956900)


# ---------- Anthropic client tests -----------------------------------------


def _mock_response(json_payload, status_code=200, headers=None):
    resp = mock.MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_payload
    resp.headers = headers or {}
    resp.text = ""
    resp.raise_for_status = mock.MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = Exception("HTTP {}".format(status_code))
    return resp


def test_client_summaries_calls_correct_url_and_returns_first_row():
    http = mock.MagicMock()
    http.get.return_value = _mock_response({"summaries": [{"daily_active_user_count": 95}]})
    client = AnthropicAnalyticsClient(http, "secret-key", mock.MagicMock())

    row = client.summaries(REPORT_DATE)

    assert row == {"daily_active_user_count": 95}
    call = http.get.call_args
    assert call.args[0].endswith("/summaries")
    # strict-before range: [day, day+1)
    assert call.kwargs["params"]["starting_date"] == "2026-05-18"
    assert call.kwargs["params"]["ending_date"] == "2026-05-19"
    assert call.kwargs["headers"]["x-api-key"] == "secret-key"


def test_client_summaries_returns_none_when_empty():
    http = mock.MagicMock()
    http.get.return_value = _mock_response({"summaries": []})
    client = AnthropicAnalyticsClient(http, "k", mock.MagicMock())
    assert client.summaries(REPORT_DATE) is None


def test_client_paginates_via_next_page_token():
    http = mock.MagicMock()
    http.get.side_effect = [
        _mock_response({"data": [{"id": 1}, {"id": 2}], "next_page": "page_abc", "has_more": True}),
        _mock_response({"data": [{"id": 3}], "next_page": None, "has_more": False}),
    ]
    client = AnthropicAnalyticsClient(http, "k", mock.MagicMock())

    rows = list(client.users(REPORT_DATE))

    assert [r["id"] for r in rows] == [1, 2, 3]
    assert http.get.call_count == 2
    second_call_params = http.get.call_args_list[1].kwargs["params"]
    assert second_call_params["page"] == "page_abc"


def test_client_iter_report_groups_by_model_and_product():
    http = mock.MagicMock()
    http.get.return_value = _mock_response(
        {"data": [{"results": [{"model": "claude-opus-4-7", "amount": "100"}]}], "has_more": False, "next_page": None}
    )
    client = AnthropicAnalyticsClient(http, "k", mock.MagicMock())

    rows = list(client.cost_report(REPORT_DATE))

    assert rows == [{"model": "claude-opus-4-7", "amount": "100"}]
    params = http.get.call_args.kwargs["params"]
    assert params["group_by[]"] == ["model", "product"]
    assert params["starting_at"] == "2026-05-18T00:00:00Z"
    assert params["ending_at"] == "2026-05-19T00:00:00Z"


def test_client_retries_on_429_then_succeeds():
    http = mock.MagicMock()
    http.get.side_effect = [
        _mock_response({}, status_code=429, headers={"retry-after": "0"}),
        _mock_response({"summaries": [{"daily_active_user_count": 1}]}),
    ]
    client = AnthropicAnalyticsClient(http, "k", mock.MagicMock())

    with mock.patch("time.sleep") as msleep:
        row = client.summaries(REPORT_DATE)

    assert row == {"daily_active_user_count": 1}
    assert http.get.call_count == 2
    assert msleep.called


# ---------- check-level integration tests ----------------------------------


def _empty_payload(rows_key="data"):
    return {rows_key: [], "next_page": None, "has_more": False}


def test_check_emits_metrics_and_service_check(dd_run_check, aggregator, instance):
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
    for name in ("users", "usage_report", "cost_report", "user_usage_report", "user_cost_report"):
        getattr(stub_client, name).return_value = iter([])

    with mock.patch(
        "datadog_checks.claude_enterprise_analytics.check.AnthropicAnalyticsClient",
        return_value=stub_client,
    ):
        dd_run_check(check)

    aggregator.assert_metric("claude_enterprise_analytics.org.dau", value=95)
    aggregator.assert_metric("claude_enterprise_analytics.org.seats_assigned", value=150)
    aggregator.assert_service_check("claude_enterprise_analytics.can_connect", status=AgentCheck.OK)


def test_check_emits_critical_service_check_on_api_error(aggregator, instance):
    """When the client raises, the check should submit a CRITICAL service check
    and re-raise so the Agent surfaces the failure."""
    check = ClaudeEnterpriseAnalyticsCheck("claude_enterprise_analytics", {}, [instance])

    stub_client = mock.MagicMock()
    stub_client.summaries.side_effect = RuntimeError("upstream 500")

    with mock.patch(
        "datadog_checks.claude_enterprise_analytics.check.AnthropicAnalyticsClient",
        return_value=stub_client,
    ):
        with pytest.raises(RuntimeError):
            check.check({})

    aggregator.assert_service_check("claude_enterprise_analytics.can_connect", status=AgentCheck.CRITICAL)


def test_check_merges_instance_tags_into_emitted_metrics(dd_run_check, aggregator):
    """Custom `tags:` set on the instance must appear alongside the report_date
    and source tags on every gauge. Uses `team`/`region` because ddev reserves
    generic keys like `env`/`host`/`service`."""
    instance = {
        "anthropic_api_key": "k",
        "org_id": "test-org",
        "lag_days": 3,
        "tags": ["team:platform", "region:eu-west-1"],
    }
    check = ClaudeEnterpriseAnalyticsCheck("claude_enterprise_analytics", {}, [instance])

    stub_client = mock.MagicMock()
    stub_client.summaries.return_value = {"daily_active_user_count": 1}
    for name in ("users", "usage_report", "cost_report", "user_usage_report", "user_cost_report"):
        getattr(stub_client, name).return_value = iter([])

    with mock.patch(
        "datadog_checks.claude_enterprise_analytics.check.AnthropicAnalyticsClient",
        return_value=stub_client,
    ):
        dd_run_check(check)

    aggregator.assert_metric_has_tag("claude_enterprise_analytics.org.dau", "team:platform")
    aggregator.assert_metric_has_tag("claude_enterprise_analytics.org.dau", "region:eu-west-1")
    aggregator.assert_metric_has_tag("claude_enterprise_analytics.org.dau", "org_id:test-org")


def test_check_requires_api_key():
    with pytest.raises(ConfigurationError):
        ClaudeEnterpriseAnalyticsCheck("claude_enterprise_analytics", {}, [{}])
