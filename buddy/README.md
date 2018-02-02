## Overview

Enabling this integration will let you:

*   Send events about deployments to Datadog
*   Correlate deployment details with your Datadog metrics
*   Detect the sources of performance spikes

![](https://raw.githubusercontent.com/DataDog/integrations-extras/master/buddy/images/datadog-integration.png)

## Setup

1.  In your Datadog account settings go to [Integrations -> APIs](https://app.datadoghq.com/account/settings#api) and copy the **API Key** token
2.  [Sign in to your Buddy account](https://app.buddy.works/login) and go to the pipeline with the deployment action that you want to track
3.  Click the plus at the end of the pipeline and select **Datadog** in the **Notifications** section
4.  Enter the name of your Datadog account and paste the API key that you copied
5.  You can use [Buddy parameters](https://buddy.works/knowledge/deployments/what-parameters-buddy-use) to define the title of the event and content sent, for example:

```
Event title
<%text filter="h">
${execution.pipeline.name} execution #${execution.id}
</%text>

Content
<%text filter="h">
${execution.to_revision.revision} - ${execution.to_revision.message}
</%text>
```

6.  When ready, click **Add action** and run the pipeline. On every successful deployment, Buddy will send an event to Datadog:

![snapshot](https://raw.githubusercontent.com/DataDog/integrations-extras/master/buddy/images/snapshot.png)

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/buddy/metadata.csv) for a list of metrics provided by this integration.

### Events
All Buddy deployment events are sent to your [Datadog Even Stream](https://docs.datadoghq.com/graphing/event_stream/)

### Service Checks
The Buddy check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).
