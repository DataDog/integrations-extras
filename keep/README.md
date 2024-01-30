# Agent Check: Keep

## Overview

Keep is an open-source AIOps alert management and automation platform, which offers a platform for consolidating, automating, and reducing noise across various parts of your observability stack. Keep integration with Datadog harnesses the strengths of both platforms, providing a unified and efficient approach to alert management and event correlation.

Keep uses Datadog monitors data, logs and events to correlate alerts and reduce noise.

Key features of this integration include:

- Centralized Alert Management: Consolidate all your Datadog alerts into Keep’s single pane of glass, offering streamlined control and visibility.
- Reduced Alert Noise: Minimize alert fatigue by filtering and prioritizing Datadog alerts, ensuring your team addresses the most critical alerts promptly.
- Comprehensive Analysis: Leverage Keep’s analytical tools to derive insights from Datadog alerts, aiding in proactive decision-making and trend analysis.

This integration is ideal for teams seeking to enhance their alert capabilities, improve operational efficiency, and make data-driven decisions with **reduced noise and distraction**.

For more information about (Keep)[6], see (Keep's documentation)[8].



## Setup

### Installation

The Keep integration is installed using the (Integration Tile)[https://app.datadoghq.com/integrations/keephq] on your Datadog account, with OAuth2.

Users will:
1. Clicking on Keep's integration tile -> Install Integration
2. User will be redirected to Keep's platform for sign-in
3. User will be redirected back to Datadog to review and confirm the required scopes from their Datadog account
4. User will be redirected back to Keep's platform to see whether installation was successfully completed

Once installed successfully, Keep will automatically create a new `Webhook` integration in your Datadog, and will modify your monitors to send alerts.

## Uninstallation

- Once this integration has been uninstalled, any previous authorizations are revoked. 
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][3].
- Confirm that the `Webhooks` integration does not contain `keep-datadog-webhook-integration-UUID` on the [Integration page][7].

### Validation

To validate Keep's integration is properly working, follow the next steps:
1. Navigate to the [Webhook Integration page][7].
2. In the installed `Webhooks` list, look for a `Webhook` that starts with `keep-datadog-webhook-integration-UUID`.

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
[7]: https://app.datadoghq.com/integrations/webhooks
[8]: https://docs.keephq.dev/providers/documentation/datadog-provider
