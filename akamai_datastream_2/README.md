# Akamai DataStream 2

## Overview

Akamai DataStream 2 captures performance and security logs for your delivery properties to stream them in near real-time to Datadog to provide complete monitoring capability.

## Setup

### Installation

Click "Install Integration" to enable a preset dashboard for viewing Akamai DataStream 2 logs and metrics.

### Configuration

To configure Akamai DataStream 2 to send logs to Datadog, follow [these instructions on the
Akamai techdocs site][2] and make sure you set the log source to `akamai.datastream`.

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

[1]: https://docs.datadoghq.com/help/
[2]: https://techdocs.akamai.com/datastream2/docs/stream-datadog
[3]: /logs?query=source%3Aakamai.datastream
