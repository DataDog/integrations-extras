# Instabug integration
## Overview

[Instabug][1]'s comprehensive platform empowers developers to monitor, prioritize, and debug performance and stability issues throughout the entire mobile app development lifecycle. Over 15,000 companies utilize the unmatched performance monitoring and crash reporting features, allowing their team of developers to leverage critical data in real time. Verizon, PayPal, eBay, and more of today's top-rated apps rely on our automated reports, alerts, and data solutions to boost their mobile app performance, prepare for smoother release cycles, and enable further developments and scalability.

On Datadog, Instabug provides a dashboard widget that will help you monitor your overall app health and how the user perceives your app’s performance with just one number, the App Apdex. Through the widget you will get:
- The overall App Apdex score
- App Apdex overtime
- Break down the sessions into 4 buckets (Satisfying, Tolerable, Frustrating or Crashing sessions)
- The latest 5 bug reports and the total number of new reports


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
