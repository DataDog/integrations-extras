# Agent Check: PerimeterX

## Overview

This integration allows [PerimeterX][2] customers to forward their PerimeterX related logs and events to Datadog.

## Setup

All configuration is done by PerimeterX. See the [PerimeterX documentation][3] regarding third party integrations.

### Installation

No installation is required on your host.

### Configuration

1. Generate a new Integration API Key in your [Datadog portal][4].
2. Open a support ticket with [PerimeterX Support][5] and request the Datadog log export integration. Support needs the following information:
   - Your Datadog Integration API Key
   - Whether you want to send metrics and/or logs
   - The PerimeterX Application ID(s) that should be forwarded to Datadog

### Validation

Once PerimeterX Support has confirmed the Datadog integration is complete, perform the following steps to confirm the integration is working as expected:

1. Login to your Datadog portal.
2. Navigate to Logs -> Search
3. Perform a search with a query filter of "Source:perimeterx"
4. Confirm you are receiving logs from PerimeterX (it may take a few minutes before logs start appearing).

## Data Collected

### Metrics

PerimeterX does not include metrics for [requests][6].

### Service Checks

PerimeterX does not include any service checks.

### Events

PerimeterX does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
[2]: https://www.perimeterx.com/
[3]: https://docs.perimeterx.com/pxconsole/docs/data-integration-to-third-party-apps
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: mailto:support@perimeterx.com
[6]: https://docs.perimeterx.com/pxconsole/docs/data-schema-metrics
