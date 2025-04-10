# Dagster+

## Overview

Dagster is a next-generation open source orchestration platform for the development, production, and observation of data assets. The Dagster+ integration provides the Dagster [EventLog][1] as Datadog logs, allowing you to build log pipelines, dashboards, and metrics based on Dagster events.

## Setup

### Installation

1. Click the 'Connect Accounts' button on the [Dagster+ integration tile][2] to start the OAuth flow and connect your Dagster and Datadog accounts.
2. Once directed to Dagster+, login with the account you'd like to use for the Datadog integration.
3. When directed to Datadog, click **Authorize** to authorize Dagster+ to create an API key to send the logs to your Datadog account.

### Validation

Within the next ten minutes, the [Dagster Overview Dashboard][3] will begin showing new log events if there are any active Dagster jobs emitting event.s

### Uninstallation
 - Visit the [Dagster+ integration tile][2] and click the "Uninstall Integration" button.
 - Once this integration has been uninstalled, any previous authorizations are revoked.
 - Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][4].

## Data Collected

### Logs

- [Dagster EventLog][1]

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://docs.dagster.io/guides/monitor/logging
[2]: https://app.datadoghq.com/dashboard/lists?q=Dagster+%20Overview
[3]: https://app.datadoghq.com/integrations/dagster-plus
[4]: https://app.datadoghq.com/organization-settings/api-keys
[5]: https://docs.datadoghq.com/help/