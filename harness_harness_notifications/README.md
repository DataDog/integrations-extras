# Harness Notifications

## Overview

Harness is a **self-service CI/CD platform** that allows engineers and DevOps to build, test, deploy, and verify software, on-demand.
With this integration, you can seamlessly send Harness pipeline event notifications to Datadog, ensuring real-time visibility into critical pipeline updates within your existing monitoring workflows. These notifications are available in the Datadog [Events Explorer][1] and are surfaced in the included dashboard. [Learn more][2]

**Note**: The ability to configure Datadog notifications in Harness is currently behind a feature flag. Please contact [Harness Support][3] to enable this feature

## Setup

After the integration is installed, these events are tagged with `source:harness_notifications`.

### Configure Datadog pipeline notifications in Harness

1. In Harness Pipeline studio, click on Notify on the right sidebar.
2. Click the `+ Notifications` button to create a new channel.
3. Provide a name for your Datadog notification channel.
4. Select the Pipeline Events you want to monitor.
5. Under Notification Method, select `Datadog(/v1/events API)` as the Channel Type.
    ![datadog-selection][4]

6. Enter your Datadog URL, which should be followed by `/api/v1/events` (e.g., `https://app.datadoghq.com/api/v1/events/`)
7. Enter your [Datadog API key][5].
    ![datadog-API-and-URL][6]

8. (Optional) Add headers if needed.
9. Test the configuration and click **Finish**.

## Uninstallation

## Disable notification rule

You can enable or disable notification rules from the Notifications page.

## Delete notification rule

You can delete a notification rule by clicking on **More options (:)** and then **Delete**. 

![](https://developer.harness.io/assets/images/notify-users-of-pipeline-events-11-e5c8b04889195bd974ef6ab87aacc9a3.png)

## Support

Need help? Contact [Harness support][7].


[1]: https://docs.datadoghq.com/service_management/events/explorer/
[2]: https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/notify-users-of-pipeline-events/#datadog-notifications
[3]: mailto:support@harness.io
[4]: https://developer.harness.io/assets/images/datadog-notification-1-b8800da49d5f75575040d229094e9c64.png
[5]: https://docs.datadoghq.com/account_management/api-app-keys/
[6]: https://developer.harness.io/assets/images/datadog-api-conf-bbc150afdeb25c7693f17a6c8aa04c75.png
[7]: https://www.harness.io/support