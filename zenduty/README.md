## Overview

Use the Zenduty integration to send Datadog alerts to the right team, notify them as per on-call schedules, and help them remediate and resolve incidents with speed.

Connect Zenduty with Datadog in order to:
- Trigger and resolve incidents, get alerts for them and track issues from Datadog
- Deploy on-call schedules, escalation policies, incident playbooks, postmortems and detailed analytics
- Use Alert Rules to custom route specific Datadog alerts to certain users or teams, write suppression rules, auto add notes, responders and incident tasks

## Setup

### Zenduty:
Follow the following steps inside Zenduty:

1. Go to **'Teams'** and click on the team you want to add the integration to.
 
2. Navigate to **'Services'**, create a new service or select an existing one.
 
3. Go to **'Integrations'** and then **'Add New Integration'**. Give it a name and select the application **'Datadog'** from the dropdown menu.

4. Go to **'Configure'** under your integrations and copy the Datadog webhook URL generated.

### Datadog:

5. From the sidebar, go to **Integrations**. Search for **'Webhooks'** from this page, and click the add button.

6. Scroll down, click on the **'+New'** button in the Webhooks section. Fill in the name, the webhook URL copied from Zenduty and paste the following JSON in the payload box:
```
{
"alert_id": "$ALERT_ID",
"hostname":"$HOSTNAME",
"date_posix":"$DATE_POSIX",
"aggreg_key":"$AGGREG_KEY",
"title": "$EVENT_TITLE",
"alert_status":"$ALERT_STATUS",
"alert_transition":"$ALERT_TRANSITION",
"link":"$LINK",
"event_msg":"$TEXT_ONLY_MSG"
}
```

7. Click on **'Save'**. The Datadog-Zenduty integration is complete.

    See the [Zenduty documentation][1] for more details and to get the most out of this integration.

**Note**: Mention ```@zenduty``` as a channel under **Notify your team** in the Datadog monitor's configuration to get alerts through Zenduty when Datadog incidents are created or resolved.

## Data Collected
### Metrics

Zenduty integration does not include any metrics.

### Events

Triggered, acknowledged and resolved events are displayed in Zenduty's dashboard

### Service Checks

Zenduty integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog Support][2].

[1]: https://docs.zenduty.com/docs/datadog
[2]: https://docs.datadoghq.com/help/
