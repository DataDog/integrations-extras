# Logz.io

## Overview

Logz.io is a unified SaaS platform that collects and analyzes logs, metrics, and traces. The platform includes AI features to improve troubleshooting, reduce response time, and help you manage costs.

This integration allows you to

- View real-time Logz.io alerts in Datadog

![import_alert_from_logz][1]

- Incorporate alert events into a dashboard to identify correlations with metrics

![dashboard][2]

## Setup

### Installation

Import your alerts into Datadog with the following steps:

1. Use a [Datadog API key][3] to create a new alert endpoint in Logz.io.
2. Create a new alert in Logz.io for a specific query.

For a more detailed setup description, see [Log Correlation with Logz.io and Datadog][4].

## Data Collected

### Metrics

The Logz.io check does not include any metrics.

### Events

The Logz.io check does not include any events.

### Service Checks

The Logz.io check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/logzio/images/import_alert_from_logz.jpg
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/logzio/images/dashboard.png
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: http://logz.io/blog/log-correlation-datadog
[5]: https://docs.datadoghq.com/help/
