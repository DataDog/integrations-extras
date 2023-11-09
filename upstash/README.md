# Upstash

## Overview

Upstash is a serverless data provider enabling Redis®, Kafka, and messaging/scheduling solutions for a diverse range of applications that provides speed, simplicity, and a seamless developer experience. Upstash utilizes the Redis and Kafka APIs, and is designed for:

* Serverless functions (AWS Lambda)
* Cloudflare Workers
* Fastly Compute@Edge
* Next.js Edge, Remix, and more
* Client-side web or mobile applications
* AI development
* WebAssembly and other environments where HTTP is preferred over TCP connections

Upstash can push calculated metrics into Datadog to:

* Through Upstash integration you will be able to add Upstash metrics to your centralized monitoring stack and gain a more comprehensive view

* Upstash will achieve this by submitting in the following metrics:
    * Hit/Miss Rate
    * Read/Write Latency (p99)
    * Keyspace
    * Number of Connections
    * Bandwidth
    * Total Data Size
    * Throughput

## Setup

### Installation

Visit [Upstash][4] to sign up for free. Once registered, visit the [Upstash integration tile][5] in Datadog and install the integration. Once installed, navigate to the **Configure** tab and click **Connect Accounts**. This will guide you through the Datadog OAuth flow to grant Upstash access to your database metrics.

### Uninstallation

To remove the Datadog integration from Upstash, navigate to the [Upstash integrations page][1] and click **Remove**. Additionally, uninstall this integration from Datadog by clicking the **Uninstall Integration** button on the [integration tile][5]. Once you uninstall this integration, any previous authorizations are revoked.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for `upstash` on the [API Keys management page][3].


Need help? Contact [Upstash support][7].

[1]: https://console.upstash.com/integration/datadog
[2]: https://upstash.com
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=Upstash
[4]: https://upstash.com
[5]: https://app.datadoghq.com/integrations/upstash
[6]: https://github.com/DataDog/integrations-extras/blob/master/upstash/metadata.csv
[7]: mailto:support@upstash.com