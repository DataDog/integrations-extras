# Agent Check: ClickHouse Cloud

## Overview

[ClickHouse Cloud][1] is a fully managed cloud-native data warehouse for real-time analytics, built on the open-source ClickHouse database.

This integration collects query logs and server logs from ClickHouse Cloud via the [Cloud Query API][2] and ships them to Datadog Logs. It monitors completed queries and exceptions from `system.query_log`, as well as error and warning entries from `system.text_log`, providing visibility into query performance, failures, and server health.

## Setup

### Installation

The ClickHouse Cloud check is not included in the [Datadog Agent][3] package, so you need to install it.

For Agent v7.21+ / v6.21+, follow the instructions below to install the ClickHouse Cloud check on your host. See [Use Community Integrations][4] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-clickhouse_cloud==0.1.0
   ```

2. Configure your integration similar to core [integrations][5].

### Configuration

1. Edit the `clickhouse_cloud.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your ClickHouse Cloud data. See the [sample clickhouse_cloud.d/conf.yaml][6] for all available configuration options.

2. [Restart the Agent][7].

**Note:** The `logs:` section with `type: integration` in the configuration file is required for log collection to function. Ensure `logs_enabled: true` is set in your main `datadog.yaml`.

### Validation

[Run the Agent's status subcommand][8] and look for `clickhouse_cloud` under the Checks section.

## Data Collected

### Metrics

This integration submits the following operational metrics to track log collection throughput:

- **`clickhouse_cloud.query_log.rows_collected`**: Number of query log rows collected per check run.
- **`clickhouse_cloud.text_log.rows_collected`**: Number of text log rows collected per check run.

See [metadata.csv][9] for the full list.

### Service Checks

See [service_checks.json][10] for a list of service checks provided by this integration.

### Events

The ClickHouse Cloud integration does not include any events.

## Support

Need help? Contact [Datadog support][11].

[1]: https://clickhouse.com/cloud
[2]: https://clickhouse.com/docs/en/cloud/manage/query-api
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[5]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://github.com/DataDog/integrations-extras/blob/master/clickhouse_cloud/datadog_checks/clickhouse_cloud/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[9]: https://github.com/DataDog/integrations-extras/blob/master/clickhouse_cloud/metadata.csv
[10]: https://github.com/DataDog/integrations-extras/blob/master/clickhouse_cloud/assets/service_checks.json
[11]: https://docs.datadoghq.com/help/
