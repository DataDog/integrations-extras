# Artie Integration

## Overview

[Artie][1] is a real-time database replication product for syncing data from source databases to data warehouses.

With this integration, you can view metrics about your Artie deployments directly in Datadog to monitor the health of your data pipelines. Metrics from this integration include the number of rows processed over time, ingestion lag, flush time, and replication slot size.

## Setup

### Installation

This integration is only available for existing Artie accounts. If you're not using Artie yet and would like to start a trial, email hi@artie.com.

1. In Datadog, click **Connect Accounts** on the Artie integration tile to connect Datadog with Artie.
2. Log into Artie if you aren't logged in yet.
3. Review the Datadog permissions that will be granted to Artie and click **Authorize**.

### Configuration

The integration will automatically send metrics to Datadog; no further configuration is needed.

### Validation

The included dashboard start to show data 5-10 minutes after you connect the integration, as long as you have data flowing in your Artie deployments.

## Data Collected

### Metrics

Artie reports the following metrics for each of your deployments:

| Metric                | Description                                                                                                       |
| --------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Rows processed        | The number of rows synced from your source database to your destination database or data warehouse                |
| Ingestion lag time    | The median amount of time (in ms) between a row being published to Kafka and being ingested into your destination |
| Ingestion row lag     | The number of rows remaining to be processed in Kafka at a given time                                             |
| Flush time            | The median amount of time (in ms) it takes Artie to flush data from its in-memory store into your destination     |
| Replication slot size | The size (in MB) of the replication slot Artie is using in any PostgreSQL source databases you have connected     |

### Service Checks

Artie does not include any service checks.

### Events

Artie does not include any events.

## Troubleshooting

Need help? Contact [Artie support][2].

[1]: https://www.artie.com/
[2]: mailto:hi@artie.com
