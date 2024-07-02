# Agent Check: Fauna

## Overview

Fauna is a fully managed, distributed document-relational database. With this integration, you can stream your Fauna database query logs into Datadog. This enables you to view your queries in real time, and you can see the following information about your queries:
1. Fauna Cost Measures
   1. Read Ops
   2. Write Ops
   3. Compute Ops
2. Query Time
3. Query Size Measures
   1. Request and response size
4. Query shape
   1. The full request body with Personal Identifiable Data removed.
5. Query response code

For the full list of fields available in the logs, see the [Fauna Query Log Record Format][1].

## Setup

### Installation

1. Click the 'Connect Accounts' button on the [Fauna integration tile][3] to start the OAuth flow and connect your Fauna and Datadog accounts.
2. Once directed to Fauna, login with the account you'd like to connect. You can skip this step if you're already logged into your Fauna account.
3. You are redirected to the Fauna Create Integration page, where you can select the region group(s) or databases that you would like to stream logs into Datadog for. Then, click **Create**.
4. When directed to Datadog, click **Authorize** to authorize Fauna to create an API key for your account that will be used to send the database query logs.

Once this flow is complete, you are redirected to the [Fauna Integrations Page][2], which shows your active integration.

Within the next ten minutes, the [Fauna Overview Dashboard][7] will begin showing metrics for any queries issued for the configured region group(s) or databases.
The above issued queries should also start appearing in the [Datadog Log Explorer][4] under the 'fauna' service.

### Configuration

You can configure the following settings for the Fauna integration:

1. Which region groups database query logs are sent to.
   1. If a region group is enabled for the integration, query logs are sent for every database in the enabled region group.
2. Which databases query logs are sent from.
3. The integration state (Active or Paused). When Paused, logs are not sent.

Visit the [Fauna Integrations Page][2] to update any configuration settings or to remove your integration.

It can take up to ten minutes to see your updates take effect in the [Fauna Overview Dashboard][7] and [Datadog Log Explorer][4].

### Validation

Once configured correctly, within ten minutes you should see metrics in the [Fauna Overview Dashboard][7] and queries in the [Datadog Log Explorer][4] under the 'fauna' service.

### Uninstallation
 - Visit the [Fauna Integrations Page][2] and remove the Datadog integration.
 - Once this integration has been uninstalled, any previous authorizations are revoked.
 - Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][5].

## Data Collected

### Logs

Fauna includes logs for every query within the databases configured in the integration.
If the integration is configured with a region group, then query logs for all databases within the region group are included.

## Troubleshooting

Need help? Contact [Fauna support][6].

[1]: https://docs.fauna.com/fauna/current/tools/query_log/reference/log_reference
[2]: https://dashboard.fauna.com/resources/integrations
[3]: https://app.datadoghq.com/integrations/fauna
[4]: https://docs.datadoghq.com/logs/explorer/
[5]: https://app.datadoghq.com/organization-settings/api-keys
[6]: mailto:support@fauna.com
[7]: https://app.datadoghq.com/dashboard/lists?q=Fauna%20Overview
