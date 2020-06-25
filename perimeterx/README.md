# Agent Check: Perimeterx

## Overview

This check monitors [perimeterx][1].

## Setup

All configuration is done by PerimeterX. Please visit the [PerimeterX Documentation](https://docs.perimeterx.com/pxconsole/docs/data-integration-to-third-party-apps) regarding third party integrations.

### Installation

No installation is required on your host

### Configuration

1. Generate a new Integration API Key in your [Data Dog portal](https://app.datadoghq.com/account/settings#api)
2, Open a support ticket with PerimeterX Support and request Data Dog log export integration. Support will need the following items:
   - Data Dog Integration API Key
   - Whether you want to send metrics and/or logs
   - PerimeterX Application ID(s) that should be forwarded to Data Dog

### Validation

## Data Collected

### Metrics

perimeterx does not includes metrics for [requests](https://docs.perimeterx.com/pxconsole/docs/data-schema-metrics)

### Service Checks

perimeterx does not include any service checks.

### Events

perimeterx does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][1].

[1]: https://docs.datadoghq.com/help/
