# Artie Integration

## Overview

[Artie][1] is a real-time database replication product for reliably and consistently syncing data from source databases to data warehouses.

With this integration, you can receive metrics about your Artie deployments directly to your Datadog account in order to monitor the health of your data pipelines. Metrics include number of rows processed over time, ingestion lag, flush time, and replication slot size.

## Setup

### Installation

This integration is only available for existing Artie accounts. If you're not using Artie yet and would like to start a trial, contact us at hi@artie.com.

1. Click **Connect Accounts** on the Artie integration tile to connect Datadog with Artie.
2. Log into Artie if you aren't logged in yet.
3. Review the Datadog permissions that will be granted to Artie and click **Authorize**.

### Configuration

The integration will automatically send metrics to Datadog; no further configuration is needed.

### Validation

The included dashboard should start to show data within 5-10 minutes of connecting the integration, as long as you have data flowing in your Artie deployments.

## Data Collected

### Metrics

Artie reports the following metrics for each of your deployments:

1. Rows processed - the number of rows synced from your source database to your destination database/data warehouse
2. Ingestion lag time - the median amount of time between a row being published to Kafka and being ingested into your destination
3. Ingestion row lag - the number of rows remaining to be processed in Kafka at a given time
4. Flush time - the median amount of time it takes Artie to flush data from its in-memory store into your destination
5. Replication slot size for any PostgreSQL source databases you have connected

### Service Checks

Artie does not include any service checks.

### Events

Artie does not include any events.

## Troubleshooting

Need help? Contact [Artie support][2].

[1]: https://www.artie.com/
[2]: mailto:hi@artie.com
