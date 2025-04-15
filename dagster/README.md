# Dagster+

## Overview

Dagster is a next-generation open-source orchestration platform designed for building, running, and monitoring data asset workflows. The Dagster+ integration streams [event logs][1] to Datadog and includes an out-of-the-box log pipeline and dashboard.

## Setup

1. Click **Connect Accounts** to launch the OAuth flow and link your Dagster and Datadog accounts.

2. Log in to Dagster+ using the account you want to use for this integration.

3. When redirected to Datadog, click **Authorize** to grant Dagster+ permission to create an API key for sending logs to your Datadog account.

### Validation

Within 10 minutes of completing the integration setup, the Dagster Overview dashboard starts showing new log events, provided there are any active Dagster jobs emitting events.

## Uninstallation

1. Navigate to the Dagster+ integration tile and click **Uninstall Integration**.

2. After uninstalling the integration, all previous authorizations are revoked.

3. Disable all API keys associated with this integration by searching for the integration name on the [API Keys page][2].

## Support

Need help? Contact [Dagster support][3].


[1]: https://docs.dagster.io/guides/monitor/logging
[2]: https://github.com/DataDog/integrations-extras/blob/master/organization-settings/api-keys?filter=Dagster
[3]: https://dagster.io/support