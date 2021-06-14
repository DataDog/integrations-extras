## Overview

The [iLert][1] integration sends Datadog alerts to iLert and seamlessly take actions on these alerts within the iLert platform.

Integrate with iLert to:

- Trigger and resolve incidents from Datadog
- Tackle incidents and set up escalation policies as they occur
- Set up a daily reminder of who is on-call

## Setup

### iLert

#### Create Datadog alert source

1. Switch to the **Alert Sources** tab and click on the "Create new alert source" button

2. Assign name and select escalation chain

3. Select **Datadog** in the Integration type field and save.

   ![iLert Alert Source New][2]

4. On the next page a **Webhook URL** is generated. You will need this URL at the bottom of the setup in Datadog.

   ![iLert Alert Source View][3]

### Datadog

#### Add iLert Webhook as alerting channel

1. Go to Datadog integrations page and [**install Webhooks integration**][8]:
2. Click an Webhooks integration, scroll to bottom and add a new webhook:

   ![Datadog Webhook New][4]

3. Enter a name, the **Datadog webhook URL** from iLert alert source and **template payload**:

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

4. Click save button
5. The integration is now set up!

   View the [official documentation][6] from iLert for more details on setup.

## Data Collected

### Metrics

iLert integration does not include any metrics.

### Events

Your iLert Triggered / Resolved events will appear iLert platform dashboard.

### Service Checks

iLert integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][7].

[1]: https://www.ilert.com
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-new.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-alert-source-view.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-webhook-new.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/ilert/images/datadog-webhook-view.png
[6]: https://docs.ilert.com/integrations/datadog
[7]: https://docs.datadoghq.com/help/
[8]: https://app.datadoghq.com/account/settings#integrations
