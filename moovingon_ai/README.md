# moovingon.ai

## Overview
[moovingon.ai][1] is a platform for cloud operations and NOC management. It consolidates alerts across your observability suite and associates them with automated runbooks for alert and incident remediation. By integrating this, you can utilize the power of Datadog and moovingon.ai for efficient, automated incident management.

moovingon.ai uses Datadog's monitors, logs, and event data for alert correlation and aggregation.
Key features of this integration include:

1. **Focused Alert Management**: Bring all your Datadog alerts together in moovinon.ai easy-to-view dashboard, giving you simple control and clear visibility.
2. **Comprehensive incident management**: Log all remediation actions performed in moovingon.ai in Datadog events for compliance and remediation clarity.
3. **Extensive Analysis**: Utilize the analytics provided by moovingon.ai to derive insights from Datadog alerts. This assists in proactive decision-making and trend analysis.

## Setup

### Installation

1. Click on **Connect Accounts** in order to login into moovingon.ai.
2. Enter a name for the datadog integration and **Submit**.
3. Proceed to the Datadog OAuth2 screen and click on the **authorize** button.
4. **(Optional)** To receive events from all monitors, click on **install/update the webhook**.

## Uninstallation

1. Inside the moovingon.ai account, Go to **Settings** --> **Templates** and remove all the related datadog templates.
2. Go to **Setings** --> **Integrations** and remove the datadog integration.
3. Inside Datadog, **Integrations**  --> **Integrations**.
4. Click the moovingon.ai tile and click on **Uninstall integration**.


### Metrics

moovingon.ai does not include any metrics.

### Service Checks

moovingon.ai does not include any service checks.
### Events

The moovingon integration includes events.

## Troubleshooting

Need help? Contact [moovingon.ai support][2].

[1]: https://moovingon.ai/
[2]: support@moovingon.com

