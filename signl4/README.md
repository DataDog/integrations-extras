## Overview

Use the [SIGNL4][1] integration to send Datadog alerts to SIGNL4 teams and seamlessly take actions on these alerts within the SIGNL4 app.

Connect SIGNL4 to Datadog in order to:
- Trigger and resolve incidents from Datadog
- Tackle incidents and set up escalation policies as they occur
- Set up a daily reminder of who is on-call

![SIGNL4 App][2]

## Setup

### SIGNL4

Follow these steps in SIGNL4:

1. Use your existing account or create a SIGNL4 account at [signl4.com][1].

2. In your SIGNL4 app find your SIGNL4 webhook address including your team secret under *Teams -> Your Team -> Secret*.

### Datadog Alerts

You can alert your SIGNL4 team about new Alerts in Datadog. Alerts that get resolved in Datadog will automatically close the alert in SIGNL4. In order to do so you need to configure the following.

1. Navigate to the [Webhooks Integration tile][9].

2. On the **Configuration** tab, go to Webhooks and click **New**.

3. Under **New Webhook**, enter a meaningful `Name` and use the SIGNL4 Webhook `URL` (created above) including your team secret, for example:

    ```
    https://connect.signl4.com/webhook/[team-secret]?ExtIDParam=alertId&ExtStatusParam=alertTransition&ResolvedStatus=Recovered
    ```

    Replace `[team-secret]` with your SIGNL4 team secret here.

    ![SIGNL4 Alerts Webhook][3]

4. Copy-paste the following JSON in the `Payload` text box:

    ```json
	{
		"title": "$EVENT_TITLE",
		"message": "$TEXT_ONLY_MSG",
		"link": "$LINK",
		"priority": "$ALERT_PRIORITY",
		"host": "$HOSTNAME",
		"alertScope": "$ALERT_SCOPE",
		"alertStatus": "$ALERT_STATUS",
		"alertId": "$ALERT_ID",
		"alertTransition": "$ALERT_TRANSITION",
		"X-S4-SourceSystem": "Datadog",
		"date": "$DATE",
		"org": {
			"id": "$ORG_ID",
			"name": "$ORG_NAME"
		},
		"id": "$ID"
	}
    ```

You can adapt the parameters according to your need but please leave alertId, alertTransition and X-S4-SourceSystem unchanged.

5. Click on **Save** to complete the webhook creation.

For more details, see [Mobile alerting with tracking & escalation for Datadog][7].

That's it and now you can use your webhook as a notification channel in your Monitor. You can choose @webhook-SIGNL4 here if SIGNL4 is the name of your webhook. When the conditions of the monitor apply your team will receive a new SIGNL4 alert.

### Datadog Incidents

You can alert your SIGNL4 team about new Incidents in Datadog. Incidents that get resolved in Datadog will automatically close the alert in SIGNL4. In order to do so you need to configure the following.

1. Navigate to the [Webhooks Integration tile][9].

2. On the **Configuration** tab, go to Webhooks and click **New**.

3. Under **New Webhook**, enter a meaningful `Name` and use the SIGNL4 Webhook `URL` (created above) including your team secret, for example:

    ```
    https://connect.signl4.com/webhook/[team-secret]?ExtIDParam=s4ExternalId&ExtStatusParam=incidentStatus&ResolvedStatus=resolved
    ```

    Replace `[team-secret]` with your SIGNL4 team secret here.

    ![SIGNL4 Incidents Webhook][4]

4. Copy-paste the following JSON in the `Payload` text box:

    ```json
	{
		"title": "$EVENT_TITLE",
		"message": "$TEXT_ONLY_MSG",
		"link": "$LINK",
		"priority": "$ALERT_PRIORITY",
		"host": "$HOSTNAME",
		"alertScope": "$ALERT_SCOPE",
		"alertStatus": "$ALERT_STATUS",
		"alertId": "$ALERT_ID",
		"incidentPublicId": "$INCIDENT_PUBLIC_ID",
		"incidentStatus": "$INCIDENT_STATUS",
		"alertTransition": "$ALERT_TRANSITION",
		"s4ExternalId": "DATADOG-INCIDENT-$INCIDENT_PUBLIC_ID",
		"X-S4-SourceSystem": "Datadog",
		"date": "$DATE",
		"org": {
			"id": "$ORG_ID",
			"name": "$ORG_NAME"
		},
		"id": "$ID"
	}
    ```

You can adapt the parameters according to your need but please leave incidentStatus, s4ExternalId and X-S4-SourceSystem unchanged.

5. Click on **Save** to complete the webhook creation.

For more details, see [Mobile alerting with tracking & escalation for Datadog][7].

### Incidents Rule

Now you can create a rule in Datadog under Monitors -> Settings (Incidents) Rules. In the you specify the criteria, i.e. the severity, service, etc. For the "Other attributes" we recommend to use "state:active" that will trigger a new alert and "state:resolved" that will close the alert. Under "Notify" you select your SIGNL4 incident webhook as created above and that's it.

![SIGNL4 Incidents Rule][5]

If you create a new incident now, your SIGNL4 team will receive an alert. If you acknowledge / close the alert in the SIGNL4 app, the incident status will be set to Stable / Resolved.

Also, if you set the incident status to Resolved in Datadog, this will close the alert in SIGNL4.

### Status Updates for Datadog Incidents

For Datadog incidents you can update the status to Stable / Resolved directly from your SIGNL4 app by acknowledging / closing the respective alert.

In order to configure this back channel, go to your SIGNL4 web portal and then to Teams -> Apps. Search for the Datadog connector app and click "Create" there. You can find more information directly within the app settings.

![Datadog Connector App][6]

You need to configure the following.

Datadog URL: The URL of your Datadog instance, e.g. https://app.datadoghq.com/ or https://app.datadoghq.eu/.  
Datadog API Key: Your Datadog API key. You can find or create this one in Datadog under your account, Organization Settings -> API Keys.  
Datadog Application Key: Your Datadog application key. You can find or create this one in Datadog under your account, Organization Settings -> Application Keys.  
Acknowledgement as Stable: Acknowledgements set the incident status to Stable.  

## Data Collected

### Metrics

The SIGNL4 integration does not include any metrics.

### Events

SIGNL4 triggered and resolved events appear in your SIGNL4 app and web portal.

### Service Checks

The SIGNL4 integration does not include any service checks.

## Troubleshooting
Need help? Contact [SIGNL4 Support][8].

[1]: https://www.signl4.com
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/signl4-phone.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/datadog-alerts-webhook.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/datadog-incidents-webhook.png
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/datadog-incidents-rule.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/signl4-datadog-connector-app.png
[7]: https://www.signl4.com/blog/portfolio_item/datadog_mobile_alerting/
[8]: mailto:success@signl4.com
[9]: https://app.datadoghq.com/account/settings#integrations/webhooks

