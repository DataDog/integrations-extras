## Overview

Sleuth is a deployment tracking tool that enables you to track software deployments through your complete DevOps stack. With a Datadog integration, Sleuth provides you with insightful, meaningful, and actionable real-time data that enable you and your team to see, with clarity, the impact of the changes you make to your code.

## Setup

To add the Datadog integration:

1. Login to your [Sleuth account][1].
2. Click **Integrations** in the sidebar.
3. Click the _Metric Trackers_ tab, then **enable** in the Datadog card.
4. Enter your Datadog API Key and Application Key in the corresponding fields.
5. If your Datadog servers' are in the EU, enable the _My Datadog servers are in the EU_ checkbox. Leave this unchecked if you are unsure.
6. Press **Save**.

> Your Datadog API Key and Application Key can be found under **Integrations** &gt; **API**. Alternatively, you can click on the **generate** link in the Sleuth dialog box (as shown below), which takes you to the API/Applications Keys area in your Datadog console.

![][2]

> Once the Datadog integration installation is successful, the message **Datadog is connected** displayed.

![][3]

### Installation

The Datadog Sleuth integration is installed exclusively from your Sleuth account. There are no settings or additional configuration needed from your Datadog account except to provide your Datadog API and application keys in Sleuth.

### Configuration

- Click the **Add metric** dropdown and select a Sleuth project to process incoming Datadog metrics. All projects within your Sleuth organization are displayed in the dropdown.

![][4]

> Integrations are made at the Sleuth organization level, and are available for all projects within that organization. Individual settings for an integration are made at the project level.

Once configuration is complete, Sleuth displays Datadog metrics in your deploys. Read [**Dashboard**][5] for more information on how metrics are communicated in Sleuth's deploy cards.


## Data Collected

### Metrics

The Sleuth integration does not include any metrics.

### Service Checks

The Sleuth integration does not include any service checks.

### Events

The Sleuth integration does not include any events.

## Removing

1. In your Sleuth Dashboard, click **Integrations** in the left sidebar, then on **Metric Trackers**.
2. In the Datadog integration card, click **disable**.

The Datadog integration is disconnected and is no longer available to any projects within that organization. Any project-level modifications you made to the Datadog integration is lost.

## Troubleshooting

Need help? Contact the [maintainer][6] of this integration.

[1]: https://app.sleuth.io/accounts/login/
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sleuth/images/datadog-integration-api-key.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sleuth/images/datadog-integration.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sleuth/images/datadog-enabled-metric-pick.png
[5]: https://help.sleuth.io/dashboard
[6]: https://github.com/DataDog/integrations-extras/blob/master/sleuth/manifest.json
