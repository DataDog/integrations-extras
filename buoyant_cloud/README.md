# Agent Check: Buoyant Cloud

## Overview

[Buoyant Cloud][1] provides fully managed Linkerd on your cluster to monitor the health of Linkerd and deployments. With this integration, you can monitor and be alerted on Linkerd's health, workload traffic, and rollout events.

## Setup

### Installation

You need to have an account at [Buoyant Cloud][1] to use this integration. You can also sign up for Buoyant Cloud in the Datadog Marketplace.

### Configuration

1. Click the **Connect Accounts** button on the tile to complete the OAuth flow.
2. Browse to the [Buoyant Cloud Notifications][2] page.
3. Click the kebab menu to edit a notification.
4. Go to the **Destinations** section and select your Datadog account to send all events matching the notification rule to Datadog.

### Validation

As Buoyant Cloud creates events, they appear in the Datadog [event explorer][3].

## Uninstallation

1. Browse to the [Buoyant Cloud Settings][4] page.
2. Click the kebab menu to the right of your Datadog org.
3. Click **Remove**.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][5].

## Data Collected

### Events

Buoyant Cloud sends [events][3] to Datadog, including:

- Linkerd health alerts
- Linkerd configuration alerts
- Workload traffic alerts
- Workload rollouts
- Manual events

## Troubleshooting

Need help? Get support from the following sources:

- Browse the [Buoyant Cloud docs][6]
- Reach out in [Linkerd Slack][7]
- [Email the Buoyant Cloud team][8]

[1]: https://buoyant.io/cloud
[2]: https://buoyant.cloud/notifications
[3]: https://app.datadoghq.com/event/explorer
[4]: https://buoyant.cloud/settings
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: https://docs.buoyant.cloud
[7]: https://slack.linkerd.io
[8]: mailto:cloud@buoyant.io
