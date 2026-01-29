# Starburst Galaxy

## Overview

The Starburst Galaxy integration for Datadog enables you to collect Starburst Galaxy cluster performance metrics using the Datadog platform.

## Setup

The Starburst Galaxy integration with Datadog enables you to monitor and visualize your Starburst Galaxy cluster metrics directly in your Datadog account. This integration automatically exports cluster performance metrics, query execution statistics, and resource utilization data to Datadog.

#### Installation

To enable Datadog monitoring for Starburst Galaxy:

1. In Starburst Galaxy's navigation menu, click **Partner Connect > Observability**.

2. Locate **Datadog** in the list of available integrations and click on the Datadog card.

3. Fill in the **API key** and **Datadog Site** fields with the corresponding values.

   - The API key is associated with your Datadog organization. If you don't have an API key, you need to create one. For instructions, see the [Datadog API Keys documentation][1].
   - Your Datadog Site corresponds to your Datadog Site URL. For more details, see the [Datadog Getting Started documentation][2].

4. Click **Validate** to test the connection. Starburst Galaxy will verify that the API key is valid and the selected Datadog site is accessible.

5. Once validation succeeds, click **Connect**.

6. Once registered with Datadog, cluster metrics will appear in your Datadog account. This can take up to several minutes.

##### Viewing Your Metrics in Datadog

Once the integration is active, Starburst Galaxy exports metrics with the following characteristics:

- **Metric Namespace:** All metrics are prefixed with `starburst_galaxy.`
- **Metric Format:** Metrics follow the pattern `starburst_galaxy.io_starburst_galaxy_name_GalaxyMetrics_<metric_name>`

To preview the metrics being collected:

1. Navigate to **Metrics > Explorer** or **Metrics > Summary** in Datadog.
2. Search for metrics starting with `starburst_galaxy.`
3. You should see metrics such as:
   - `starburst_galaxy.io_starburst_galaxy_name_GalaxyMetrics_RunningQueries`
   - `starburst_galaxy.io_starburst_galaxy_name_GalaxyMetrics_QueuedQueries`
   - `starburst_galaxy.io_starburst_galaxy_name_GalaxyMetrics_WorkerCount`

##### Validation

Once enabled, the integration status in the Datadog panel on the Starburst Galaxy's **Partner Connect** page will show as **Connected**.

If you encounter an issue during the integration, contact Starburst support.

#### Update Integration

To update the metadata associated with the integration (for example, to rotate API keys):

1. In the Datadog panel on the **Partner Connect** page, click on the configured integration.
2. Click **Edit connection**.
3. Update the **API key** and **Datadog Site** fields as needed.
4. Click **Validate** to test the new configuration.
5. Click **Update** to save your changes. The integration will be redeployed.

## Uninstallation

#### Uninstall Integration

To deactivate the integration:

1. In the Datadog panel on the **Partner Connect** page, click on the configured integration.
2. Click **Delete connection**.
3. Confirm the deletion when prompted.

When deactivated, the integration status in the panel will show as **Inactive**.

After deactivating an integration, the metrics data will remain in Datadog according to your Datadog retention policy.

## Support

If you experience issues with configuring the integration, connecting to Datadog, or have questions about exported metrics, contact Starburst support. Visit [Starburst Support][3] to submit a support ticket or access support resources.


[1]: https://docs.datadoghq.com/account_management/api-app-keys/
[2]: https://docs.datadoghq.com/getting_started/site/
[3]: https://www.starburst.io/learn/support/