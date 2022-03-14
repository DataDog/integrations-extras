# Agent Check: Speedscale

## Overview

This integration publishes traffic replay results from [Speedscale][1] into Datadog. This lets you combine your observability data from Datadog with the results of a particular replay to drill-down into the root cause of poor performance. Find and troubleshoot potential performance issues before they show up in production with a combination of Speedscale and Datadog.

## Setup

### Configuration

In order to utilize the integration you need to capture the following from Datadog:

* [API Key][2] - An API key is required by the Datadog Agent to submit metrics and events to Datadog

A best practice is to save this into an environment variable. Most likely you will store this environment variable in your continuous integration system, but when doing a one-off test you can access in your terminal like so:

```
export DDOG_API_KEY=0
```

Gather the report id of a specific report that you want to upload into Datadog. When working with continuous integration you should be able to get the report id associated with your commit hash. Store this report id in an environment variable:

```
export SPD_REPORT_ID=0
```

Now with the specific report id and the Datadog API key, you run the `speedctl` CLI to export that traffic replay report as a Datadog event.

```
speedctl export datadog report ${SPD_REPORT_ID} --apiKey ${DDOG_API_KEY}
✔ {"status":"ok",...}
```
### Validation

After you have exported the report, you should see it in the Datadog [Event Stream][2].

## Data Collected

### Metrics

Speedscale does not include any metrics.

### Service Checks

Speedscale does not include any service checks.

### Events

The Speedscale integration sends events to your [Datadog Event Stream][3] when a traffic replay is complete to understand the impact this has on your metrics.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://docs.speedscale.com/reference/integrations/datadog/
[2]: https://docs.datadoghq.com/account_management/api-app-keys/
[3]: https://app.datadoghq.com/event/stream
[4]: https://docs.datadoghq.com/help/
