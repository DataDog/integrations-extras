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

2. In your SIGNL4 app find your SIGNL4 webhook address including your team secret under *Settings -> APIs*.

### Datadog

Follow these steps in Datadog:

1. Navigate to the [Webhooks Integration tile][6].



2. On the **Configuration** tab, scroll down and click **New**.

3. Under **New Webhook**, enter a meaningful `Name` and use the SIGNL4 Webhook `URL` (created above) including your team secret, for example:

    ```
    https://connect.signl4.com/webhook/<team-secret>?ExtIDParam=alertId&ExtStatusParam=alertTransition&ResolvedStatus=Recovered
    ```

    Replace `<team-secret>` with your SIGNL4 team secret here.

    ![SIGNL4 Webhook][3]

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

5. Click on **Save** to complete the service integration.

For more details, see [Mobile alerting with tracking & escalation for Datadog][4].

## Data Collected

### Metrics

The SIGNL4 integration does not include any metrics.

### Events

SIGNL4 triggered and resolved events appear in your SIGNL4 app and web portal.

### Service Checks

The SIGNL4 integration does not include any service checks.

## Troubleshooting
Need help? Contact [SIGNL4 Support][5].

[1]: https://www.signl4.com
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/signl4-phone.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/signl4/images/datadog-webhook.png
[4]: https://www.signl4.com/blog/portfolio_item/datadog_mobile_alerting/
[5]: mailto:success@signl4.com
[6]: https://app.datadoghq.com/account/settings#integrations/webhooks
