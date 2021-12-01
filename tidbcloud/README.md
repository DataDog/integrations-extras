# TiDB Cloud Integration

## Overview

[TiDB Cloud][1] makes deploying, managing and maintaining your TiDB clusters even simpler with a fully managed cloud instance that you control through an intuitive console. TiDB Cloud allows developers and DBAs with little or no training to handle once-complex tasks such as infrastructure management and cluster deployment with ease, to focus on your applications, not the complexities of your database.

The Datadog integration is an observability feature of TiDB Cloud that exports metrics of TiDB Cloud clusters to your Datadog platform.

> **Note:**
>
> - For TiDB clusters on premises, please refer to [TiDB Integration][4].

## Setup

To set up the TiDB Cloud Datadog integration for your cluster, provide a Datadog API key and region to TiDB Cloud.

Refer to the [TiDB Cloud Preferences Page][2] to configure the Datadog integration for your TiDB Cloud project.

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
[5]: https://github.com/DataDog/integrations-extras/blob/master/tidbcloud/metadata.csv
