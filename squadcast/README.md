## Overview

Use the Datadog-Squadcast integration to send Datadog alerts to Squadcast and seamlessly take actions on these alerts within the Squadcast platform.

Connect Squadcast to Datadog in order to:
- Trigger and resolve incidents from Datadog
- Tackle incidents and set up escalation policies as they occur
- Set up a daily reminder of who is on-call

## Setup

**Note**: Only the users with Account Owner or Admin privileges can configure services on Squadcast.
At least one Escalation Policy must be configured before you can add a service.

### Squadcast

Follow these steps in Squadcast:

1. Open the **Services** page from the sidebar.

2. Choose an existing service, or create a new service by clicking on **Add Service**.

3. Click on **Alert Sources** and select **Datadog** from the drop down.

5. Copy the **Datadog Webhook URL** shown and click **Done**.

### Datadog

Follow these steps in Datadog:

1. Open the **Integrations** page from the sidebar.

2. Use the search bar to search for "webhooks".

3. Once the **Webhooks** tile appears, hover and click on "Install".

4. Navigate to the **Configuration** tab and scroll to the bottom of the page.

5. (a) Give the Webhook a name in the Name field.

   (b) Paste the **Datadog Webhook URL** provided by Squadcast in the URL field.

   (c) Copy-paste the following JSON in the text box under the **Payload** section.
    
![Squadcast Webhook][2]

```json
    {
        "alertId": "$ALERT_ID",
        "eventMessage": "$TEXT_ONLY_MSG",
        "title": "$EVENT_TITLE",
        "url": "$LINK",
        "alertTransition": "Triggered",
        "hostname": "$HOSTNAME",
        "orgName":"$ORG_NAME",
        "priority":"$PRIORITY",
        "snapshot": "$SNAPSHOT",
        "alertQuery": "$ALERT_QUERY",
        "alertScope": "$ALERT_SCOPE",
        "alertStatus": "$ALERT_STATUS",
        "eventType": "$EVENT_TYPE",
        "event_id": "$ID",
        "alert_metric": "$ALERT_METRIC",
        "alert_priority": "$ALERT_PRIORITY",
        "alert_title": "$ALERT_TITLE",
        "alert_type" : "$ALERT_TYPE",
        "event_msg" : "$EVENT_MSG",
        "incident_pub_id" : "$INCIDENT_PUBLIC_ID",
        "incident_title" : "$INCIDENT_TITLE",
        "incident_url" : "$INCIDENT_URL",
        "incident_msg" : "$INCIDENT_MSG",
        "security_rule_id" : "$SECURITY_RULE_ID",
        "security_rule_name" : "$SECURITY_RULE_NAME",
        "security_signal_severity" : "$SECURITY_SIGNAL_SEVERITY",
        "security_signal_title" : "$SECURITY_SIGNAL_TITLE",
        "security_signal_msg" : "$SECURITY_SIGNAL_MSG",
        "security_rule_query" : "$SECURITY_RULE_QUERY",
        "security_rule_type" : "$SECURITY_RULE_TYPE",
        "tags" : "$TAGS"
    }
```

6. Click on “Save” to complete the service integration.

    View the [official documentation][3] from Squadcast for more details on setup.

## Data Collected
### Metrics

Squadcast integration does not include any metrics.

### Events

Your Squadcast Triggered / Resolved events will appear in your Squadcast platform dashboard.

### Service Checks

Squadcast integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog Support][4].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/squadcast/images/datadog-service.png
[2]: https://user-images.githubusercontent.com/87639260/140858849-b4059d94-893d-4900-9168-db4c369a62a0.png
[3]: https://support.squadcast.com/docs/datadog
[4]: https://docs.datadoghq.com/help/
