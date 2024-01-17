# Agent Check: Keep

## Overview

Keep is an open-source AIOps alert management tool.

## Setup

### Installation

The Keep integration is installed using the (Integration Tile)[https://app.datadoghq.com/integrations/keephq] on your Datadog account, with OAuth2.

### Validation

To validate Keep's integration is properly working, follow the next steps:
1. Head over to Datadog's (Integrations Page)[https://app.datadoghq.com/integrations]
2. Search for `Webhooks`
3. Click the `Webhooks` tile
4. In the installed `Webhooks` list, look for a `Webhook` that starts with `keep-datadog-webhook-integration-UUID`

## Data Collected

### Metrics

Keep sends metrics about the fatigueness of specific connected monitors. 

### Service Checks

Keep does not include any service checks.

### Events

Keep does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://www.keephq.dev/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/

