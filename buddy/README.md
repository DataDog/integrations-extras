# Buddy Integration

## Overview

Enable this integration to:

- Send events about deployments to Datadog
- Correlate deployment details with your Datadog metrics
- Detect the sources of performance spikes

![datadog-integration][1]

## Setup

- In your Datadog account settings go to [Integrations -> APIs][2] and copy the **API Key** token

- [Sign in to your Buddy account][3] and go to the pipeline with the deployment action that you want to track

- Click the plus at the end of the pipeline and select **Datadog** in the **Notifications** section

- Enter the name of your Datadog account and paste the API key that you copied

- Use [Buddy parameters][4] to define the title of the event and content sent, for example:

```text
# Event title
${'${execution.pipeline.name} execution #${execution.id}'}

# Content
${'${execution.to_revision.revision} - ${execution.to_revision.message}'}
```

- When ready, click **Add action** and run the pipeline. On every successful deployment, Buddy sends an event to Datadog:

![snapshot][5]

## Data Collected

### Metrics

The Buddy check does not include any metrics.

### Events

All Buddy deployment events are sent to your [Datadog Event Stream][6]

### Service Checks

The Buddy check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][7].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/buddy/images/datadog-integration.png
[2]: https://app.datadoghq.com/organization-settings/api-keys
[3]: https://app.buddy.works/login
[4]: https://buddy.works/knowledge/deployments/what-parameters-buddy-use
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/buddy/images/snapshot.png
[6]: https://docs.datadoghq.com/events/
[7]: https://docs.datadoghq.com/help/
