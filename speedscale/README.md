# Agent Check: Speedscale

## Overview

This integration publishes traffic replay results from [Speedscale][1] into Datadog. This lets you combine your observability data from Datadog with the results of a particular Speedscale replay to investigate the root cause of poor performance. Find and troubleshoot potential performance issues before they show up in production with the Speedscale Datadog integration.

## Setup

### Configuration

1. To use this integration you need a Datadog [API Key][2] so that events can be submitted into Datadog.

    A best practice is to save this value into an environment variable. Most likely you will store this environment variable in your continuous integration system, but when doing a one-off test you can access it in your terminal like so:

```
export DDOG_API_KEY=0
```

2. Gather the report ID of a specific report that you'd like to upload to Datadog. When working with continuous integration, get the report ID associated with your commit hash. Store this report ID in an environment variable:

```
export SPD_REPORT_ID=0
```

3. With the specific report ID and the Datadog API key, run the `speedctl` command to export that traffic replay report as a Datadog event.

```
speedctl export datadog report ${SPD_REPORT_ID} --apiKey ${DDOG_API_KEY}
✔ {"status":"ok",...}
```
### Validation

View the Datadog [Event Stream][2] to see your exported report.

## Data Collected

### Metrics

Speedscale does not include any metrics.

### Service Checks

Speedscale does not include any service checks.

### Events

The Speedscale integration sends events to your [Datadog Event Stream][3] when a traffic replay is complete to help you understand the impact this has on your metrics.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://docs.speedscale.com/reference/integrations/datadog/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/
[3]: https://app.datadoghq.com/event/stream
[4]: https://docs.datadoghq.com/help/
