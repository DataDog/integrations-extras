## Overview

The [ilert][1] integration sends Datadog alerts to ilert and seamlessly takes actions on these alerts within the ilert platform.
ilert is an incident management platform that enables teams to cover all stages of the incident cycle. ilert provides reliable and actionable alerting, call routing, flexible on-call schedules, status pages, various ChatOps features, AI assistance in incident communications, and post-mortem creation. With ilert, DevOps teams increase uptime and respond to incidents faster.

Integrate with ilert to:

- Trigger and resolve incidents from Datadog
- Tackle incidents and set up escalation policies as they occur
- Set up a daily reminder of who is on-call

## Setup

### ilert

#### Create Datadog alert source

1. Switch to the **Alert Sources** tab and click on the "Create new alert source" button

2. Search for "**Datadog**", select the **Datadog** tile and click on Next.

   ![ilert Alert Source New][2]

3. Assign a name.

   ![ilert Alert Source New 2][10]

4. Select a desired escalation policy.

   ![ilert Alert Source New 3][11]

5. On the next page a **Webhook URL** is generated. You need this URL for the integration setup within Datadog.

   ![ilert Alert Source View][3]

### Datadog

#### Add ilert Webhook as alerting channel

1. From the Datadog Integrations page, [**install the Webhooks integration**][8].
2. On the Webhooks integration tile, add a new webhook:

   ![Datadog Webhook New][4]

3. Enter a name, the **Datadog webhook URL** generated earlier from the ilert alert source, and the **template payload**:

   ```json
   {
     "body": "$EVENT_MSG",
     "last_updated": "$LAST_UPDATED",
     "event_type": "$EVENT_TYPE",
     "alert_transition": "$ALERT_TRANSITION",
     "alert_id": "$ALERT_ID",
     "link": "$LINK",
     "title": "$EVENT_TITLE",
     "date": "$DATE",
     "org": {
       "id": "$ORG_ID",
       "name": "$ORG_NAME"
     },
     "id": "$ID"
   }
   ```

   ![Datadog Webhook View][5]

4. Click Save.

## Data Collected

### Metrics

The ilert integration does not include any metrics.

### Events

Your ilert triggered and resolved events appear in the ilert platform dashboard.

### Service Checks

The ilert integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][7].

[1]: https://www.ilert.com/?utm_medium=organic&utm_source=integration&utm_campaign=datadog
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-view.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-webhook-new.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-webhook-view.png
[6]: https://docs.ilert.com/integrations/datadog?utm_medium=organic&utm_source=integration&utm_campaign=datadog
[7]: https://docs.datadoghq.com/help/
[8]: https://app.datadoghq.com/integrations/webhooks
[9]: https://docs.ilert.com/incident-comms-and-status-pages/metrics/import-metrics-from-datadog
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new-2.png
[11]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new-3.png
