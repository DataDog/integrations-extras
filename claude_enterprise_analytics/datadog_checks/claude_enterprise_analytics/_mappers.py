# (C) Typeform Platform 2026-present
# Unofficial integration. Not affiliated with Anthropic, PBC.
# Licensed under a 3-clause BSD style license (see LICENSE)
"""Anthropic Analytics rows -> Datadog gauge submissions.

Each mapper is a generator that yields `(metric_name, value, extra_tags_list)`
tuples. The Check iterates over these and calls `self.gauge(name, value,
tags=tags)`.

Field paths verified empirically against the live API on 2026-05-21.

Key API quirk: cost amounts come back as STRINGS in USD cents
("131309.570280" → $1,313.10), so we divide by 100 via _cents_to_usd().
"""


# --- helpers ---------------------------------------------------------------

def _num(value):
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _cents_to_usd(value):
    """Cost-report `amount`/`list_amount` are returned in USD cents despite
    the `currency: USD` field. Verified by cross-checking the org-level web
    spend dashboard on 2026-05-21."""
    return _num(value) / 100.0


def _g(obj, *path, **kwargs):
    default = kwargs.get("default", 0)
    cur = obj
    for key in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
        if cur is None:
            return default
    return cur


def _tag(key, value):
    if value is None or value == "":
        return "{}:unknown".format(key)
    return "{}:{}".format(key, value)


def _rd_tag(report_date):
    return "report_date:{}".format(report_date.isoformat())


# --- /summaries -----------------------------------------------------------

def from_summaries(row, report_date):
    if not row:
        return
    rd = _rd_tag(report_date)
    yield ("org.dau", _num(row.get("daily_active_user_count")), [rd])
    yield ("org.wau", _num(row.get("weekly_active_user_count")), [rd])
    yield ("org.mau", _num(row.get("monthly_active_user_count")), [rd])
    yield ("org.seats_assigned", _num(row.get("assigned_seat_count")), [rd])
    yield ("org.invites_pending", _num(row.get("pending_invite_count")), [rd])
    yield ("org.adoption_rate.daily", _num(row.get("daily_adoption_rate")), [rd])
    yield ("org.adoption_rate.weekly", _num(row.get("weekly_adoption_rate")), [rd])
    yield ("org.adoption_rate.monthly", _num(row.get("monthly_adoption_rate")), [rd])
    yield ("org.cowork.dau", _num(row.get("cowork_daily_active_user_count")), [rd])
    yield ("org.cowork.wau", _num(row.get("cowork_weekly_active_user_count")), [rd])
    yield ("org.cowork.mau", _num(row.get("cowork_monthly_active_user_count")), [rd])


# --- /users ---------------------------------------------------------------

def from_users(rows, report_date):
    rd = _rd_tag(report_date)
    for row in rows:
        email = _g(row, "user", "email_address", default="unknown")
        utags = [rd, _tag("user_email", email)]
        yield ("user.chat.messages", _g(row, "chat_metrics", "message_count"), utags)
        yield ("user.chat.conversations", _g(row, "chat_metrics", "distinct_conversation_count"), utags)
        yield ("user.chat.thinking_messages", _g(row, "chat_metrics", "thinking_message_count"), utags)
        yield ("user.projects.used", _g(row, "chat_metrics", "distinct_projects_used_count"), utags)
        yield ("user.projects.created", _g(row, "chat_metrics", "distinct_projects_created_count"), utags)
        yield ("user.artifacts.created", _g(row, "chat_metrics", "distinct_artifacts_created_count"), utags)
        yield ("user.skills.used", _g(row, "chat_metrics", "distinct_skills_used_count"), utags)
        yield ("user.connectors.used", _g(row, "chat_metrics", "connectors_used_count"), utags)
        yield ("user.files.uploaded", _g(row, "chat_metrics", "distinct_files_uploaded_count"), utags)

        cc_core = _g(row, "claude_code_metrics", "core_metrics", default={}) or {}
        yield ("user.claude_code.sessions", _g(cc_core, "distinct_session_count"), utags)
        yield ("user.claude_code.commits", _g(cc_core, "commit_count"), utags)
        yield ("user.claude_code.prs", _g(cc_core, "pull_request_count"), utags)
        yield ("user.claude_code.lines_added", _g(cc_core, "lines_of_code", "added_count"), utags)
        yield ("user.claude_code.lines_removed", _g(cc_core, "lines_of_code", "removed_count"), utags)

        tool_actions = _g(row, "claude_code_metrics", "tool_actions", default={}) or {}
        for tool_name, tool_data in tool_actions.items():
            if not isinstance(tool_data, dict):
                continue
            tname = tool_name[:-len("_tool")] if tool_name.endswith("_tool") else tool_name
            for outcome in ("accepted", "rejected"):
                yield (
                    "user.claude_code.tool_actions",
                    _num(tool_data.get(outcome + "_count")),
                    utags + [_tag("tool", tname), _tag("outcome", outcome)],
                )

        yield ("user.web_search_count", _num(row.get("web_search_count")), utags)


# --- /usage_report (grouped by model, product) ----------------------------

def from_usage_report(rows, report_date):
    rd = _rd_tag(report_date)
    for row in rows:
        tags = [
            rd,
            _tag("model", row.get("model")),
            _tag("product", row.get("product")),
            _tag("context_window", row.get("context_window")),
        ]
        yield ("tokens.uncached_input", _num(row.get("uncached_input_tokens")), tags)
        yield ("tokens.cache_read", _num(row.get("cache_read_input_tokens")), tags)
        yield ("tokens.cache_write_1h", _num(_g(row, "cache_creation", "ephemeral_1h_input_tokens")), tags)
        yield ("tokens.cache_write_5m", _num(_g(row, "cache_creation", "ephemeral_5m_input_tokens")), tags)
        yield ("tokens.output", _num(row.get("output_tokens")), tags)
        yield ("requests", _num(row.get("requests")), tags)
        yield ("web_search_requests", _num(_g(row, "server_tool_use", "web_search_requests")), tags)


# --- /cost_report (grouped by model, product) -----------------------------

def from_cost_report(rows, report_date):
    rd = _rd_tag(report_date)
    for row in rows:
        tags = [
            rd,
            _tag("model", row.get("model")),
            _tag("product", row.get("product")),
            _tag("currency", row.get("currency") or "USD"),
        ]
        yield ("cost.amount_usd", _cents_to_usd(row.get("amount")), tags)
        yield ("cost.list_amount_usd", _cents_to_usd(row.get("list_amount")), tags)


# --- /user_usage_report ---------------------------------------------------

def from_user_usage_report(rows, report_date):
    rd = _rd_tag(report_date)
    for row in rows:
        email = _g(row, "actor", "email", default="unknown")
        utags = [rd, _tag("user_email", email)]
        yield ("user.tokens_total", _num(row.get("total_tokens")), utags)
        yield ("user.uncached_input_tokens", _num(row.get("uncached_input_tokens")), utags)
        yield ("user.output_tokens", _num(row.get("output_tokens")), utags)
        yield ("user.cache_read_tokens", _num(row.get("cache_read_input_tokens")), utags)
        yield (
            "user.cache_write_5m_tokens",
            _num(_g(row, "cache_creation", "ephemeral_5m_input_tokens")),
            utags,
        )
        yield (
            "user.cache_write_1h_tokens",
            _num(_g(row, "cache_creation", "ephemeral_1h_input_tokens")),
            utags,
        )
        yield ("user.requests", _num(row.get("requests")), utags)


# --- /user_cost_report ----------------------------------------------------

def from_user_cost_report(rows, report_date):
    rd = _rd_tag(report_date)
    for row in rows:
        email = _g(row, "actor", "email", default="unknown")
        utags = [rd, _tag("user_email", email), _tag("currency", row.get("currency") or "USD")]
        yield ("user.cost.amount_usd", _cents_to_usd(row.get("amount")), utags)
        yield ("user.cost.list_amount_usd", _cents_to_usd(row.get("list_amount")), utags)
