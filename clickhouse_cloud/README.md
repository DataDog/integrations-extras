# Agent Check: ClickHouse Cloud

## Overview

[ClickHouse Cloud][1] is a fully managed cloud-native data warehouse for real-time analytics. This integration collects query logs and server logs from ClickHouse Cloud via the [Cloud Query API][2] and ships them to Datadog Logs.

The check queries two ClickHouse system tables:

- **`system.query_log`** - Completed queries and exceptions with duration, memory usage, read/write stats, and error details.
- **`system.text_log`** - Server-side log entries at Error, Warning, Fatal, and Critical levels.

Key features:

- Cursor-based pagination that resumes where it left off across Agent restarts.
- Automatic filtering of ClickHouse Cloud internal service accounts (~99% noise reduction on idle clusters).
- Slow query highlighting with configurable threshold.
- Two service checks for connectivity monitoring.

## Setup

### Prerequisites

1. A ClickHouse Cloud service with the **Cloud Query API** enabled.
2. An API key pair (key ID + key secret) created at [ClickHouse Cloud API Keys][3] with query access permissions.

### Installation

Run the following command to install the Agent integration:

```shell
datadog-agent integration install -t datadog-clickhouse_cloud==0.1.0
```

For containerized environments, see the [Datadog documentation][4].

### Configuration

1. Edit the `clickhouse_cloud.d/conf.yaml` file in the `conf.d/` folder at the root of your Agent's configuration directory.

   ```yaml
   instances:
     - service_id: "<YOUR_SERVICE_UUID>"
       key_id: "<YOUR_API_KEY_ID>"
       key_secret: "<YOUR_API_KEY_SECRET>"
       cluster_name: "production-clickhouse"

   logs:
     - type: integration
       source: clickhouse
   ```

   **Important:** The `logs:` section is required. Without it, `send_log()` silently fails.

2. [Restart the Agent][5].

See the [example configuration][6] for all available options.

### Multi-Service Monitoring

To monitor multiple ClickHouse Cloud services, add one instance block per service:

```yaml
instances:
  - service_id: "<PROD_SERVICE_UUID>"
    key_id: "<PROD_KEY_ID>"
    key_secret: "<PROD_KEY_SECRET>"
    cluster_name: "prod-clickhouse"

  - service_id: "<STAGING_SERVICE_UUID>"
    key_id: "<STAGING_KEY_ID>"
    key_secret: "<STAGING_KEY_SECRET>"
    cluster_name: "staging-clickhouse"
```

### Validation

Run the [Agent's status subcommand][7] and look for `clickhouse_cloud` under the Checks section.

## Data Collected

### Logs

This integration collects logs from ClickHouse Cloud system tables and sends them to Datadog with the following attributes:

**Query Logs** (`system.query_log`):

| Attribute | Description |
|---|---|
| `clickhouse.query_id` | Unique query identifier |
| `clickhouse.user` | User who executed the query |
| `clickhouse.duration_ms` | Query execution time in milliseconds |
| `clickhouse.memory_bytes` | Peak memory usage |
| `clickhouse.read_rows` | Number of rows read |
| `clickhouse.read_bytes` | Number of bytes read |
| `clickhouse.written_rows` | Number of rows written |
| `clickhouse.written_bytes` | Number of bytes written |
| `clickhouse.exception` | Exception message (if any) |
| `clickhouse.exception_code` | ClickHouse error code |
| `clickhouse.query_type` | `finish` or `exception` |
| `clickhouse.query_kind` | `Select`, `Insert`, `Create`, etc. |
| `clickhouse.database` | Target database |
| `clickhouse.tables` | Tables accessed |
| `clickhouse.client` | Client application name |

**Text Logs** (`system.text_log`):

| Attribute | Description |
|---|---|
| `clickhouse.logger` | ClickHouse logger component name |
| `clickhouse.thread_id` | Thread identifier |
| `clickhouse.query_id` | Associated query identifier |

### Metrics

| Metric | Type | Description |
|---|---|---|
| `clickhouse_cloud.query_log.rows_collected` | gauge | Number of query log rows collected per check run |
| `clickhouse_cloud.text_log.rows_collected` | gauge | Number of text log rows collected per check run |

### Service Checks

**clickhouse_cloud.query_log.can_connect**

Returns `CRITICAL` if the check cannot query the ClickHouse Cloud Query API for query logs. Returns `OK` otherwise.

**clickhouse_cloud.text_log.can_connect**

Returns `CRITICAL` if the check cannot query the ClickHouse Cloud Query API for server text logs. Returns `OK` otherwise.

### Events

ClickHouse Cloud does not include any events.

## Troubleshooting

### No logs appearing

1. Verify the `logs:` section exists in your `conf.yaml` with `type: integration` and `source: clickhouse`.
2. Check that `logs_enabled: true` is set in your main `datadog.yaml`.
3. Run `datadog-agent status` and look for the check under the Collector section.

### "file is nil" error

This means the `logs:` block is missing from your configuration. Add it:

```yaml
logs:
  - type: integration
    source: clickhouse
```

### High log volume

Set `exclude_internal_users: true` (the default) to filter ClickHouse Cloud internal service accounts. On idle clusters, this reduces query_log volume by ~99%.

Need help? Contact [rahuljain3109@gmail.com][8].

## Support

For support or feature requests, contact the author:

- Email: [rahuljain3109@gmail.com][8]
- Repository: [github.com/pythonicrahul/datadog-clickhouse-cloud][9]

[1]: https://clickhouse.com/cloud
[2]: https://clickhouse.com/docs/en/cloud/manage/query-api
[3]: https://clickhouse.cloud/settings/api-keys
[4]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://github.com/DataDog/integrations-extras/blob/master/clickhouse_cloud/datadog_checks/clickhouse_cloud/data/conf.yaml.example
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: mailto:rahuljain3109@gmail.com
[9]: https://github.com/pythonicrahul/datadog-clickhouse-cloud
