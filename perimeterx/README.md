# Agent Check: Perimeterx

## Overview

This integration allows [PerimeterX][https://www.perimeterx.com/] customers to forward their PerimeterX related logs and events into Datadog.

## Setup

All configuration is done by PerimeterX. Please visit the [PerimeterX documentation](https://docs.perimeterx.com/pxconsole/docs/data-integration-to-third-party-apps) regarding third party integrations.

### Installation

No installation is required on your host.

### Configuration

1. Generate a new Integration API Key in your [Datadog portal](https://app.datadoghq.com/account/settings#api)
2. Open a support ticket with PerimeterX Support and request the Datadog log export integration. Support will need the following items:
   - Datadog Integration API Key
   - Whether you want to send metrics and/or logs
   - PerimeterX Application ID(s) that should be forwarded to Datadog

### Validation

Once PerimeterX Support has confirmed the Datadog integration is complete, you can perform the following steps to confirm the integration is working as expected:

1. Login to your Datadog portal.
2. Navigate to Logs -> Search
3. Perform a search with a query filter of "Source:perimeterx"
4. Confirm you are receiving logs from PerimeterX (this may take a few minutes before logs start appearing).

## Data Collected

### Metrics

PerimeterX does not includes metrics for [requests](https://docs.perimeterx.com/pxconsole/docs/data-schema-metrics).

### Service Checks

PerimeterX does not include any service checks.

### Events

PerimeterX does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
