# Modal

## Overview

[Modal][1] lets you run generative AI models, large-scale batch jobs, job
queues, and much more. This integration collects metrics (CPU, memory
or GPU use for example) and logs (stdout/stderr logging from your modal
applications, or audit logs for your account) that you can visualize through Datadog
dashboards and set up alerts for with Datadog monitors.

## Setup

### Installation

To set up the Modal integration:

1. Navigate to the [**Modal** tile][2] on the Datadog Integrations page and
   click **Install Integration**.

2. Click **Connect Accounts** to begin authorization of this integration. You
   will be redirected to log into [Modal][1], and once logged in, you'll be
   redirected to the Datadog authorization page.

3. Click the **Authorize** button to complete setup.

Logs and metrics from your Modal apps should now start appearing in Datadog.

## Data Collected

### Metrics

Modal collects GPU, CPU, and memory utilization metrics for
applications/functions that run on Modal.

### Logs

Modal collects audit logs and all application logs (all stdout/stderr logging).

### Events

Modal does not include any events.

## Uninstallation

Once this integration has been uninstalled, any previous authorizations are
revoked and logs/metrics stop being emitted to Datadog.

1. On the **Configure** tab in the **Modal** integration tile in Datadog, click **Uninstall Integration**.

2. Ensure that all API keys associated with this integration have been disabled
   by searching for the integration name on the [API Keys page][4].

## Troubleshooting

Need help? Contact [Modal support][3].

[1]: https://modal.com
[2]: https://app.datadoghq.com/integrations?integrationId=modal
[3]: mailto:support@modal.com
[4]: https://app.datadoghq.com/organization-settings/api-keys?filter=Modal

