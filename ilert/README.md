## Overview

The [ilert][1] integration sends Datadog alerts to ilert and seamlessly takes actions on these alerts within the ilert platform.

Integrate with ilert to:

- Trigger and resolve incidents from Datadog
- Tackle incidents and set up escalation policies as they occur
- Set up a daily reminder of who is on-call
- Export metrics from Datadog to ilert to provide information about the health of your services on ilert status pages

## Setup

### ilert

#### Create Datadog alert source

1. Switch to the **Alert Sources** tab and click on the "Create new alert source" button

2. Search for "**Datadog**", select the **Datadog** tile and click on next.

   ![ilert Alert Source New][2]

3. Assign a name

   ![ilert Alert Source New 2][10]

4. Select a desired escalation policy

   ![ilert Alert Source New 3][11]

5. On the next page a **Webhook URL** is generated. You need this URL at the bottom of the setup in Datadog.

   ![ilert Alert Source View][3]

### Datadog

#### Add ilert Webhook as alerting channel

1. Go to Datadog integrations page and [**install Webhooks integration**][8]:
2. On the Webhooks integration page, scroll to the bottom and add a new webhook:

   ![Datadog Webhook New][4]

3. Enter a name, the **Datadog webhook URL** from ilert alert source and **template payload**:

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

4. Click save button to finish setting up this check.

   View the [ilert Datadog Integration documentation][6] for more details.

## Data Collected

### Metrics

To export metrics from Datadog and display them on your ilert status page, follow the instructions in the [ilert documentation][9]

### Events

Your ilert triggered and resolved events appear in the ilert platform dashboard.

### Service Checks

ilert integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][7].

[1]: https://www.ilert.com/?utm_medium=organic&utm_source=integration&utm_campaign=datadog
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-view.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-webhook-new.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-webhook-view.png
[6]: https://docs.ilert.com/integrations/datadog?utm_medium=organic&utm_source=integration&utm_campaign=datadog
[7]: https://docs.datadoghq.com/help/
[8]: https://app.datadoghq.com/account/settings#integrations
[9]: https://docs.ilert.com/incident-comms-and-status-pages/metrics/import-metrics-from-datadog
[10]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new-2.png
[11]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new-3.png
