# Instabug integration
## Overview

[Instabug][1] is a mobile-focused platform that empowers mobile teams to monitor, prioritize, and debug performance and stability issues throughout the mobile app development lifecycle.

The Instabug dashboard widget in Datadog helps you monitor your overall app health and how users perceive your app's performance with just one number, the App Apdex. The widget provides:
- The overall App Apdex score
- App Apdex overtime
- A breakdown of the sessions into four buckets (`Satisfying`, `Tolerable`, `Frustrating` or `Crashing` sessions)
- The five most recent bug reports and the total number of new reports


## Setup
1. If you haven't already, [Sign up for Instabug][2] for free and follow the steps to integrate the SDK into your app.
2. After integrating the Instabug SDK in your app, go to a new or existing [Datadog dashboard][4].
3. Press the **+ Edit Dashboard** button to expose the widget drawer.
4. Search for `Instabug` under the **Apps** tab of the widget drawer.
5. Click or drag the Instabug widget icon to add it to your dashboard and open the Instabug editor modal.
6. Authenticate and connect your Instabug account to Datadog by logging in with your Instabug credentials.
7. Optionally, give the widget a title.
8. Press **Save** to finish configuring the Datadog dashboard widget.

## Data Collected
The Instabug integration does not include any metrics.

## Service Checks
The Instabug integration does not include any service checks.

## Support
Need help? Contact [Instabug Support][3].

[1]: http://instabug.com
[2]: https://dashboard.instabug.com/signup
[3]: mailto:support@instabug.com
[4]: https://app.datadoghq.com/dashboard/lists
