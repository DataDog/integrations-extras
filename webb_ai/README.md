# Webb.ai

## Overview

Matt by Webb.ai is the first AI-enabled reliability engineer. Matt troubleshoots Monitors from Datadog, incidents from infrastructure like Kubernetes, and alerts from cloud providers like AWS, Azure, and Google Cloud. It automates troubleshooting to identify the root cause of an alert or incident in less than 5 mins.

With this integration
- Datadog monitors in alert state will be identified and automatically analyzed by Matt
- Troubleshooting results will improve as Matt can query Datadog metrics when required(even for kubernetes incidents, aws alerts etc.)

Data queried by Matt:
- Event stream to identify Monitors in alert state
- Monitors and Metrics data while troubleshooting

## Setup

1. Visit [Webb.ai][2] to sign up for free
2. Navigate to Webb.ai tile in [Datadog integrations page][5] and click **Install Integration**
3. Go to the **Configure** tab and click **Connect Accounts**
4. Follow the series of OAuth steps to complete the integration

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
- RCAs performed by Matt
- Changes observed in Kubernetes clusters 

## Troubleshooting

Need help? Contact [Webb.ai support][3].

[1]: https://app.webb.ai/integrations
[2]: https://app.webb.ai/
[3]: mailto:support@webb.ai
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://app.datadoghq.com/integrations

