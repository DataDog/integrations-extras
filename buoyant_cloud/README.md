# Agent Check: Buoyant Cloud

## Overview

[Buoyant Cloud][1] provides fully managed Linkerd on your cluster to monitor the health of Linkerd and deployments. With this integration, you can monitor and be alerted on Linkerd's health, workload traffic, and rollout events.

## Setup

### Installation

You need to have an account at [Buoyant Cloud][1] to use this integration. You can also sign up for Buoyant Cloud in the Datadog Marketplace.

### Configuration

1. Log in to your Buoyant Cloud account.
2. Browse to the [Buoyant Cloud Settings][2] page, and click `Connect Datadog`.
3. Browse to the [Buoyant Cloud Notifications][3] page.
4. Click the kebab menu to edit a notification.
5. Go to the **Destinations** section and select your Datadog account to send all events matching the notification rule to Datadog.

### Validation

As Buoyant Cloud creates events, they appear in the Datadog [event explorer][4].

## Uninstallation

1. Browse to the [Buoyant Cloud Settings][2] page
2. Click the kebab menu to the right of your Datadog org
3. Click `Remove`

## Data Collected

### Events

Buoyant Cloud sends [events][4] to Datadog, including:

- Linkerd health alerts
- Linkerd configuration alerts
- Workload traffic alerts
- Workload rollouts
- Manual events

## Troubleshooting

Need help? Get support from the following sources:

- Browse the [Buoyant Cloud docs][5]
- Reach out in [Linkerd Slack][6]
- [Email the Buoyant Cloud team][7]
- [Contact Buoyant][1]

[1]: https://buoyant.io/cloud
[2]: https://buoyant.cloud/settings
[3]: https://buoyant.cloud/notifications
[4]: https://app.datadoghq.com/event/explorer
[5]: https://docs.buoyant.cloud
[6]: https://slack.linkerd.io
[7]: mailto:cloud@buoyant.io
