# Agent Check: Buoyant Cloud

## Overview

[Buoyant Cloud][1] provides fully managed Linkerd on your cluster to monitor the health of Linkerd and deployments. With this integration, you can monitor and be alerted on Linkerd's health, workload traffic, rollout events, and metrics.

## Setup

### Installation

You need to have an account at [Buoyant Cloud][1] to use this integration. You can also sign up for Buoyant Cloud in the Datadog Marketplace.

### Configuration

1. Click the **Connect Accounts** button on the tile to complete the OAuth flow.
2. Browse to the [Buoyant Cloud Notifications][2] page.
3. Add or edit a rule under **Events** or **Metrics**.
4. Go to the **Destinations** section and select your Datadog account to send all events or metrics matching the notification rule to Datadog.

### Validation

As Buoyant Cloud creates events, they appear in the Datadog [event explorer][3]. Metrics appear in the Datadog [metrics explorer][4].

## Uninstallation

1. Browse to the [Buoyant Cloud Settings][5] page.
2. Click the kebab menu to the right of your Datadog org.
3. Click **Remove**.

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][6].

## Data Collected

### Events

Buoyant Cloud sends [events][3] to Datadog, including:

- Linkerd health alerts
- Linkerd configuration alerts
- Workload traffic alerts
- Workload rollouts
- Manual events

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

## Troubleshooting

Need help? Get support from the following sources:

- Browse the [Buoyant Cloud docs][8]
- Reach out in [Linkerd Slack][9]
- [Email the Buoyant Cloud team][10]

[1]: https://buoyant.io/cloud
[2]: https://buoyant.cloud/notifications
[3]: https://app.datadoghq.com/event/explorer
[4]: https://app.datadoghq.com/metric/explorer
[5]: https://buoyant.cloud/settings
[6]: https://app.datadoghq.com/organization-settings/api-keys?filter=Buoyant%20Cloud
[7]: https://github.com/DataDog/integrations-extras/blob/master/buoyant_cloud/metadata.csv
[8]: https://docs.buoyant.cloud
[9]: https://slack.linkerd.io
[10]: mailto:cloud@buoyant.io
