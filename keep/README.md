# Agent Check: Keep

## Overview

Keep is an open-source AIOps alert management tool.

Keep acts as a single pane of glass and helps you turn 1000s into just 10s of meaningful alerts.

We use monitors data, logs and events to correlate alerts and reduce noise.

## Setup

### Installation

The Keep integration is installed using the (Integration Tile)[https://app.datadoghq.com/integrations/keephq] on your Datadog account, with OAuth2.

Users will:
1. Be redirected to Keep's platform
2. Click on the Datadog tile to initate an OAuth flow
3. Review and confirm the required scopes in their Datadog account

## Uninstallation

- Once this integration has been uninstalled, any previous authorizations are revoked. 
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.
- Confirm that `Webhooks` integration does not contain `keep-datadog-webhook-integration-UUID` in the Datadog's (Integrations Page)[https://app.datadoghq.com/integrations].

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

Need help? Contact [Datadog Partners Support][3] team.

[1]: https://www.keephq.dev/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/

