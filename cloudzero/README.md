# Agent Check: CloudZero

## Overview

This check monitors [CloudZero][1].

## Setup

### Installation

To install the CloudZero check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/python/)
 on any machine.

2. Run `ddev release build cloudzero` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/cloudzero/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. <List of steps to setup this Integration>

### Validation

<Steps to validate integration is functioning as expected>

## Data Collected

### Metrics

CloudZero does not include any metrics.

### Service Checks

CloudZero does not include any service checks.

### Events

CloudZero does not include any events.

### Uninstallation
- Once this integration has been uninstalled, any previous authorizations are revoked.
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page](https://app.datadoghq.com/organization-settings/api-keys?_gl=1*pc1ehd*_gcl_aw*R0NMLjE2ODY4NTM2MzIuQ2owS0NRanc3YXFrQmhEUEFSSXNBS0dhMG9Ma2Y4VWlPcmo2SHhoVkpFbE1yb0ZWdW1iSHVDVmhwYzdPb1psWXdHdy12NG9qV21SWjNmY2FBczJiRUFMd193Y0I.*_gcl_au*MTUyMDYzMDY1Mi4xNjgzNzI2OTI1*_ga*MTEyODQ5ODQyNy4xNjgzNzI2OTI1*_ga_KN80RDFSQK*MTY4OTA4NjY3NC4xNS4xLjE2ODkwODY5MzkuMC4wLjA.*_fplc*SG9HMWQ2YUNXT2JYJTJGSzJQMXo5RGRMcTRnQzUyUUt6SWdENkRPTU5yc3ZwNjhRb1NZUWpTMHR2RnZmZGxFSEpvTlZpRGUzSGJvaFpnR21KNDJCbExTZzhUUUlrMXlIdXYlMkZzUWZtRyUyQndQR1RuY0I1WGJZN3dmbngxT2lzdnNnJTNEJTNE).

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/help/

