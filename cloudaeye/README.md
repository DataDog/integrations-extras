# CloudAEye

## Overview

Kosal from CloudAEye acts as your root cause copilot. This integration enables Datadog users to import observability data (logs, metrics, traces) and view automated root cause analyses in CloudAEye. Additionally, it identifies similar issues within Jira and related code changes that may be contributing to the incident. To expedite incident identification, Kosal sends events with a summary and root cause to Datadog.

## Setup

### Pre-installation steps

- Create a [CloudAEye account](https://docs.cloudaeye.com/user-guide/tasks/register.html) if you do not already have one. 


### Installation

- Log in to your CloudAEye account and add a **Datadog Integration**. 
  - To integrate your Datadog account with CloudAEye, we require the following details.

    - `Site`: The Datadog site where your observability data is located, such as **US1-East**. Read more about Datadog sites in [the documentation](https://docs.datadoghq.com/getting_started/site/#access-the-datadog-site)

    - `API Key`: A Datadog API key helps CloudAEye uniquely identify the organization. Read more about API keys in [the documentation](https://docs.datadoghq.com/account_management/api-app-keys/).

    - `Application Key`: In addition to an API key, CloudAEye needs a Datadog application key to programmatically access your data. Read more about application keys in [the documentation](https://docs.datadoghq.com/account_management/api-app-keys/).


- You can now explore your logs, metrics and traces data in the CloudAEye dashboard.

### Notification setup

To get notified about any incident:
1. On the [CloudAEye integration page][1], navigate to **Settings > Root Cause Analysis** from the side navigation drawer. 
2. Select the **Send Alerts** checkbox.
3. Choose or add the notification alert channel of your choice.


## Uninstallation

To remove the Datadog integration from CloudAEye:
1. From the side navigation drawer on the [CloudAEye integrations page][1], navigate to **Integrations > Datadog**.
2. Click **Remove**.
3. Click the **Uninstall Integration** button. Once you uninstall this integration, any previous authorizations are revoked.
4. Ensure that all API keys associated with this integration have been disabled by searching for the integration name (CloudAEye) on the [API keys management page][3].



## Support

Need help? Contact [CloudAEye support](mailto:support@cloudaeye.com).


## References

- Follow the [step-by-step guide](https://docs.cloudaeye.com/user-guide/integrations/datadog.html) in the CloudAEye docs to set up Datadog integration. 


[1]: https://console.cloudaeye.com/integrations/datadog
[2]: https://app.datadoghq.com/organization-settings/oauth-applications
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=CloudAEye