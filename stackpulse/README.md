# Torq Integration

## Overview

The [Torq][1] integration enables you to trigger workflows in response to Datadog alerts, providing alert enrichment. You can then send back events directly from your Torq workflows to your Datadog event stream and dedicated Torq dashboard.

## Setup

To set up this integration, you must have an active [Torq account][2] and an Account Owner role in that account. You must also have proper admin permissions in Datadog.

### Create a Datadog trigger integration in Torq

1. Go to **Integrations > Triggers**, locate the **Datadog** card, and click **Add**.

2. Enter a meaningful name for the integration and click **Add**.

3. Copy the webhook URL that is generated. You'll need this URL when you configure a Webhook integration in your Datadog tenant.

### Define the monitors to trigger events in Torq

1. Navigate to **Integrations > Integrations**, click the **Webhooks** card, and click **New**.
    ![datadog_webhook](https://raw.githubusercontent.com/DataDog/integrations-extras/master/stackpulse/images/datadog_webhook.png)

2. Enter a meaningful name for the Webhook integration and paste the Webhook URL that you generated in Torq. The integration name is how you'll the identifier (remember to use it later in specific Datadog monitors to trigger Torq) and the Webhook URL from the previous step.
    ![datadog_webhook_2](https://raw.githubusercontent.com/DataDog/integrations-extras/master/stackpulse/images/datadog_webhook_2.png)

3. Torq recommends adding additional alert information to the payload. You can use portions of the below configuration:

    ```json linenums="1"
    {
        "body": "$EVENT_MSG",
        "title": "$EVENT_TITLE",
        "date": "$DATE",
        "id": "$ID",
        "metadata": {
            "AGGREG_KEY": "$AGGREG_KEY",
            "ALERT_CYCLE_KEY": "$ALERT_CYCLE_KEY",
            "ALERT_ID": "$ALERT_ID",
            "ALERT_METRIC": "$ALERT_METRIC",
            "ALERT_QUERY": "$ALERT_QUERY",
            "ALERT_SCOPE": "$ALERT_SCOPE",
            "ALERT_STATUS": "$ALERT_STATUS",
            "ALERT_TITLE": "$ALERT_TITLE",
            "ALERT_TRANSITION": "$ALERT_TRANSITION",
            "ALERT_TYPE": "$ALERT_TYPE",
            "EMAIL": "$EMAIL",
            "EVENT_MSG": "$EVENT_MSG",
            "EVENT_TITLE": "$EVENT_TITLE",
            "EVENT_TYPE": "$EVENT_TYPE",
            "HOSTNAME": "$HOSTNAME",
            "ID": "$ID",
            "LAST_UPDATED": "$LAST_UPDATED",
            "LINK": "$LINK",
            "METRIC_NAMESPACE": "$METRIC_NAMESPACE",
            "ORG_ID": "$ORG_ID",
            "ORG_NAME": "$ORG_NAME",
            "PRIORITY": "$PRIORITY",
            "SNAPSHOT": "$SNAPSHOT",
            "TAGS": "$TAGS",
            "TEXT_ONLY_MSG": "$TEXT_ONLY_MSG",
            "USER": "$USER",
            "USERNAME": "$USERNAME",
            "LOGS_SAMPLE": "$LOGS_SAMPLE"
        }
    }
    ```

4. Pick monitors for triggering Torq Playbooks, and in the **Alert Your Team** field, add a reference to the newly created Webhook integration. For further details, see the [DataDog documentation on managing monitors][7].

## Use Datadog steps in Torq workflows

You need to create a Datadog API key and an application key, which you'll use as input parameters for Datadog steps in Torq.

!!! note
    Some Datadog steps in Torq require an API key and application key, and some require the Datadog integration.

### Create an API Key in Datadog

After you create the API key, make sure you copy and save it. You won't be able to access it later. For more information about API keys, see the [Datadog documentation](https://docs.datadoghq.com/account_management/api-app-keys/).

1. Hover over your user name and select **Organization Settings**.
2. From the left panel, click **API Keys**.
3. Click **+ New Key**.
    ![datadog_api_key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/stackpulse/images/datadog_api_key.png)
4. Enter a meaningful name for the API key, such as `Torq`, and click **Create Key**.
5. Copy the `Key` and save it. You will need this key when creating a Datadog integration in Torq.

### Create an Application Key in Datadog

After you create the application key, make sure you copy and save it. You won't be able to access it later. For more information about application keys, see the [Datadog documentation](https://docs.datadoghq.com/account_management/api-app-keys/#add-application-keys/).

1. Hover over your user name and select **Organization Settings**.
2. From the left panel, click **Application Keys**.
3. Click **+ New Key**.
    ![datadog_app_key](https://raw.githubusercontent.com/DataDog/integrations-extras/master/stackpulse/images/datadog_app_key.png)
4. Enter a meaningful name for the application key, such as `Torq`, and click **Create Key**.
5. Copy the `Key` and save it. You will need this key when creating a Datadog integration in Torq.

### Create a Datadog integration in Torq

The integration enables you to use Datadog steps in your Torq workflows.

1. Go to **Integrations > Steps**, locate the **Datadog** card, and click **Add**.

2. Enter a meaningful name for the integration, such as `Datadog-<monitor_type>` and click **Add**.

## Data Collected

### Metrics

The Torq integration does not provide any metrics.

### Events

The Torq integration allows you to send events to your Datadog event stream from a Torq workflow using the step [Datadog Post Event][10] step. You can use the step with your playbooks to notify Datadog about successful mitigations, execution failures and send enriched alert data back to Datadog.

### Service Checks

The Torq integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://torq.io
[2]: https://torq.io/get-started/
[5]: https://app.datadoghq.com/account/settings#integrations/webhooks
[7]: https://docs.datadoghq.com/monitors/manage_monitor/
[10]: https://github.com/torqio/steps/tree/master/steps/datadog/post-event
[11]: https://docs.datadoghq.com/help/
