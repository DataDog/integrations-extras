# Upstash Integration

## Overview

The Upstash integration enables you to monitor the health and performance of your serverless databases directly within Datadog. By collecting key metrics such as active connections, command throughput, latency, and storage usage, this integration provides deep visibility into your data layer, helping you optimize performance and troubleshoot issues alongside the rest of your application telemetry.

## Setup

### Installation

Visit [Upstash][4] to sign up for free. Once registered, visit the [Upstash integration tile][5] in Datadog and install the integration. Once installed, navigate to the **Configure** tab and click **Connect Accounts**. This guides you through the Datadog OAuth flow to grant Upstash access to your database metrics.

## Uninstallation

To remove the Datadog integration from Upstash, navigate to the [Upstash integrations page][1] and click **Remove**. Additionally, uninstall this integration from Datadog by clicking the **Uninstall Integration** button on the [integration tile][5]. Once you uninstall this integration, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for `upstash` on the [API Keys management page][3].

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.
### Events

The Upstash integration does not include any events.

### Service Checks

The Upstash integration does not include any service checks.

## Dashboards

The Upstash integration includes two out-of-the-box dashboards to visualize your data:

1.  **Upstash Redis - Overview:** Provides a high-level view of your database health, including latency heatmaps, command throughput, storage breakdown, and connection statistics.
2.  **Upstash QStash - Overview:** Tracks message delivery statuses, workflow executions, and bandwidth consumption for your messaging pipeline.

## Support

Need help? Contact [Upstash support][7].

[1]: https://console.upstash.com/integration/datadog
[2]: https://upstash.com
[3]: /organization-settings/api-keys?filter=Upstash
[4]: https://upstash.com
[5]: /integrations/upstash
[6]: https://github.com/DataDog/integrations-extras/blob/master/upstash/metadata.csv
[7]: mailto:support@upstash.com