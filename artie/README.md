# Artie

## Overview

[Artie][1] is a fully managed change data capture (CDC) platform that streams changes from your production databases to your data warehouse, data lake, or another database in real time. Artie captures inserts, updates, deletes, and schema changes from sources such as PostgreSQL, MySQL, SQL Server, MongoDB, DynamoDB, and Oracle, and merges them into destinations such as Snowflake, BigQuery, Databricks, Redshift, ClickHouse, PostgreSQL, and Iceberg with sub-minute latency. See the full list of [supported sources][2] and [destinations][3].

This integration sends metrics from your Artie pipelines to Datadog so you can monitor replication health alongside the rest of your stack. It includes an out-of-the-box **Artie Overview** dashboard and the following metrics:

- **Rows processed**, broken down by pipeline, table, and operation type (create, update, delete, or backfill)
- **Ingestion lag**, measured both in time and in the number of rows still waiting to be processed
- **Flush count and flush time**, including the reason each flush was triggered (`rows`, `size`, or `time`)
- **PostgreSQL replication slot size**, so you can catch unconsumed write-ahead log (WAL) growth before it fills your source database's disk

Use these metrics to build Datadog monitors for pipelines that fall behind, tune [flush rules][4] for throughput and latency, and correlate replication behavior with source database and warehouse metrics you already collect in Datadog.

### How it works

Artie collects metrics from every running pipeline as part of normal operation. Once you connect the integration, Artie submits those metrics to the Datadog metrics API on a short interval using an API key it creates in your Datadog organization. No Datadog Agent, collector, or configuration file is involved, and no network access to your databases or Artie infrastructure is required.

Each data point carries the time the activity happened, not the time it was submitted, so series line up with your other Datadog metrics. Expect new activity to appear a few minutes after it happens.

Only pipelines in the **Running** state are exported. Paused pipelines stop reporting until they are resumed. Rows processed during a backfill are included and tagged `operation:backfill`, so you can separate initial loads from ongoing changes.

## Setup

### Prerequisites

- **An Artie account.** If you don't have one yet, [sign up][5] with your work email. New accounts start with a 14-day trial, no credit card required, and a free plan is available after the trial. See [Artie pricing][6] for current plan limits.
- **At least one running pipeline.** Artie only emits metrics for pipelines that are actively replicating data. See the [Artie quickstart][7] to create your first pipeline.
- **An Artie Admin role.** Only Artie Admins can connect or disconnect the Datadog integration. See [Managing your team][8].
- **A Datadog user with the API Keys Write permission.** During setup, Artie creates a Datadog API key in your organization and uses it to submit metrics. Datadog checks this against the permissions of the user who authorizes the connection, so the authorization fails if that user cannot create API keys. See [Datadog role permissions][15].

The integration works with all Datadog sites, including US1, US3, US5, EU1, AP1, and US1-FED, as well as custom subdomains.

### Installation

No Datadog Agent or configuration file is required. Artie pushes metrics directly to Datadog after you authorize the connection.

1. In Datadog, open the Artie integration tile and click **Connect Accounts**.
2. Log in to Artie if you aren't logged in already. The integration is connected to the Artie company you are logged in to.
3. Review the Datadog permissions that will be granted to Artie, then click **Authorize**.

After authorization, Artie redirects you to a confirmation page and starts sending metrics for every running pipeline in your Artie company. Pipelines you create later are included automatically. You can check the connection status at any time under **Settings** > **Integrations** in Artie.

Each Artie company can be connected to one Datadog organization. If the integration is already connected, disconnect it in Artie before connecting again.

### Validation

Metrics appear in Datadog within 5-10 minutes of connecting, as long as at least one pipeline is replicating data.

To confirm:

1. In Datadog, go to **Dashboards** > **Dashboard List** and open **Artie Overview**. The **Rows processed** and **Ingestion lag** widgets populate first.
2. Alternatively, open the [Metrics Explorer][9] and search for `artie.rows_processed`.

If no data appears after 15 minutes, see the Troubleshooting section below.

### Uninstallation

1. In Artie, open **Settings** > **Integrations**, click **Manage** next to Datadog, then click **Disconnect**. Artie stops sending metrics immediately.
2. In Datadog, open the Artie integration tile and click **Uninstall Integration**.
3. In Datadog, go to **Organization Settings** > **API Keys** and delete the API key that Artie created.

Uninstalling removes the integration's dashboard and associated assets from your Datadog account. Metrics already ingested remain available for the duration of your Datadog retention period. To reconnect later, complete all three steps above first, then follow the Installation steps again.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

How to read each metric:

| Metric                           | What it tells you                                                                                                                                                                                                                                                             |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `artie.rows_processed`           | Rows Artie wrote to the destination, by pipeline, table, and operation. A sustained drop to zero on a busy table usually means the source stopped producing changes or the pipeline is stalled. Backfill rows are tagged `operation:backfill`.                                      |
| `artie.ingestion_lag_ms`         | Median time between a change being captured from the source and Artie processing it. This is the main freshness signal. It rises when the destination cannot absorb flushes fast enough, or during a backfill of a large table.                                                     |
| `artie.row_lag`                  | Number of captured rows waiting to be processed. Read it together with `artie.ingestion_lag_ms`: high row lag with low time lag means a burst is being worked through, while both rising together means the pipeline is falling behind.                                         |
| `artie.flush_count`              | Number of flushes from Artie's in-memory buffer to the destination, by reason. Many `time` flushes with few rows each means batches are too small for a warehouse destination. Many `rows` or `size` flushes means the pipeline is keeping up with high volume.                       |
| `artie.flush_time_ms`            | Median time a flush takes to complete. Flush time is dominated by the destination's merge step, so a rising value usually points at the destination (warehouse queueing, undersized compute, or a large table being merged) rather than at Artie.                                   |
| `artie.replication_slot_size_mb` | Size of the PostgreSQL replication slot Artie is consuming. PostgreSQL retains WAL until Artie confirms it, so this should hover near zero in steady state. Sustained growth means the pipeline is paused or behind, and left unchecked it can fill the source database's disk. |

All metrics carry the following tags so you can filter and group by pipeline, connector, and table:

| Tag           | Description                                                                                                  |
|---------------|--------------------------------------------------------------------------------------------------------------|
| `pipeline`    | The name of the Artie pipeline.                                                                              |
| `deployment`  | Same value as `pipeline`. Kept for compatibility with the included dashboard and existing monitors.          |
| `source`      | The name of the pipeline's source connector in Artie.                                                        |
| `destination` | The name of the pipeline's destination connector in Artie.                                                   |
| `data_plane`  | The Artie data plane the pipeline runs on.                                                                   |
| `environment` | The Artie environment the pipeline belongs to. Only present if your company uses environments.               |
| `table`       | The source table name. Not present on `artie.replication_slot_size_mb`.                                      |

Some metrics carry additional tags:

| Tag         | Metrics                                      | Description                                                        |
|-------------|----------------------------------------------|--------------------------------------------------------------------|
| `operation` | `artie.rows_processed`                       | The row operation type: `create`, `update`, `delete`, or `backfill`. |
| `reason`    | `artie.flush_count`, `artie.flush_time_ms`   | What triggered the flush: `rows`, `size`, or `time`.               |
| `slotname`  | `artie.replication_slot_size_mb`             | The PostgreSQL replication slot name.                              |

### Events

The Artie integration does not include any events.

### Service Checks

The Artie integration does not include any service checks.

## Dashboard

The **Artie Overview** dashboard is installed with the integration and is organized into four groups:

- **Overview**: total rows processed and current ingestion lag across all pipelines.
- **Data Volume**: rows processed over time, and the split by operation, pipeline, and table.
- **Performance**: ingestion lag in time and in rows, flush count by reason, and flush time.
- **Database Health**: PostgreSQL replication slot size per pipeline and slot.

Use the `deployment`, `table`, and `operation` template variables at the top of the dashboard to focus on one pipeline or table. Integration dashboards are read-only, so clone it first if you want to customize it.

## Monitoring

Artie metrics work with standard [Datadog metric monitors][16]. The following examples are starting points. Adjust the thresholds to your pipelines' normal behavior, which you can read off the dashboard after a few days of data.

Alert when any table on any pipeline falls more than five minutes behind:

```text
avg(last_15m):avg:artie.ingestion_lag_ms{*} by {pipeline,table} > 300000
```

Alert when a pipeline that is normally busy processes no rows for an hour:

```text
sum(last_1h):sum:artie.rows_processed{pipeline:prod-postgres-to-snowflake}.as_count() < 1
```

Alert when a PostgreSQL replication slot grows past 10 GB:

```text
max(last_10m):max:artie.replication_slot_size_mb{*} by {pipeline,slotname} > 10240
```

Artie also provides built-in [custom monitors][17] for data volume, ingestion lag, and replication slot size, with notifications to the recipients you choose. Use those if you prefer to alert from Artie, and use Datadog monitors when you want Artie alerts to follow the same routing and escalation as the rest of your infrastructure.

## Limits

- The integration sends metrics only. It does not send logs, traces, or events.
- Metrics are submitted as custom metrics, and every distinct combination of tag values is a separate time series. Pipelines with many tables produce correspondingly more series. See [Datadog custom metrics billing][18] to understand how this affects your plan.
- Each Artie company can be connected to one Datadog organization at a time.
- Metrics are aggregated by Artie before submission. `artie.ingestion_lag_ms` and `artie.flush_time_ms` are medians, so individual slow rows or flushes are not visible as outliers.
- If you also use Grafana, Artie can send the same metrics to Grafana Cloud or a Prometheus remote-write endpoint. See [Artie monitoring integrations][19].

## Troubleshooting

**No metrics are showing up in Datadog**

- Confirm that at least one pipeline has the **Running** status in the [Artie dashboard][11]. Only running pipelines are exported. Paused pipelines and pipelines that are still deploying do not emit metrics.
- Confirm that Datadog shows as **Connected** under **Settings** > **Integrations** in Artie.
- Wait up to 10 minutes after connecting. Metrics are exported on a short interval rather than streamed continuously.

**Authorization fails with "Your Datadog user doesn't have permission to create API keys"**

The Datadog user who clicks **Authorize** needs the API Keys Write permission. Ask a Datadog admin to grant it, or have a user who already has it connect the integration.

**Authorization fails with "This Datadog connection has expired"**

The connection must be completed within a few minutes of starting it. Start again from **Connect Accounts** on the Artie integration tile in Datadog.

**Authorization fails with "datadog integration already enabled"**

Your Artie company is already connected to a Datadog organization. To connect a different one, follow the Uninstallation steps first.

**Ingestion lag is high**

Rising `artie.ingestion_lag_ms` or `artie.row_lag` usually means the destination cannot keep up with incoming changes. Check the `reason` tag on `artie.flush_count`: frequent `time` flushes with small batches on a warehouse destination add fixed latency per flush. See [Tuning flush rules][4] for guidance.

**The PostgreSQL replication slot keeps growing**

A continuously growing `artie.replication_slot_size_mb` means PostgreSQL is retaining WAL that Artie has not consumed yet, which can eventually exhaust disk space on the source. See [PostgreSQL troubleshooting][12] for diagnosis steps and [Preventing WAL growth][20] for how to set up protection on the database side. Consider adding a Datadog monitor on this metric with a threshold appropriate for your database's free disk space.

For additional help, see the [Artie documentation][13] or contact [Artie support][14].

## Support

Need help? Contact [Artie support][14].

[1]: https://www.artie.com/
[2]: https://www.artie.com/docs/sources
[3]: https://www.artie.com/docs/destinations
[4]: https://www.artie.com/docs/pipelines/flush-rules/tuning
[5]: https://app.artie.com/signup
[6]: https://www.artie.com/pricing
[7]: https://www.artie.com/docs/quickstart
[8]: https://www.artie.com/docs/account/managing-your-team
[9]: https://app.datadoghq.com/metric/explorer
[10]: https://github.com/DataDog/integrations-extras/blob/master/artie/metadata.csv
[11]: https://app.artie.com/
[12]: https://www.artie.com/docs/sources/postgresql/troubleshooting
[13]: https://www.artie.com/docs
[14]: mailto:hi@artie.com
[15]: https://docs.datadoghq.com/account_management/rbac/permissions/
[16]: https://docs.datadoghq.com/monitors/types/metric/
[17]: https://www.artie.com/docs/monitoring/custom-monitors
[18]: https://docs.datadoghq.com/account_management/billing/custom_metrics/
[19]: https://www.artie.com/docs/monitoring/integrations
[20]: https://www.artie.com/docs/guides/database/preventing-postgres-wal-growth-on-rds
