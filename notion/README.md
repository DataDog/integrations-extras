# Agent Check: Notion

## Overview

Notion is a Connected Workspace. It's where modern teams create and share docs, take notes, manage projects, and organize knowledge, all in one place. Install Notion's integration with Datadog to manage and monitor your workspace activity in [Datadog Cloud SIEM][1]. You can import your workspace's audit logs for real-time monitoring, alerting, and analysis. From there, you can detect and investigate potential security issues, suspicious behavior, and troubleshoot access with confidence and ease.

To see the full list of events emitted by Notion, see our [documentation][2].

## Setup

1. Open the Notion tile and click _Install Integration_.

2. Click _Connect Accounts_ to redirect to _Settings & Members_ in Notion.

3. Login to Notion, then navigate to _Connections_ > _Workspace Connections_ > _+Add Connection_ > _Datadog_. 

4. Notion prompts you to follow a series of OAuth steps to authorize the integration with Datadog.

Once connected, Notion starts sending near real-time data to Datadog.

## Uninstallation
Once this integration has been uninstalled, any previous authorizations are revoked.
Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][4].

In Notion navigate to Setting & Members > Connections > Workspace Connections > ... next to Datadog > Disconnect

## Support 
Need help? Contact [Notion Support][3]

[1]: https://docs.datadoghq.com/security/cloud_siem/
[2]: https://www.notion.so/notiondevs/SIEM-Integrations-Overview-309423e17dfa4c6d9a031cadff07ab6a?pvs=4#e384c9d013cb42cc9f98165730ab6f5c
[3]: mailto:team@makenotion.com
[4]: https://app.datadoghq.com/organization-settings/api-keys?filter=Notion
