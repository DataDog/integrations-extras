# Agent Check: Claude Enterprise Analytics

> **Unofficial integration.** This check is community-maintained and **not affiliated with, endorsed by, or supported by Anthropic, PBC**. "Anthropic" and "Claude" are trademarks of Anthropic, PBC. For official support of the underlying API, contact Anthropic.

## Overview

This integration pulls daily usage, cost, and seat-utilization data from the [Anthropic Claude Enterprise Analytics API][1] and submits it to Datadog as metrics. It is useful for Anthropic enterprise customers who want Claude usage observability inside their existing Datadog dashboards: cost attribution per user/model/product, seat adoption tracking, Claude Code activity (commits, PRs, lines, tool acceptance rate), token mix and cache effectiveness, and web-search usage.

The check polls six API endpoints once per collection interval for a single past day (default: today minus 3, because Anthropic's analytics have a 3-day aggregation lag):

- `/summaries` -- org-wide DAU/WAU/MAU, assigned seats, adoption rates
- `/users` -- per-user activity across chat, projects, artifacts, Claude Code, web search
- `/usage_report` -- token consumption by model and product
- `/cost_report` -- USD spend by model and product (list price; see "Known Limitations")
- `/user_usage_report` -- per-user token totals
- `/user_cost_report` -- per-user USD spend

All metrics are emitted as gauges at agent wall-clock time and tagged with `report_date:YYYY-MM-DD` representing the activity day. Build dashboards that filter or group by `report_date` rather than relying on Datadog's wall-clock x-axis.

## Setup

### Installation

1. Install the [Datadog Agent][2] on your host.
2. Install this integration from the `integrations-extras` repo:
   ```
   datadog-agent integration install -t datadog-claude-enterprise-analytics==<version>
   ```

### Configuration

1. Generate an API key at [claude.ai/analytics/api-keys][1] (requires the Primary Owner role on your Anthropic org). The key must carry the `read:analytics` scope.
2. Edit `claude_enterprise_analytics.d/conf.yaml` in your Agent's `conf.d/` directory:
   ```yaml
   instances:
     - anthropic_api_key: <YOUR_KEY>
       org_id: my-org             # free-form tag value, surfaced on every metric
       lag_days: 3                 # how many days behind today to poll
       min_collection_interval: 3600  # once per hour is plenty; Anthropic refreshes daily
   ```
   See [`conf.yaml.example`][4] for all options.
3. [Restart the Agent][5].

### Validation

Run [`datadog-agent status`][6] and look for `claude_enterprise_analytics` under the Checks section. Then in the Datadog UI, open Metrics Explorer and search for `claude_enterprise_analytics.*` -- you should see ~45 metrics arrive within one collection interval.

## Data Collected

### Metrics

45 gauges under the `claude_enterprise_analytics.` namespace. Highlights:

- `claude_enterprise_analytics.org.dau` / `.wau` / `.mau` / `.seats_assigned` / `.adoption_rate.{daily,weekly,monthly}`
- `claude_enterprise_analytics.cost.amount_usd` / `.list_amount_usd` (tagged by `model`, `product`)
- `claude_enterprise_analytics.user.cost.amount_usd` (tagged by `user_email`)
- `claude_enterprise_analytics.tokens.{uncached_input,output,cache_read,cache_write_1h,cache_write_5m}`
- `claude_enterprise_analytics.user.claude_code.{sessions,commits,prs,lines_added,lines_removed,tool_actions}`
- `claude_enterprise_analytics.web_search_requests`

See [`metadata.csv`][7] for the full list with descriptions and tag keys.

### Events

This integration does not submit events.

### Service Checks

- `claude_enterprise_analytics.can_connect` -- `CRITICAL` if the Anthropic API could not be reached during the check run, otherwise `OK`. See [`service_checks.json`][8].

## Known Limitations

- **Cost is list-priced.** Anthropic's API returns `amount` equal to `list_amount` in every response. Enterprise contract discounts are not exposed through this API, so the dashboard's USD figures reflect retail compute consumption rather than your actual invoice. Treat cost data as a relative attribution signal (which model/user is most expensive) rather than as billing truth.
- **3-day data lag.** Each report represents activity from `today - 3` (configurable via `lag_days`). Polling more frequently than once per day will resubmit the same daily totals.
- **Datadog metric submission window.** Metrics are submitted at the agent's current wall-clock time, not the activity date -- Datadog rejects timestamps more than ~1h in the past. The activity date is preserved via the `report_date` tag; dashboards must group/filter by it.
- **Cost is returned in USD cents** (smallest currency subunit) despite the `currency: USD` field. This check divides by 100 before submission.

## Troubleshooting

- **No data after a fresh install:** Anthropic's analytics endpoint can return empty bodies for very recent dates. Try increasing `lag_days` from 3 to 5.
- **`401 Unauthorized`:** confirm the API key is generated by a Primary Owner and carries the `read:analytics` scope.
- **`400 Bad Request`** on the first run: the underlying analytics endpoints expect strict-before date ranges; this check handles that automatically, but a mismatched system clock can produce the wrong date. Verify the agent host has accurate UTC time.

Need help with the integration itself? Open an issue against the [integrations-extras repository][10]. For Anthropic API issues, contact your Anthropic account team.

[1]: https://support.claude.com/en/articles/13703965-claude-enterprise-analytics-api-reference-guide
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/containers/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/claude_enterprise_analytics/datadog_checks/claude_enterprise_analytics/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/configuration/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/configuration/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/claude_enterprise_analytics/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/claude_enterprise_analytics/assets/service_checks.json
[10]: https://github.com/DataDog/integrations-extras/issues
