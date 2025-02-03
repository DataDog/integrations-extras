# Harness Notifications

## Overview

The Datadog Notifications in Harness allows you to send pipeline event notifications directly to your Datadog monitoring system using the [Events API (v1)][1]. This integration helps you keep track of important pipeline updates within your existing monitoring workflows. [Learn more][2]

Please note, currently, the Datadog notifications feature is behind the feature flag `PIPE_DATADOG_NOTIFICATIONS`. Please, contact [Harness Support][3] to enable this feature in Harness.

## Setup

The **Harness Notifications** integration allows you to send pipeline event notifications directly to the Events Explorer in Datadog. Once installed, these events will be tagged with `source:harness_notifications`

## [Configure Datadog pipeline notifications in Harness][4]

1. In Harness Pipeline studio, click on Notify on the right sidebar.
2. Click on `+ Notifications` button to create a new channel.
2. Give a name to your Datadog notification channel.
2. Select Pipeline Events as per your requirements.
3. Select Channel type as `Datadog(/v1/events API)` in Notification Method.
    ![datadog-selection][5]

4. Provide the Datadog URL and API key.: Please provide the Datadog URL followed by `/api/v1/events` eg. `https://app.datadoghq.com/api/v1/events/`
    ![datadog-API-and-URL][6]

5. (Optional) Add headers if needed.
6. Test and complete the setup.

For details, check Datadog's documentation on [Events API (v1)][1].

## Uninstallation

## [Disable notification rule][8]

Once you've created notification rules, you can enable/disable them in the Notifications page.

![](https://developer.harness.io/assets/images/notify-users-of-pipeline-events-11-e5c8b04889195bd974ef6ab87aacc9a3.png)

## Support

Need help? Contact [Harness support][9].


[1]: https://docs.datadoghq.com/api/latest/events/
[2]: https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/notify-users-of-pipeline-events/#datadog-notifications
[3]: mailto:support@harness.io
[4]: https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/notify-users-of-pipeline-events/#configuration "Direct link to Configuration"
[5]: https://developer.harness.io/assets/images/datadog-notification-1-b8800da49d5f75575040d229094e9c64.png
[6]: https://developer.harness.io/assets/images/datadog-api-conf-bbc150afdeb25c7693f17a6c8aa04c75.png
[8]: https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/notify-users-of-pipeline-events/#enable-or-disable-notification-rules "Direct link to Enable or disable notification rules"
[9]: https://www.harness.io/support