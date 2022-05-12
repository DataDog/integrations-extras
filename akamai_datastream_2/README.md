# Akamai DataStream 2

## Overview

Akamai DataStream 2 captures performance and security logs for your delivery properties to stream them in near real-time to Datadog to provide complete monitoring capability.

## Setup

### Installation

To install the pre-built Akamai DataStream 2 log pipeline and dashboard, visit the [integration tile][4] and click Install.

### Configuration

To configure Akamai DataStream 2 to send logs to Datadog, follow [these instructions on the
Akamai techdocs site][2] and make sure you set the log source to `akamai.datastream`.

### Validation

To validate that this integration is configured properly, [search for logs with the source `akamai.datastream`][3].

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
[4]: /account/settings#integrations/akamai-datastream-2