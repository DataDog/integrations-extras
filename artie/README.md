# Artie

## Overview

[Artie][1] is a fully managed change data capture (CDC) platform that streams changes from your production databases to your data warehouse, data lake, or another database in real time. Artie captures inserts, updates, deletes, and schema changes from sources such as PostgreSQL, MySQL, SQL Server, MongoDB, DynamoDB, and Oracle, and merges them into destinations such as Snowflake, BigQuery, Databricks, Redshift, ClickHouse, PostgreSQL, and Iceberg with sub-minute latency. See the full list of [supported sources][2] and [destinations][3].

This integration sends metrics from your Artie pipelines to Datadog so you can monitor replication health alongside the rest of your stack. It includes an out-of-the-box **Artie Overview** dashboard and the following metrics:

- **Rows processed**, broken down by pipeline, table, and operation type (create, update, delete, or backfill)
- **Ingestion lag**, measured both in time and in the number of rows still waiting to be processed
- **Flush count and flush time**, including the reason each flush was triggered (`rows`, `size`, or `time`)
- **PostgreSQL replication slot size**, so you can catch unconsumed write-ahead log (WAL) growth before it fills your source database's disk

Use these metrics to build Datadog monitors for pipelines that fall behind, tune [flush rules][4] for throughput and latency, and correlate replication behavior with source database and warehouse metrics you already collect in Datadog.

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

A continuously growing `artie.replication_slot_size_mb` means PostgreSQL is retaining WAL that Artie has not consumed yet, which can eventually exhaust disk space on the source. See [PostgreSQL troubleshooting][12] for diagnosis steps. Consider adding a Datadog monitor on this metric with a threshold appropriate for your database's free disk space.

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
