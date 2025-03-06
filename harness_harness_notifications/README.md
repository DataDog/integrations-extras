# Harness Notifications

## Overview

Harness is a self-service CI/CD platform that allows engineers and DevOps to build, test, deploy, and verify software, on-demand. With this integration, you can seamlessly send Harness pipeline event notifications to Datadog, ensuring real-time visibility into critical pipeline updates within your existing monitoring workflows. These notifications are available in the Datadog [Events Explorer][1] and are shown in the out-of-the-box dashboard.

**Note**: The ability to configure Datadog notifications in Harness is behind a feature flag. Contact [Harness Support][2] to enable this feature. See the [Harness documentation][3] to learn more about this integration.

## Setup

After the integration is installed, these events are tagged with `source:harness_notifications`.

### Configure Datadog pipeline notifications in Harness

1. In Harness Pipeline studio, click **Notify** on the right sidebar.
2. Click **+ Notifications** to create a new channel.
3. Provide a name for your Datadog notification channel.
4. Select the Pipeline Events you want to monitor.
5. Under Notification Method, select **Datadog(/v1/events API)** as the Channel Type.
6. Enter your Datadog URL, which should be followed by `/api/v1/events` (for example, `https://app.datadoghq.com/api/v1/events/`)
7. Enter your [Datadog API key][4].
8. (Optional) Add headers if needed.
9. Test the configuration and click **Finish**.

## Uninstallation

Notification channels can be enabled, disabled, or deleted from the Notifications page.
-   To enable or disable notification rules, toggle the **Enabled** switch.
-   To delete, select **:** for more options, then click **Delete**.


## Support

Need help? Contact [Harness support][5].


[1]: https://docs.datadoghq.com/service_management/events/explorer/
[2]: mailto:support@harness.io
[3]: https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/notify-users-of-pipeline-events/#datadog-notifications
[4]: https://docs.datadoghq.com/account_management/api-app-keys/
[5]: https://www.harness.io/support