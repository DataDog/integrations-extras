# Agent Check: Speedscale

## Overview

This integration publishes the results from [Speedscale][1] into Datadog.

## Setup

### Configuration

In order to utilize the integration you need to capture the following from Datadog:

* [API Key][2] - An API key is required by the Datadog Agent to submit metrics and events to Datadog

A best practice is to save this into environment variables like so:

```
export DDOG_API_KEY=0
```

### Validation

Now you can select a specific report and export it using `speedctl`:

```
export SPD_REPORT_ID=0
speedctl export datadog report ${SPD_REPORT_ID} --apiKey ${DDOG_API_KEY}
✔ {"status":"ok",...}
```

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
