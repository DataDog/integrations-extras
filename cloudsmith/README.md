# Agent Check: Cloudsmith

## Overview

This check monitors [Cloudsmith][1] through the Datadog Agent.
- Monitor storage, bandwidth and token usage in your Cloudsmith account. 

### Data Freshness Notes
The current `cloudsmith.storage_used` and `cloudsmith.bandwidth_used` metrics are sourced from Cloudsmith's quota endpoint, which is updated by Cloudsmith at most once per day. This means rapid changes during the day may not immediately appear in these percentage metrics. They remain valuable for daily quota tracking, trend visualization, and threshold alerting (warning at 75%, critical at 85%).

To visualize historical daily usage, the provided dashboard now includes time series (line and bar) widgets for storage and bandwidth percentage. You can clone the dashboard and adjust time ranges (e.g., last 30 days) to see how quota consumption evolves.

Real-time bandwidth bytes are available via the Cloudsmith v2 analytics time-series endpoint and are disabled by default for backward compatibility. When enabled they provide:

* `cloudsmith.bandwidth_bytes_interval`: Total bytes downloaded in the most recent minute bucket.

Enable by setting `enable_realtime_bandwidth: true` in `cloudsmith.yaml`. All other parameters (interval, aggregation, look-back, refresh cadence) use sensible internal defaults and do not require configuration.

If the endpoint returns fewer than two data points the integration skips emission for that cycle to prevent misleading values.

Dashboard queries include the template variable `cloudsmith_org` so you can scope all views to a specific organization or switch between them easily.


## Setup

The Cloudsmith check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Cloudsmith check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-cloudsmith==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `cloudsmith.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Cloudsmith performance data. See the [sample cloudsmith.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `cloudsmith` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

### Events

All Cloudsmith related events collected appear within the Datadog Event Stream with the `source:cloudsmith` property. They are collected every five minutes to reduce the number of requests sent to the Cloudsmith API.

There are two types of events:

- Security Scan event
- Audit Logs event

They are accessible with aggregation keys: `@aggregation_key:audit_log` and `@aggregation_key:vulnerabilities`.

### Historical Quota Usage Visualization
Recommended dashboard widgets for tracking daily quota usage:
* Query Value (current percent used): `avg:cloudsmith.storage_used{*}` and `avg:cloudsmith.bandwidth_used{*}`
* Time Series Line (daily trend): `avg:cloudsmith.storage_used{*}` over last 30d
* Time Series Bar (daily discrete view): same queries with display style set to bars

Because values update daily, consider setting longer time ranges (7d, 30d) to derive consumption trends and projections.

## Troubleshooting

Need help? Contact [Cloudsmith support][10].

[1]: https://cloudsmith.com
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/datadog_checks/cloudsmith/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/cloudsmith/assets/service_checks.json
[10]: https://help.cloudsmith.io/docs/contact-us#live-chat-via-intercom
