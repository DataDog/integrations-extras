# Upstash Integration

## Overview

Upstash is a serverless data platform that unifies Redis, Vector, QStash, and Workflow tools for modern, high-performance applications. The Upstash integration enables you to monitor the health and performance of your serverless resources directly within Datadog. By collecting key metrics such as database latency, active connections, and throughput, alongside QStash message delivery states, workflow runs, and dead letter queues (DLQ), this integration enhances your observability by consolidating your data layer monitoring with your broader application telemetry, helping you optimize performance and troubleshoot issues faster.

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

## Support

Need help? Contact [Upstash support][7].

[1]: https://console.upstash.com/integration/datadog
[2]: https://upstash.com
[3]: /organization-settings/api-keys?filter=Upstash
[4]: https://upstash.com
[5]: /integrations/upstash
[6]: https://github.com/DataDog/integrations-extras/blob/master/upstash/metadata.csv
[7]: mailto:support@upstash.com