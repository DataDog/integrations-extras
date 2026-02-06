# Starburst Galaxy

## Overview

Starburst Galaxy is a fully-managed data lakehouse platform built on Trino that lets you query data across 50+ sources without moving or copying it. The platform delivers 6x faster SQL execution and 10x cost savings compared to traditional data warehouses, with built-in governance and support for Apache Iceberg, Delta Lake, and other open table formats.

The Starburst Galaxy integration with Datadog enables you to monitor and visualize your Starburst Galaxy cluster metrics directly in your Datadog account. With this integration you can monitor cluster health, query performance, and resource utilization in real time.

## Setup

1. In the Starburst Galaxy navigation menu, go to **Partner Connect > Observability**.
2. Find **Datadog** in the list of integrations and select the Datadog card.
3. Enter your Datadog **API key** and **Site**.
    - The API key is tied to your Datadog organization. To create an API key, see the [API and Application Keys documentation][1].
    - The Datadog site corresponds to your Datadog site URL. For more information, see [Getting Started with Datadog Sites][2].
4. Click  **Validate**  to test the connection. Starburst Galaxy verifies that the API key is valid and the selected Datadog site is accessible.
5. After validation succeeds, click  **Connect**. Metrics appear in your Datadog account within a few minutes.

Once you enable the integration, you should see a **Connected** status in the Datadog panel on Starburst Galaxy's **Partner Connect** page. If you encounter setup issues, contact Starburst support.

 ### Update Configuration

To rotate API keys or update the integration configuration:

1. In the Datadog panel on the **Partner Connect** page, click the configured integration.
2. Click **Edit connection**.
3. Update the **API key** and **Datadog Site** fields as needed.
4. Click **Validate** to test the new configuration.
5. Click **Update** to save your changes and redeploy the integration.

## Uninstallation

### In Starburst Galaxy

1. In the Datadog panel on the **Partner Connect** page, click on the configured integration.
2. Click **Delete connection**.
3. Confirm the deletion when prompted.

When deactivated, the integration status in the panel will show as **Inactive**.

### In Datadog

1. Navigate to the Starburst Galaxy integration tile.
2. Click **Uninstall** to remove the included dashboard.

## Support

Need help? Contact [Starburst Support][3].


[1]: https://docs.datadoghq.com/account_management/api-app-keys/
[2]: https://docs.datadoghq.com/getting_started/site/
[3]: https://www.starburst.io/learn/support/