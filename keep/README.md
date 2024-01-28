# Agent Check: Keep

## Overview

Keep is an open-source AIOps alert management tool.

Keep acts as a single pane of glass and helps you turn 1000s into just 10s of meaningful alerts.

We use monitors data, logs and events to correlate alerts and reduce noise.

## Setup

### Installation

The Keep integration is installed using the (Integration Tile)[https://app.datadoghq.com/integrations/keephq] on your Datadog account, with OAuth2.

Users will:
1. Clicking on Keep's integration tile -> Install Integration
2. User will be redirected to Keep's platform for sign-in
3. User will be redirected back to Datadog to review and confirm the required scopes from their Datadog account
4. User will be redirected back to Keep's platform to see whether installation was successfully completed

## Uninstallation

- Once this integration has been uninstalled, any previous authorizations are revoked. 
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][3].
- Confirm that the `Webhooks` integration does not contain `keep-datadog-webhook-integration-UUID` on the [Integrations page][4].

### Validation

To validate Keep's integration is properly working, follow the next steps:
1. Navigate to the [Integrations page][4].
2. Search for `Webhooks`.
3. Click the `Webhooks` tile.
4. In the installed `Webhooks` list, look for a `Webhook` that starts with `keep-datadog-webhook-integration-UUID`.

## Data Collected

### Metrics

Keep sends metrics about the fatigueness of specific connected monitors. 

### Service Checks

The Keep integration does not include any service checks.

### Events

The Keep integration does not include any events.

## Troubleshooting

Need help? Contact [Keep's Support team][5].

[1]: https://app.datadoghq.com/integrations/keephq
[2]: /developers/authorization/oauth2_in_datadog/
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://app.datadoghq.com/integrations
[5]: mailto:rnd@keephq.dev?subject=[Datadog]%20OAuth%20Integration%20Support
[6]: https://www.keephq.dev/
