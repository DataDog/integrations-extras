## Overview

Use the Datadog-Squadcast integration to send Datadog alerts to Squadcast and seamlessly take actions on these alerts within the Squadcast platform.

Connect Squadcast to Datadog in order to:
- Trigger and resolve incidents from Datadog
- Tackle incidents and set up escalation policies as they occur
- Set up a daily reminder of who is on-call

## Setup

**Note**:
Only the users with Account Owner or Admin privileges can configure services on Squadcast.
At least one Escalation Policy must be configured before you can add a service.

### Follow these steps in Squadcast:

1. Open **Services** page from the sidebar.

2. Click on "Add Service".

3. Enter a meaningful **Service Name** and optionally a **Service Description**.

4. Select **Datadog** from the **Integration Type** drop-down menu.

5. Copy the **Datadog Webhook URL** generated below and click "Save".

![Squadcast Service][1]

### Follow these steps in Datadog:

1. Open the **Integrations** page from the sidebar.

2. Use the search bar to search for "webhooks".

3. Once the **Webhooks** tile appears, hover and click on "Install".

4. Navigate to the **Configuration** tab and scroll to the bottom of the page.

5. Under the section **Name and URL**, enter a meaningful name and paste the **Datadog Webhook URL** provided by Squadcast.

    ![Squadcast Webhook][2]

6. Tick the checkbox under the section **Use custom payload**.
7. Copy-paste the following JSON in the text box under the **Custom Payload** section:

    ```json
    {
        "alertId": "$ALERT_ID",
        "eventMessage": "$TEXT_ONLY_MSG",
        "title": "$EVENT_TITLE",
        "url": "$LINK",
        "alertTransition": "$ALERT_TRANSITION"
    }
    ```

8. Click on "Install Integration" to complete the service integration.

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
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/squadcast/images/datadog-webhook.png
[3]: https://support.squadcast.com/docs/datadog
[4]: https://docs.datadoghq.com/help/
