# CloudAEye

## Overview

Kosal from CloudAEye acts as your root cause co-pilot. This integration enables Datadog users to import observability data (logs, metrics, traces) and view automated root cause analyses in CloudAEye. Additionally, it identifies similar issues within Jira and related code changes that may be contributing to the incident. To expedite incident identification, Kosal sends events with a summary and root cause to Datadog.

## Setup

### Installation

- Search for `CloudAEye` in the datadog integrations page.

- Click on **Install Integration** button.

- You need to create a [CloudAEye account](https://docs.cloudaeye.com/user-guide/tasks/register.html) if you do not already have one. 

- On successful registration, login to your cloudaeye account and add a **Datadog Integration**. Follow this [step-by-step guide](https://docs.cloudaeye.com/user-guide/integrations/datadog.html) to setup this integration. 

  - To integrate your datadog account with CloudAEye, we usually require the following details.

    - `Site`: The datadog site where your observability data is located. **Ex: US1-East**. Read more about datadog sites [here](https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site)

    - `API Key`: An API key helps us uniquely identify the organization. Read more about API Key [here](https://docs.datadoghq.com/account_management/api-app-keys/)

    - `Application Key`: In addition to an API key, we need an Application Key to programmatically access your data. Read more about Application Key [here](https://docs.datadoghq.com/account_management/api-app-keys/)


- Once the integration is complete, your Datadog account is successfully connected to CloudAEye.



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
