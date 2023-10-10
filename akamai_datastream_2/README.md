# Akamai DataStream 2

## Overview

Akamai DataStream 2 captures performance and security logs for your delivery properties. This integration streams the data in near real-time to Datadog for complete monitoring.

## Setup

### Installation

Click **Install Integration** to enable a preset dashboard for viewing Akamai DataStream 2 logs and metrics.

### Configuration

To configure Akamai DataStream 2 to send logs to Datadog, follow [these instructions on the
Akamai techdocs site][2], make sure to set the log source to `akamai.datastream` and the log format to `JSON`.

Ensure the logs are being sent to the right datacenter by configuring the correct URL:  
US1 `http-intake.logs.datadoghq.com/v1/input`  
US3 `http-intake.logs.us3.datadoghq.com/v1/input`  
US5 `http-intake.logs.us5.datadoghq.com/v1/input`  
EU `http-intake.logs.datadoghq.eu/v1/input`  
AP1 `http-intake.logs.ap1.datadoghq.com/v1/input`  
US1-FED `http-intake.logs.ddog-gov.com/v1/input`  

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
