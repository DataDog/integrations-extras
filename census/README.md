# Agent Check: Census

## Overview

[Census][1] is the leading reverse ETL platform that turns your data warehouse into a hub for marketing and business operations, empowering everyone with trustworthy and actionable data. Hundreds of companies like Canva, Figma, Loom, and Notion use Census to publish analytics directly into all their applications in real time.

Monitoring offers critical insights into maintaining and reacting to development processes. Often, developers use a whole suite of tools and products, each monitored independently. To ease the monitoring process, Census integrates with Datadog to provide developers the ability to monitor their Census workflows, along with their internal monitoring, all within Datadog. The integration comes with a pre-configured dashboard, providing a birds-eye view of your Census syncs.

The Census integration emits [metrics][3] and events regarding syncs setup within Census.

## Requirements

A Census Platform tier (or higher) subscription is required to enable this integration.

## Setup

1. Login to your [Census account][2]
2. Navigate to the Census workspace that you wish to connect to your Datadog account.
3. Go to the workspace settings tab, and click on "Configure" on the Datadog tile.
4. Click on "Connect" to connect to your Datadog account via OAuth2.
5. Return to Datadog and access the out-of-box dashboard included with this integration.

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

Need help? Contact [Datadog support][4].

[1]: https://www.getcensus.com/
[2]: https://app.getcensus.com/
[3]: https://github.com/DataDog/integrations-extras/blob/master/census/metadata.csv
[4]: https://docs.datadoghq.com/help/
