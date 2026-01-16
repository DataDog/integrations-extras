# Upstash Integration

## Overview

[Upstash][2] is a serverless database platform that offers various data solutions, including **Redis**, **QStash**, and **Vector** databases.

Key features of all Upstash products include:

* **Serverless Architecture:** No need to manage or provision servers.
* **Scale to Zero:** Pay only for actual usage. Resources scale down to minimal levels during periods of low or no activity.
* **REST API:** Ideal for environments that do not allow TCP connections, such as Cloudflare Workers.
* **Global Database:** Low latency access worldwide.
* **Per-request Pricing:** A model perfectly suited for edge and serverless functions.

These features make Upstash a powerful fit for serverless and edge computing environments, allowing developers to focus on building applications rather than resource management.

---

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
