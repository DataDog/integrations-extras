# CloudAEye

## Overview

Kosal from CloudAEye is your root cause co-pilot. It analyzes your observability data (logs, metrics, traces) and pin-points the root cause automatically. Kosal publishes events with a summary to an integrated dashboard that helps to identify incidents faster. Additionally, Kosal adeptly identifies similar issues within Jira and related code changes that may be causing the incident. Using this integration you may troubleshoot and resolve incidents faster which improves your mean time to repair (MTTR).

## Setup

### Installation

- Search for CloudAEye in the integrations page.
- Click on **Install Integration** button.
- Once installed, click on **Connect Accounts** button which will take you to the [CloudAEye integrations page][1] (Side Navigation Drawer => Integrations => Datadog).
- Add a Datadog integration. You may have to create your CloudAEye account if you don't have one.
- Once the keys are populated, your Datadog account will get connected to the CloudAEye.

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