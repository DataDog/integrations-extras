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

The included dashboard will start to show data 5-10 minutes after you connect the integration as long as you have data flowing in your Artie deployments.


## Troubleshooting

Need help? Contact [Artie support][2].

[1]: https://www.artie.com/
[2]: mailto:hi@artie.com
