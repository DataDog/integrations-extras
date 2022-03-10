# StackPulse Integration

## Overview

The [StackPulse][1] integration enables you to trigger automatic playbooks in response to Datadog alerts, providing alert enrichment, incident mitigation, and collaboration. You can then send back events from your playbook executions directly to your Datadog event stream and dedicated StackPulse dashboard.

## Setup

To set up this integration, you must have an active [StackPulse account][2] and an Account Owner role in that account. You must also have proper admin permissions in Datadog.

### StackPulse

1. On the **Integrations** page under **Monitoring**, locate the **Datadog** card and click [**New**][2].

2. Provide a meaningful name for the integration and click **Add**.

3. **Copy** the newly created webhook endpoint.

### Datadog

1. Navigate to **Integrations** and choose the [**Webhooks**][5] card.

2. Click on **New** to add a new Webhook integration.

3. Fill in the name for a new Webhook integration (remember to use it later in specific Datadog monitors to trigger StackPulse) and the Webhook URL from the previous step.

4. StackPulse recommends enhancing the payload with additional alert information, using portions of a configuration below:

    ```json
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

5. Pick monitors for triggering StackPulse Playbooks, and in the **Alert Your Team** field, add a reference to the newly created Webhook integration. For more details, see [Manage Monitors][7].

6. Navigate to **Integrations -> APIs** and choose the **API Keys** card. Under **New API Key**, input a meaningful name for the new key and click **Create API Key**, then **Copy** the new key.

### Back to StackPulse

1. On the **Integrations** page under **Secrets**, locate the **Datadog API Keys** card and click [**Add**][8].

2. Provide a meaningful name for the integration and click **Add**.

## Data Collected

### Metrics

The StackPulse integration does not provide any metrics.

### Events

The StackPulse integration allows you to send events to your Datadog event stream using the [Datadog Post Event][10] step. You can use the step with your playbooks to notify Datadog about successful mitigations, execution failures and send enriched alert data back to Datadog.

### Service Checks

The StackPulse integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][11].

[1]: https://stackpulse.com
[2]: https://stackpulse.com/get-started/
[3]: https://app.stackpulse.io/integrations/datadog?create=true
[5]: https://app.datadoghq.com/account/settings#integrations/webhooks
[7]: https://docs.datadoghq.com/monitors/manage/
[8]: https://app.stackpulse.io/integrations/datadog%20api%20keys?create=true
[10]: https://github.com/stackpulse/steps/tree/master/steps/datadog/post-event
[11]: https://docs.datadoghq.com/help/
