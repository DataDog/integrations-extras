# Agent Check: Fauna

## Overview

Fauna is a fully managed, distributed document-relational database. With this integration, Fauna users can stream their 
database query logs into Datadog. This allows customers to view their queries in near real-time, allowing users to see
the following for their queries:
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

1. Use the 'Connect Accounts' button to begin the oauth flow to connect your Fauna and Datadog account.
2. Once directed to Fauna, login with the account you'd like to connect.
   1. this step can be skipped if already logged into your Fauna account.
3. You will be directed to the Fauna Create Integration page, from here, select the region group(s) or databases that you would like to stream logs into Datadog for and click create.
4. When directed to Datadog, click Authorize to authorize Fauna to create an API key for your account that will be used to send the database query logs.

Once this flow is complete it will redirect you to the [Fauna Integrations Page][2] showing your active integration.
Within the next 10 minutes, any queries issued for the configured region group(s) or databases should now show up in the 
Datadog Log Explorer under the 'fauna' service.

### Configuration

Fauna allows configuring the following on your Datadog integration:
1. Which region groups that database query logs are sent for.
   1. If a region group is enabled for the integration, query logs are sent for every database in the enabled region group.
2. Which databases that query logs are sent for.
3. The integration state, Active or Paused. When Paused no logs will be sent.

Visit the [Fauna Integrations Page][2] to update any of the configuration or to remove your integration.

It can take up to 10 minutes to see your updates take effect in the Datadog Log Explorer.

### Validation

Once configured correctly, you should begin seeing your queries showing up in the Datadog Log Explorer under the 'fauna' service.

### Uninstallation
 - Visit the [Fauna Integrations Page][2] and remove the Datadog integration.
 - Once this integration has been uninstalled, any previous authorizations are revoked.
 - Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.

## Data Collected

### Logs

Fauna will include logs for every query for the databases configured in the integration. 
If the integration is configured with a region group, then query logs for all databases within the region group are included.

## Troubleshooting

Need help? Contact [Fauna support](mailto:support@fauna.com).

[1]: https://docs.fauna.com/fauna/current/tools/query_log/reference/log_reference
[2]: https://dashboard.fauna.com/resources/integrations
