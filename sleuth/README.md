## Overview

Sleuth is a deployment tracking tool that enables you to track software deployments through your complete DevOps stack. With a Datadog integration, Sleuth provides you with insightul, meaningful and actionable real-time data that enable you and your team to see, with clarity, the impact of the changes you make to your code.

## Setup

To add the Datadog integration:

1. Login to your [Sleuth account](https://app.sleuth.io/accounts/login/). 
1. Click **Integrations** in the sidebar.
2. Click the _Metric Trackers_ tab, then **enable** in the Datadog card.
3. Enter your Datadog API Key and Application Key in the corresponding fields. 
4. If your Datadog servers' are in the EU, enable the _My Datadog servers are in the EU_ checkbox. Leave this unchecked if you are unsure.  
5. Press **Save**. 

> Your Datadog API Key and Application Key can be found under **Integrations** &gt; **API**. Alternatively, you can click on the **generate** link in the Sleuth dialog box (as shown below), which takes you to the API/Applications Keys area in your Datadog console. 

![](/images/datadog-integration-api-key.png)

> Once the Datadog integration is successful, you will see the message **Datadog is connected** displayed. 

![](/images/datadog-integration.png)

### Installation

The Datadog Sleuth integration is installed exclusively from your Sleuth account. There are no settings or additional configuration that needs to be done from your Datadog account aside from providing your Datadog API and Application Keys in Sleuth. 

### Configuration

* Click the **Add metric** dropdown and select a Sleuth project that will process incoming Datadog application metrics. All projects within your Sleuth organization are displayed in the dropdown. 

![](/images/datadog-enabled-metric-pick.png)

> Integrations are made at the Sleuth organization level, and are available for all projects within that organization. Individual settings for an integration are made at the project level.  

That’s it—Sleuth will start displaying Datadog metrics in your deploys. Read [**Dashboard**](https://help.sleuth.io/dashboard) for more information on how metrics are communicated in Sleuth's deploy cards. 


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

The Datadog integration is disconnected and is no longer available to any projects within that organization. Any project-level modifications you made to the Datadog integration will be lost.
