# TiDB Cloud Integration

## Overview

[TiDB Cloud][1] is a fully managed cloud service of TiDB, an open-source database.

Use the TiDB Cloud Datadog integration to export metrics from TiDB Cloud clusters to Datadog.

> **Note:**
>
> - For TiDB clusters on premises, see the [TiDB Integration][4].

## Setup

To set up the TiDB Cloud Datadog integration for your cluster, provide a Datadog API key and region to TiDB Cloud.

See [TiDB Cloud Preferences][2] to configure the Datadog integration for your TiDB Cloud project.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Service Checks

The TiDB Cloud integration does not include any service checks.

### Events

The TiDB Cloud integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://tidbcloud.com
[2]: https://tidbcloud.com/console/preferences
[3]: https://docs.datadoghq.com/help/
[4]: https://docs.datadoghq.com/integrations/tidb/
[5]: https://github.com/DataDog/integrations-extras/blob/master/tidb_cloud/metadata.csv
