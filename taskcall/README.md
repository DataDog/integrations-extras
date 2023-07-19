# TaskCall

## Overview

TaskCall is a real-time incident response system that reduces system downtime by automating the response process. It continuously accepts feeds from monitoring tools to provide a comprehensive view of your system. It uses its on-call management and incident response mechanisms to assemble the right team and resolve incidents in the fastest possible time.

TaskCall's integration allows Datadog users to bolster their operations by improving their incident awareness and simplifying the process in which they are handled. Incidents sync up bi-directionally between the two platforms. Once Datadog alerts are received in TaskCall, users will be able to systematically manage all incidents without being interrupted. Users will also benefit from improved impact visibility from dependency graphs and status dashboards. With a better understanding of the state of your overall infrastructure, efficient resolutions can be achieved.


## Key Features

- Correct on-call responders are notified as soon as an alert is received from Datadog.
- Repeating alerts are automatically silenced to avoid interrupting the on-call responders when they are already looking at the incident.
- The integration is bi-directional. Status and priority are synced up between Datadog and TaskCall.
- Incidents are automatically resolved in TaskCall when alert conditions are no longer present.
- This integration is available on all TaskCall subscription plans.


## Setup

The integration needs to be configured from both TaskCall and Datadog.

### Install TaskCall App in Datadog

1. [Create a TaskCall account][1] if you do not already have one.
2. **In Datadog**: Navigate to the [TaskCall integration tile][6].
3. On the TaskCall integration tile, go to the **Configure** tab and click **Connect Accounts**. You will be redirected to TaskCall.
4. **In TaskCall**: Give the integration a **name** and select the **service** you want the integration to be on.

![TaskCall Authorization][5]

5. Click **Integrate**. You will be redirected to a Datadog authorization page.
6. Authorize the integration, ensuring that you have the correct permissions to do so.
7. Once you authorize the integration you will be redirected to TaskCall.
8. **In TaskCall**: Copy the **Integration Url** that is issued for the integration. You will need this to set up the webhook in Datadog.

### Create Webhook in Datadog

1. Go to Integrations > Integrations.
2. Find **Webhooks** and click on it.
3. Click on the **New Webhook** button.
4. Give it a name and paste the **Integration Url** you copied over from TaskCall.
5. Copy the following [JSON payload][2] and paste it in the Payload section.
```json
{
     "body": "$EVENT_MSG",
     "last_updated": "$LAST_UPDATED",
     "event_type": "$EVENT_TYPE",
     "title": "$EVENT_TITLE",
     "date": "$DATE",
     "org": {
         "id": "$ORG_ID",
         "name": "$ORG_NAME"
     },
     "id": "$ID",
     "aggreg_key": "$AGGREG_KEY",
     "alert": {
         "cycle_key": "$ALERT_CYCLE_KEY",
         "id": "$ALERT_ID",
         "metric": "$ALERT_METRIC",
         "scope": "$ALERT_SCOPE",
         "status": "$ALERT_STATUS",
         "title": "$ALERT_TITLE",
         "transition": "$ALERT_TRANSITION",
         "type": "$ALERT_TYPE",
         "query": "$ALERT_QUERY"
     },
     "user": "$USER",
     "username": "$USERNAME",
     "priority": "$PRIORITY",
     "text_msg": "$TEXT_ONLY_MSG",
     "snapshot": "$SNAPSHOT",
     "link": "$LINK",
     "hostname": "$HOSTNAME",
     "incident_uuid": "$INCIDENT_UUID",
     "incident_public_id": "$INCIDENT_PUBLIC_ID",
     "incident_title": "$INCIDENT_TITLE",
     "incident_url": "$INCIDENT_URL",
     "incident_msg": "$INCIDENT_MSG",
     "incident_severity": "$INCIDENT_SEVERITY",
     "security_rule_id": "$SECURITY_RULE_ID",
     "security_rule_name": "$SECURITY_RULE_NAME",
     "security_signal_severity": "$SECURITY_SIGNAL_SEVERITY",
     "security_signal_title": "$SECURITY_SIGNAL_TITLE",
     "security_signal_msg": "$SECURITY_SIGNAL_MSG",
     "security_rule_query": "$SECURITY_RULE_QUERY",
     "security_rule_type": "$SECURITY_RULE_TYPE",
     "tags": "$TAGS"
}
```
6. Once the details have been entered, click Save.

Please refer to the [TaskCall Datadog Integration Guide][3] for more information.

## Uninstallation

- In TaskCall, delete the integration from Services > Integrations.
- Navigate to the [TaskCall integration tile][6] in Datadog and uninstall it. You must also delete the webhook you created to send notifications to TaskCall.
- Once this integration has been uninstalled, any previous authorizations are revoked.


## Support

[Contact TaskCall support][4] for any questions regarding the integration or the platform.


[1]: https://app.us.taskcallapp.com/register
[2]: https://docs.taskcallapp.com/integrations/v1/datadog-integration-guide#in-datadog
[3]: https://docs.taskcallapp.com/integrations/v1/datadog-integration-guide
[4]: https://www.taskcallapp.com/contact-us
[5]: https://taskcallapp.com/images/vendors/datadog/DatadogTaskCallAuthorization.png
[6]: https://app.datadoghq.com/integrations/taskcall