# Agent Check: Doppler

## Overview

[Doppler][1] is a secrets manager designed with both security and developer productivity in mind.

This integration allows Activity Logs from [Doppler][1] to be streamed to Datadog, allowing you to monitor changes to your workplace.

## Setup

1. Click **Connect Accounts** on the Doppler integration tile to connect Datadog with Doppler.
2. Log into Doppler or create an account if you have not already.
3. Select the Doppler workplace that you would like to configure. This step will automatically be skipped if you only have one workplace.

Once the installation is complete, Doppler Activity Logs will automatically start flowing to Datadog.

### Configuration

The integration will automatically send all Doppler Activity Logs to Datadog, no further configuration is available at this time.

### Validation

During installation, Doppler creates a test log to verify that the installed credentials work properly. Verify that this test log is present in your logs to verify the installation.

### Uninstallation

- Go to your [Doppler workplace settings][4] and disconnect the Datadog integration
- Remove all API keys associated with this integration by searching for the integration name on the [Datadog API Keys page][5].

## Data Collected

### Logs

Doppler creates a log for every entry in your workplace's [Doppler Activity Log][2]. The type of log, as well as any associated log parameters, will be included in the payload.

## Support

Need help? Contact [Doppler support][3].

[1]: https://www.doppler.com
[2]: https://docs.doppler.com/docs/workplace-logs
[3]: https://support.doppler.com
[4]: https://dashboard.doppler.com/workplace/settings
[5]: https://app.datadoghq.com/organization-settings/api-keys
