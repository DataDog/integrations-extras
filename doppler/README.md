# Agent Check: Doppler

## Overview

[Doppler][1] is a secrets manager designed with both security and developer productivity in mind.
Doppler allows you to securely store secrets (for example: API keys, database credentials, and other sensitive values) and deliver them to your applications.

This integration allows Activity Logs from [Doppler][1] to be streamed to Datadog, allowing you to monitor changes to your workplace.

Doppler does not collect any data from your Datadog account.

### Installation

1. Click **Connect Accounts** on the Doppler integration tile to connect Datadog with Doppler.
2. Log into Doppler or create an account if you have not already.
3. Select the Doppler workplace that you would like to configure. This step will automatically be skipped if you only have one workplace.
4. Click **Settings** to navigate to your workplace settings.
5. Under **Logging Services** > **Datadog**, click **Connect**.
6. Choose your Datadog site from the Dropdown.
7. Log into Datadog. This step will be skipped if you are already signed in.
8. Review the Datadog permissions that will be granted to Doppler and click **Authorize**.

Once the installation is complete, Doppler Activity Logs will automatically start flowing to Datadog.

### Configuration

The integration will automatically send all Doppler Activity Logs to Datadog, no further configuration is available at this time.

### Validation

During installation, Doppler creates a test log to verify that the installed credentials work properly. Verify that this test log is present in your logs to verify the installation.

## Data Collected

Doppler does not collect any information from your Datadog account.

### Uninstallation

- Go to your [Doppler workplace settings][4] and disconnect the Datadog integration
- Remove all API keys associated with this integration by searching for the integration name on the [Datadog API Keys page][5].

### Metrics

Doppler does not report any metrics.

### Service Checks

Doppler does not provide any service checks.

### Logs

Doppler creates a log for every entry in your workplace's [Doppler Activity Log][2]. The type of log, as well as any associated log parameters, will be included in the payload.

### Events

Doppler does not produce any Datadog events.

## Troubleshooting

Need help? Contact [Doppler support][3].

[1]: https://www.doppler.com
[2]: https://docs.doppler.com/docs/workplace-logs
[3]: https://support.doppler.com
[4]: https://dashboard.doppler.com/workplace/settings
[5]: https://app.datadoghq.com/organization-settings/api-keys
