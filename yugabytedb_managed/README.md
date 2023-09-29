# YugabyteDB Managed

## Overview

[YugabyteDB][9] is a cloud-native, distributed database that is API compatible with PostgreSQL.

[YugabyteDB Managed][1], YugabyteDB's DBaaS, offers an out-of-box integration to provide customers the ability to export metrics from a cluster into Datadog. The integration comes pre-bundled with a dashboard to provide visibility into all the most important metrics needed to monitor the health and performance of a YugabyteDB Managed cluster such as:
- Node resource usage (disk, memory, CPU, networking, etc).
- Read/write operation throughput and latencies (both YSQL and YCQL).
- Advanced Master and Tablet Server telemetry (internal RPC throughput/latencies, WAL size, etc)

## Setup
- **Note:** This feature is not available for [Sandbox Clusters][5].
- Additional setup documentation can be found [here][6].

### Installation

To enable the YugabyteDB Managed integration with Datadog:

#### Create a configuration
1. Within YugabyteDB Managed, go to the **Metrics** tab under the **Integrations** page from the navigation panel on the left side of the page.
2. Select the **Add Export Configuration** button.
3. Choose the **Datadog** provider.
4. Fill in the **API key** and **Site** fields with the corresponding values.
   - The **API key** is associated with your Datadog organization. If you don't have an API key to use with your YugabyteDB Managed cluster, you need to create one in your [Datadog Organization Settings][2]. For further instructions, see the [Datadog documentation][3].
   - Your **Site** corresponds to your Datadog Site URL. For more details, see the [Datadog documentation][4].
5. You can validate the provided configuration by clicking the **Test Configuration** button before selecting **Create Configuration**.

#### Associate a configuration to a cluster
1. Within YugabyteDB Managed, go to the **Metrics** tab under the **Integrations** page from the navigation panel on the left side of the page.
2. Find your cluster in the **Export Metrics by Cluster** table.
3. Open the dropdown for your cluster under the **Export Configuration** dropdown and select the desired configuration.
4. Wait for the **Export Status** to show `Active`.
   - **Note:** Your cluster cannot be paused or have another operation in progress when associating a configuration.

### Configuration

Open your Datadog dashboard list and select the `YugabyteDB Managed Overview` dashboard to start viewing telemetry.

## Uninstallation

To disable metrics being exported to Datadog:
1. Within YugabyteDB Managed, go to the **Metrics** tab under the **Integrations** page from the navigation panel on the left side of the page.
2. Find your cluster in the **Export Metrics by Cluster** table.
3. Open the dropdown for your cluster under the **Export Configuration** dropdown and select `None`.
4. Wait for the **Export Status** to show `-`.
   - **Note:** Your cluster cannot be paused or have another operation in progress when removing a configuration.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

YugabyteDB Managed does not include any service checks.

### Events

YugabyteDB Managed does not include any events.

## Support

Need help? Contact [YugabyteDB support][8].

[1]: https://www.yugabyte.com/managed/
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
[4]: https://docs.datadoghq.com/getting_started/site/
[5]: https://docs.yugabyte.com/preview/yugabyte-cloud/cloud-basics/create-clusters/create-clusters-free/
[6]: https://docs.yugabyte.com/preview/yugabyte-cloud/cloud-monitor/metrics-export/#datadog
[7]: https://github.com/DataDog/integrations-extras/blob/master/yugabytedb_managed/metadata.csv
[8]: https://support.yugabyte.com/
[9]: https://yugabyte.com/

