## Overview

Enabling this integration will let you:

*   Send events about deployments to Datadog
*   Correlate deployment details with your Datadog metrics
*   Detect the sources of performance spikes

![](https://raw.githubusercontent.com/DataDog/integrations-extras/master/buddy/images/datadog-integration.png)

## Setup
## Configuration

1.  In your Datadog account settings go to [Integrations -> APIs](https://app.datadoghq.com/account/settings#api) and copy the **API Key** token
2.  [Sign in to your Buddy account](https://app.buddy.works/login) and go to the pipeline with the deployment action that you want to track
3.  Click the plus at the end of the pipeline and select **Datadog** in the **Notifications** section
4.  Enter the name of your Datadog account and paste the API key that you copied
5.  You can use [Buddy parameters](https://buddy.works/knowledge/deployments/what-parameters-buddy-use) to define the title of the event and content sent, for example:

```
# Event title
${execution.pipeline.name} execution #${execution.id}

# Content
${execution.to_revision.revision} - ${execution.to_revision.message}`
```              

6.  When ready, click **Add action** and run the pipeline. On every successful deployment, Buddy will send an event to Datadog:

![](https://raw.githubusercontent.com/DataDog/integrations-extras/master/buddy/images/snapshot.png)
