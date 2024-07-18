# CloudAEye

## Overview

Kosal from CloudAEye acts as your root cause co-pilot. This integration enables Datadog users to import observability data (logs, metrics, traces) and view automated root cause analyses. Additionally, it identifies similar issues within Jira and related code changes that may be contributing to the incident. To expedite incident identification, Kosal publishes events with a summary and root cause to a Datadog dashboard.

## Setup

### Installation

- Search for `CloudAEye` in the datadog integrations page.

- Click on **Install Integration** button.

- On successful installation, click on the **Connect Accounts** button upon which you will be redirected to the Integrations page on CloudAEye console (Side Menu > Integrations > Datadog).

- To integrate your datadog account with CloudAEye, you will need to provide the following details

  - `Site`: Select the datadog site where your observability data is located. **Ex: US1-East**. Read more about datadog sites [here](https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site)

  - `API Key`: An API key helps us uniquely identify the organization. To create a new API key in Datadog console, navigate to **Organization Settings > API Keys** and then create a new API Key for CloudAEye integration. Once created copy that key and provide it here. Read more about API Key [here](https://docs.datadoghq.com/account_management/api-app-keys/)

  - `Application Key`: In addition to an API key, we need an Application Key to programmatically access your data. To create a new Application key in Datadog console, navigate to **Organization Settings > Application Keys** and then created a new Application key (with **scope set to read-only** in all sections). Once created copy that key and provide it here. Read more about Application Key [here](https://docs.datadoghq.com/account_management/api-app-keys/)

- Once the required keys are populated, click `Test Connection` to test your your Datadog account integration with CloudAEye. A success message indicates that your integration is successful.
### Configuration

Once integrated, begin exploring your logs, metrics, and traces data in the CloudAEye dashboard. Some of the most useful features are:
- To get notified about any incident, go to the settings page from CloudAEye's **Side Navigation Drawer => Settings => Root Cause Analysis**, then select the Send Alerts checkbox and choose/add a new notification alert channel of your choice.
- You can also ask any questions related to your logs, metrics, or traces from Kosal at the [Root Cause Analysis Dashboard][4].

## Uninstallation

To remove the Datadog integration from CloudAEye:
1. Navigate to the [CloudAEye integrations page][1] (Side Navigation Drawer => Integrations => Datadog) and click **Remove**.
2. Uninstall this integration from Datadog by clicking the **Uninstall Integration** button below. Once you uninstall this integration, any previous authorizations are revoked.
3. Ensure that all API keys associated with this integration have been disabled by searching for the integration name (CloudAEye) on the [API Keys management page][3].

## Support

Need help? Contact [CloudAEye support](mailto:support@cloudaeye.com).


[1]: https://console.cloudaeye.com/integrations/datadog
[2]: https://app.datadoghq.com/organization-settings/oauth-applications
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=CloudAEye
[4]: https://console.cloudaeye.com/rca?startTime=1,months&endTime=now
