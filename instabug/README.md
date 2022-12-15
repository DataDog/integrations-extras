# Instabug integration
## Overview

[Instabug][1] helps mobile teams proactively improve the quality of their mobile apps and deliver a high-quality experience to end users. You can use APM, Crash Reporting, and Bug Reporting tools to help optimize your app's performance and improve the end-user experience.

Instabug provides a dashboard widget for Datadog dashboards that helps monitor your overall app health and how users perceive your app's performance with just one number, the App Apdex. The widget provides:
- The overall App Apdex score.
- The App Apdex overtime.
- A breakdown of the sessions into four buckets (`Satisfying`, `Tolerable`, `Frustrating` or `Crashing` sessions).
- The five latest bug reports and the total number of new reports.

## Setup
1. If you haven't already, [Signup for Instabug][2] for free and follow the steps to integrate the SDK into your app.
2. After integrating the Instabug SDK in your app, go to a new or existing Datadog dashboard.
3. Press the **Add Widgets** button to expose the widget drawer.
4. Search for `Instabug` to find the Instabug widget in the Apps section of the widget drawer.
5. Click or drag the Instabug widget icon to add it to your dashboard and open the Instabug editor modal.
6. Authenticate and connect your Instabug account to Datadog by logging in with your credentials.
7. Optionally, give the widget a title.
8. Press **Save** to finish configuring the Datadog dashboard widget.

## Data Collected
The Instabug integration does not include any metrics.

## Service Checks
The Instabug integration does not include any service checks.

## Support
Need help? Contact [Datadog Support][3].

[1]: http://instabug.com
[2]: https://dashboard.instabug.com/signup
[3]: https://docs.datadoghq.com/help/
