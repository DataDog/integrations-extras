# Agent Check: Fauna

## Overview

This integration allows Fauna users to import their database query logs into Datadog. Users are able to configure it for specific databases or for entire region groups. When enabled all requests made to fauna matching the database or region group configuration will show up in Datadog logs under the fauna service.
To see what fields are included, see the [Fauna Query Log Record Format][1].

## Setup

### Installation

Use the 'Connect Accounts' button above to connect your Fauna and Datadog account. This will allow Fauna to send logs to your Datadog account and will take you through a brief configuration process.


### Configuration

Once your accounts are connected, you can visit the [Fauna Integrations Page][2] to modify the integration configuration.

### Validation

Once configured correctly, you should begin seeing your queries showing up in the Datadog Log Explorer!

### Uninstallation
 - Visit the [Fauna Integrations Page][2] and remove the Datadog integration.
 - Once this integration has been uninstalled, any previous authorizations are revoked.
 - Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the API Keys page.

## Data Collected

### Logs

Fauna will include logs for every query for the databases configured in the integration. If the integration is configured with a region group, then query logs for all databases within the region group are included.

## Troubleshooting

Need help? Contact [Fauna support](mailto:support@fauna.com).

[1]: https://docs.fauna.com/fauna/current/tools/query_log/reference/log_reference
[2]: https://dashboard.fauna.com/resources/integrations
