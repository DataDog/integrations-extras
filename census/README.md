# Agent Check: Census

## Overview

Monitoring offers critical insights into maintaining and reacting to development processes. Often, developers use a whole suite of tools and products, each monitored independently. To ease the monitoring process, Census integrates with Datadog to provide developers the ability to monitor their Census workflows, along with their internal monitoring, all within Datadog.

The Census integration emits sync metrics and events to Datadog, which are embedded into a pre-configured dashboard. Further alerts and incident management can be configured to sit atop the dashboard.

## Requirements

A Census Platform tier (or higher) subscription is required to enable this integration.

## Setup

The Census integration comes with a pre-configured dashboard, which allows an overview of the syncs running on your Census workspace.

Setup with the following steps:

1. Login to your Census account
2. Navigate to the Census workspace that you wish to connect to your Datadog account.
3. Go to the workspace settings tab, and click on "Configure" on the Datadog tile.
4. Click on "Connect" to connect to your Datadog account via OAuth2.
5. Return to Datadog and enable the Census integration from the integration tile. This will import the pre-configured dashboard.

### Validation

Execute a sync on your Census workspace and await the corresponding metrics and events to emit to your Datadog account. The pre-configured dashboard will pick up these metrics and events. Events and metrics for a sync may take up to a couple of minutes to be transmitted to Datadog after sync completion.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this check.

### Service Checks

Census does not include any service checks.

### Events

This integration sends events to Datadog regarding sync completion events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-extras/blob/master/census/metadata.csv
[4]: https://docs.datadoghq.com/help/
