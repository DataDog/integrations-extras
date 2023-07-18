# TaskCall

## Overview

TaskCall is a real-time incident response system that reduces system downtime by automating the response process. It continuously accepts feeds from monitoring tools to provide a comprehensive view of your system. It uses its on-call management and incident response mechanisms to assemble the right team and resolve incidents in the fastest possible time.

TaskCall’s integration allows Datadog users to bolster their operations by improving their incident awareness and simplifying the process in which they are handled. Incidents sync up bi-directionally between the two platforms. Once Datadog alerts are received in TaskCall, users will be able to systematically manage all incidents without being interrupted. Users will also benefit from improved impact visibility from dependency graphs and status dashboards. With better understanding of the state of your overall infrastructure efficient resolutions can be achieved.


## Key Features

- Correct on-call responders are notified as soon as an alert is received from Datadog.
- Repeating alerts are automatically silenced to avoid interrupting the on-call responders when they are already looking at the incident.
- The integration is bi-directional. Status and priority are synced up between Datadog and TaskCall.
- Incidents are automatically resolved in TaskCall when alert conditions are no longer present.
- The integration is available on all TaskCall subscription plans.


## Setup

The integration needs to be configured from both TaskCall and Datadog.

### In TaskCall

1. [Create a TaskCall account][1] if you do not already have one.
2. Go to Configurations > Services . Select the service you want to integrate with.
3. Once you are on the Service details page, go to the Integrations tab. Click on New Integration.
4. Give the integration a name.
5. From the integration types, select the top radio button indicating that you are trying to use a built-in integration.
6. From the list of built-in integrations, select Datadog.
7. Click Save. You will be directed to Datadog to authorize the integration.

### In Datadog

1. Go to Integrations > Integrations.
2. Find Webhooks and click on it.
3. Click on the New Webhook button.
4. Give it a name and paste the Integration Url you copied over from TaskCall.
5. Copy the [JSON payload][2] from the TaskCall Datadog Integration Guide and paste it in the Payload section.
6. Once the details have been entered, click Save.

Please refer to the [TaskCall Datadog Integration Guide][3] for more information.

### Uninstallation

- In TaskCall, delete the integration from Services > Integrations.
- In Datadog, delete the webhook you created.
- Once this integration has been uninstalled, any previous authorizations are revoked.
- Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.


## Support

[Contact TaskCall support][4] for any questions regarding the integration or the platform.


[1]: https://app.us.taskcallapp.com/register
[2]: https://docs.taskcallapp.com/integrations/v1/datadog-integration-guide#in-datadog
[3]: https://docs.taskcallapp.com/integrations/v1/datadog-integration-guide
[4]: https://www.taskcallapp.com/contact-us