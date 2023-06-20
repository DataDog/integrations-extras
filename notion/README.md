# Agent Check: Notion

## Overview

Notion is a Connected Workspace. It's where modern teams create and share docs, take notes, manage projects, and organize knowledge, all in one place. Install Notion's integration with Datadog to manage and monitor your workspace activity in [Datadog Cloud SIEM][1]. You can import your workspace's audit logs for real-time monitoring, alerting, and analysis. From there, you can detect and investigate potential security issues, suspicious behavior, and troubleshoot access with confidence and ease.

## Setup

Datadog setup

Go to the Configuration tab and click Install Integration at the bottom.

Click Connect Accounts to redirect to Settings & Members in Notion

Login to Notion then navigate to Connections > Workspace Connections > +Add Connection > Datadog. 

Notion will prompt you to follow a series of OAuth steps to authorize the integration with Datadog.

Once connected, Notion will start sending near real-time data to Datadog.

## Uninstallation
Once this integration has been uninstalled, any previous authorizations are revoked.
Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][4].

In Notion navigate to Setting & Members > Connections > Workspace Connections > ... next to Datadog > Disconnect

## Data Collected

[Full list of events emitted from Notion][2]

## Support 
Need help? Contact [Notion Support][3]

[1]: https://docs.datadoghq.com/security/cloud_siem/
[2]: https://www.notion.so/notiondevs/SIEM-Integrations-Overview-309423e17dfa4c6d9a031cadff07ab6a?pvs=4#e384c9d013cb42cc9f98165730ab6f5c
[3]: mailto:team@makenotion.com
[4]: https://app.datadoghq.com/organization-settings/api-keys?filter=Notion
