# AlertNow

## Overview

AlertNow is an integrated incident management platform that collects alerts from various and complex IT environments and delivers the alerts to the right people, enabling them to handle incidents rapidly. Connecting AlertNow with Datadog automatically syncs your Datadog alerts with those in AlertNow. You can manage alerts on a single platform, notify your teams, and respond to critical issues immediately.


What AlertNow offers:
- Trigger and resolve incidents from Datadog
- Notify the right people via email, SMS, Voice call, and mobile application when they occur
- Notify users based on escalation policy
- Reports on MTTA and MTTR, and analysis reports

![alertnow overview][1]

## Setup

### AlertNow

To connect Datadog with AlertNow, you must create a webhook and add monitors in Datadog.

1. Use your existing account or create an AlertNow account in opsnow.com.
2. Log in to AlertNow and go to the Configuration > Integration menu.
3. Click **Create Integration**, and then select the **Datadog** card.

    ![datadog card][2]

4. In the Create integration page, enter the required information, and then click the OK button to create the integration.

    ![datadog integration][3]

5. Copy the URL from the Integration page of AlertNow.
    ![datadog detail][4]


### Datadog

Follow the steps below for Datadog integration.

1. Open the [Webhooks Integration tile][5].

2. Select the **Configuration** tab, and scroll to the bottom and click **New**.

3. On the **New Webhook** form, enter a meaningful name and AlertNow Webhook URL which was created in the AlertNow integration page. The format of copied AlertNow Webhook URL is as below, and variables in **{API-KEY}** vary.

    <pre><code> https://alertnowitgr.opsnow.com/integration/datadog/v1/{API-KEY} </code></pre>

    ![datadog webhook][6]

4. Paste JSON Payload below and paste it in the Payload window.

    ``` json
    {
        "id":"$ID",
        "email":"$EMAIL",
        "eventTitle":"$EVENT_TITLE",
        "eventMsg":"$EVENT_MSG",
        "textOnlyMsg":"$TEXT_ONLY_MSG",
        "eventType":"$EVENT_TYPE",
        "date":"$DATE",
        "datePosix":"$DATE_POSIX",
        "alertId":"$ALERT_ID",
        "alertType":"$ALERT_TYPE",
        "aggregKey":"$AGGREG_KEY",
        "orgId":"$ORG_ID",
        "alertStatus":"$ALERT_STATUS",
        "alertScope":"$ALERT_SCOPE",
        "hostname":"$HOSTNAME",
        "user":"$USER",
        "username":"$USERNAME",
        "snapshot":"$SNAPSHOT",
        "link":"$LINK",
        "priority":"$PRIORITY",
        "tags":"$TAGS",
        "lastUpdated":"$LAST_UPDATED",
        "lastUpdatedPosix":"$LAST_UPDATED_POSIX",
        "alertMetric":"$ALERT_METRIC",
        "metricNamespace":"$METRIC_NAMESPACE",
        "alertTransition":"$ALERT_TRANSITION",
        "orgName":"$ORG_NAME",
        "alertQuery":"$ALERT_QUERY",
        "alertTitle":"$ALERT_TITLE",
        "alertCycleKey":"$ALERT_CYCLE_KEY"
    }

    ```

5. Refer to [Datadog documents][7] for the next configuration steps.


## Support

Need help? Contact [Datadog support][8] or reach out to [AlertNow support](mailto:support@opsnow.com).

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/alertnow/images/alertnow_overview.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/alertnow/images/integration_card_datadog.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/alertnow/images/create_integration_datadog_en.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/alertnow/images/datadog_integration_detail.png
[5]: https://app.datadoghq.com/account/login?next=%2Faccount%2Fsettings#integrations/webhooks
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/alertnow/images/datadog_webhook.png
[7]: https://docs.datadoghq.com/monitors/
[8]: https://docs.datadoghq.com/help/