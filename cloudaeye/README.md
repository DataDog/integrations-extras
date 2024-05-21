# CloudAEye

## Overview

Kosal automates root cause analysis (RCA), significantly improving incident resolution time and streamlining the experience for engineers. This AI-powered workflow replaces manual tasks that engineers currently handle by analyzing data - logs, metrics, traces - and pin-pointing the root cause with relevant context. As a result, engineers can redirect their focus to more critical aspects. Additionally, Kosal adeptly identifies historical issues within Jira and traces related code changes that may lie at the heart of the problem.

## Setup

### Installation

Visit [CloudAEye][4] to sign up for free. Once registered, visit the [CloudAEye integrations page][1] and add a Datadog integration. This guides you through the Datadog OAUTH2 flow to grant CloudAEye access to your traces, logs, and metrics data.

### Configuration

Once integrated, begin exploring your Datadog costs within CloudAEye. You can create filters for specific Datadog organizations and services alongside costs from any of the other supported CloudAEye providers.

## Uninstallation

To remove the Datadog integration from CloudAEye, navigate to the [CloudAEye integrations page][1] and click **Remove**. Additionally, uninstall this integration from Datadog by clicking the **Uninstall Integration** button below. Once you uninstall this integration, any previous authorizations are revoked. 

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page][3].

## Support

Need help? Contact [CloudAEye support](mailto:support@cloudaeye.com).


[1]: https://console.cloudaeye.com/integrations/datadog
[2]: https://app.datadoghq.com/organization-settings/oauth-applications
[3]: https://app.datadoghq.com/organization-settings/api-keys?filter=CloudAEye
[4]: https://console.cloudaeye.com
