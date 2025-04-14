# Dagster+

## Overview

Dagster is a next-generation open source orchestration platform for the development, production, and observation of data assets. The Dagster+ integration provides the Dagster [EventLog][1] as Datadog logs, allowing you to build log pipelines, dashboards, and metrics based on Dagster events.

[1]: https://docs.dagster.io/guides/monitor/logging

## Setup

1. Click the 'Connect Accounts' button to start the OAuth flow and connect your Dagster and Datadog accounts.
2. Once directed to Dagster+, login with the account you'd like to use for the Datadog integration.
3. When directed to Datadog, click **Authorize** to authorize Dagster+ to create an API key to send the logs to your Datadog account.

### Validation

Within the next ten minutes, the Dagster Overview Dashboard will begin showing new log events if there are any active Dagster jobs emitting events.

## Uninstallation

 - Visit the Dagster+ integration tile and click the "Uninstall Integration" button.
 - Once this integration has been uninstalled, any previous authorizations are revoked.
 - Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys page][2].

[2]: https://app.datadoghq.com/organization-settings/api-keys

## Support

For any issues, visit [our support page.][1]


[1]: https://dagster.io/support