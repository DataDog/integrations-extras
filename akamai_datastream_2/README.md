# Akamai DataStream 2

## Overview

Akamai DataStream 2 captures performance, security, and CDN health logs for your properties on the Akamai Intelligent Edge Platform. This integration streams the data in near real-time to Datadog.

You can use Akamai DataStream 2 logs to gain insight into long term trends, resolve performance and security issues, and monitor high-throughput data delivery streams. See the [DataStream 2 documentation][6] for further details and use cases.

## Setup

### Installation

Click **Install Integration** to enable a preset dashboard for viewing Akamai DataStream 2 logs and metrics.

### Configuration

To configure Akamai DataStream 2 to send logs to Datadog, follow [these instructions on the
Akamai techdocs site][2], make sure to set the log source to `akamai.datastream` and the log format to `JSON`.

Ensure that you have the Datadog Site selector on the right of the page set to your [Datadog Site][4], and copy the logs endpoint URL below:  

`https://{{< region-param key="http_endpoint" code="true" >}}/v1/input`

### Validation

To validate that this integration is configured properly, [search for logs with the source `akamai.datastream`][3]. You may have to wait a few minutes after configuring the datastream in Akamai before logs are visible in Datadog.

## Data Collected

### Metrics

Akamai DataStream 2 does not include any metrics.

### Service Checks

Akamai DataStream 2 does not include any service checks.

### Events

Akamai DataStream 2 does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].

## Further Reading

Additional helpful documentation, links, and articles:

- [Monitor Akamai Datastream 2 with Datadog][4]

[1]: https://docs.datadoghq.com/help/
[2]: https://techdocs.akamai.com/datastream2/docs/stream-datadog
[3]: https://app.datadoghq.com/logs?query=source%3Aakamai.datastream
[4]: https://www.datadoghq.com/blog/monitor-akamai-datastream2/
[5]: https://docs.datadoghq.com/getting_started/site/
[6]: https://techdocs.akamai.com/datastream2/docs
