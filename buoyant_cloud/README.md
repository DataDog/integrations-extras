# Agent Check: Buoyant Cloud

## Overview

Get fully managed Linkerd right on your cluster. [Buoyant Cloud][1] manages the
CNCF graduated service mesh, so your team doesn't have to. Your engineers will
focus on building your business while Buoyant Cloud ensures that Linkerd is
always up and running. It automatically monitors the health of your Linkerd
deployment across all clusters, continually checks for potential failure
conditions or regressions, automates common operational tasks such as upgrades,
and provides an intuitive UI with an at-a-glance view of the state of your
service mesh. Best of all, Buoyant Cloud works with open source Linkerd, so
there's no lock-in or modification required.

This integration allows Datadog users to send Buoyant Cloud events and alerts to
Datadog.

## Setup

### Installation

Head over to [Buoyant Cloud][1] to request an account.

### Configuration

1. Log in to your Buoyant Cloud account.
2. Browse to the [Buoyant Cloud Settings][2] page, and click `Connect Datadog`.
3. Browse to the [Buoyant Cloud Notifications][3] page, edit some notifications,
   to associate them with Datadog.

### Validation

As Buoyant Cloud creates events, you should see them appear in Datadog, under
the `Events` section.

## Uninstallation

1. Browse to the [Buoyant Cloud Settings][2] page
2. Click the 3 dots to the right of your Datadog org
3. Click `Remove`
4. In the Datadog UI, remove any related Buoyant Cloud API keys from
   Organization Settings

## Data Collected

### Events

Buoyant Cloud sends events to Datadog.

## Troubleshooting

Need help? Get support from the following sources:

- Browse the [Buoyant Cloud docs][4]
- Reach out in [Linkerd Slack][5]
- [Email the Buoyant Cloud team][6]
- [Contact Buoyant][1]

[1]: https://buoyant.io/cloud
[2]: https://buoyant.cloud/settings
[3]: https://buoyant.cloud/notifications
[4]: https://docs.buoyant.cloud
[5]: https://slack.linkerd.io
[6]: mailto:cloud@buoyant.io
