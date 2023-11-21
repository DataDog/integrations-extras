# YugabyteDB Managed

## Overview

[YugabyteDB][1] is a cloud-native, distributed database that is API compatible with PostgreSQL.

[YugabyteDB Managed][2] is YugabyteDB's fully-managed Database-as-a-service (DBaaS). With this integration, you can send your cluster metrics to Datadog for visibility into the health and performance of your YugabyteDB Managed clusters. This integration comes with an out-of-the-box dashboard to provide visibility into all the most important metrics needed to monitor the health and performance of a YugabyteDB Managed cluster such as:
- Node resource usage (disk, memory, CPU, networking, and more).
- Read/write operation throughput and latencies (both YSQL and YCQL).
- Advanced Master and Tablet Server telemetry (for example, internal RPC throughput/latencies and WAL read/write throughput).

## Setup
**Note**: This feature is not available for [Sandbox Clusters][3].

### Installation

To enable the YugabyteDB Managed integration with Datadog:

#### Create a configuration
1. In YugabyteDB Managed, navigate to the **Integrations > Metrics** tab.
2. Click **Create Export Configuration** or **Add Export Configuration**.
3. Select the **Datadog** provider.
4. Fill in the **API key** and **Site** fields with the corresponding values. For more information, see the [Datadog API and Application Keys][5] and [Datadog Site URL][6] documentation.
5. Click **Test Configuration** to validate the configuration.
6. Click **Create Configuration**.

#### Associate a configuration to a cluster
1. In YugabyteDB Managed, navigate to the **Integrations > Metrics** tab.
2. Find your cluster in the **Export Metrics by Cluster** table.
3. Select the desired configuration from the **Export Configuration** dropdown menu.
4. Wait for the **Export Status** to show `Active`.

**Note**: Your cluster cannot associate a configuration when paused or when another operation is in progress.

For more information on setup, see the [YugabyteDB documentation][4].

## Uninstallation

To disable metrics being exported to Datadog:
1. In YugabyteDB Managed, navigate to the **Integrations > Metrics** tab.
2. Find your cluster in the **Export Metrics by Cluster** table.
3. Open the dropdown for your cluster under the **Export Configuration** dropdown and select `None`.
4. Wait for the **Export Status** to show `-`.

**Note**: Your cluster cannot associate a configuration when paused or when another operation is in progress.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

YugabyteDB Managed does not include any service checks.

### Events

YugabyteDB Managed does not include any events.

## Support

Need help? Contact [YugabyteDB support][8].

[1]: https://yugabyte.com/
[2]: https://www.yugabyte.com/managed/
[3]: https://docs.yugabyte.com/preview/yugabyte-cloud/cloud-basics/create-clusters/create-clusters-free/
[4]: https://docs.yugabyte.com/preview/yugabyte-cloud/cloud-monitor/metrics-export/#datadog
[5]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[6]: https://docs.datadoghq.com/getting_started/site/
[7]: https://github.com/DataDog/integrations-extras/blob/master/yugabytedb_managed/metadata.csv
[8]: https://support.yugabyte.com/hc/en-us/requests/new

