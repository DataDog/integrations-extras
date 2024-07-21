# Webb.ai

## Overview

Matt by Webb.ai is the first AI-enabled reliability engineer.
Matt troubleshoots monitors and alerts from Datadog, Kubernetes, and cloud providers like AWS, Azure, and GCP.
It identifies the root cause of an alert or incident in less than 5 mins.

With this integration, Matt automatically identifies alerts from Datadog and troubleshoots them, and the mean time to debug those alerts is reduced significantly. 80-90% of troubleshooting is automated, greatly reducing the debugging time for on-call engineers.

This integration queries the following data:
- Datadog events
- Datadog metrics and tags

This integration sends events to Datadog, including the root cause analysis performed by Matt and changes in Kubernetes clusters.
You can view detailed root cause analyses for your alerts, including all hypotheses analyzed and the exact steps Matt took with supporting evidence.
With this analysis, 80-90% of troubleshooting is automated, greatly reducing the debugging time of on-call engineers. 

## Setup

1. Visit [Webb.ai][2] and sign up for the free service.
2. Navigate to Webb.ai tile in the [Datadog integrations page][5] and click **Install Integration**.
3. Go to the **Configure** tab and click **Connect Accounts**.
4. Follow the series of OAuth steps to finish setting up the integration.

## Uninstallation
To remove the Datadog integration from Webb.ai, navigate to the [Webb.ai integrations page][1] and delete the Datadog integration from the list.

Once this integration has been uninstalled, any previous authorizations are revoked.

To ensure that all API keys associated with this integration are disabled, search for the integration name on the [Datadog API Keys][4] page.

## Data Collected

### Metrics
Webb.ai does not generate any metrics; it relies on Datadog metrics.

### Service Checks
Webb.ai does not include any service checks.

### Events
Webb.ai sends the following events to Datadog:
- Root cause analyses performed by Matt
- Changes observed in Kubernetes clusters 

## Troubleshooting

Need help? Contact [Webb.ai support][3].

[1]: https://app.webb.ai/integrations
[2]: https://app.webb.ai/
[3]: mailto:support@webb.ai
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://app.datadoghq.com/integrations

