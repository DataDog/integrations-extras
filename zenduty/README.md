## Overview

Use the Zenduty integration to send Datadog alerts to the right team, notify them as per on-call schedules, and help them remediate and resolve incidents with speed. Send notifications via e-mail, Slack, Microsoft Teams, SMS, Phone Calls, Android and iOS push messages.

Connect Zenduty with Datadog in order to:
- Trigger and resolve incidents, get alerts for them, and track issues from Datadog
- Deploy on-call schedules, escalation policies, incident playbooks, postmortems, and detailed analytics
- Use Alert Rules to custom route specific Datadog alerts to certain users or teams, write suppression rules, and automatically add notes, responders, and incident tasks

## Setup

### Zenduty
In [Zenduty][1], follow the steps below:

1. Go to **Teams** and click on the team you want to add the integration to.
 
2. Navigate to **Services**. Create a new service or select an existing one.
 
3. Go to **Integrations** and then **Add New Integration**. Give the integration a name, and select the application **Datadog** from the dropdown menu.

4. Go to **Configure** under your integrations, and copy the generated Datadog webhook URL.

### Datadog

5. From the sidebar, go to **Integrations**. Search for **Webhooks** from [this page][2], and click the add button.

6. Scroll down, click on the **+New** button in the Webhooks section. Fill in the name, the webhook URL copied from Zenduty, and paste the following JSON in the payload box:
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

7. Click on **Save**. The Datadog Zenduty integration setup is complete.

See the [Zenduty documentation][3] for more details and to get the most out of this integration.

**Note**: Mention ```@zenduty``` as a channel under **Notify your team** in the Datadog monitor's configuration to get alerts through Zenduty when Datadog incidents are created or resolved.

## Data Collected
### Metrics

The Zenduty integration does not include any metrics.

### Events

Triggered, acknowledged, and resolved events are displayed in Zenduty's dashboard.

### Service Checks

The Zenduty integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog Support][4].

[1]: https://www.zenduty.com
[2]: https://app.datadoghq.com/integrations/webhooks?search=webhook
[3]: https://docs.zenduty.com/docs/datadog
[4]: https://docs.datadoghq.com/help/
