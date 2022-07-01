# Android Integration

## Overview

With the Datadog [Android integration][1], you can spend less time triaging issues and more time releasing new features by:

- Debugging the root cause of slow performance issues and application crashes in third-party libraries, network requests, or large media files
- Improving application responsiveness, setting up service level indicators (SLIs), and diagnosing issues with out-of-the-box dashboards, real-time metrics, and deobfuscated crash reports
- Intelligently grouping high-volume application errors into a manageable set of unique issues

Correlate the impact of the user experience on your business by:

- Analyzing critical mobile user experience data such as screen engagement by demographics, version releases, or any custom attributes, to reach your business KPIs
- Automatically correlating every user journey with a timeline of session events and attributes including ID, cellular activity, referral URL, and more
- Understanding user behavior trends with customizable analytics and geographical maps

Monitor the end-to-end health of your application by:

- Pivoting from your user experience data to backend traces, runtime metrics, and logs for the complete context when investigating issues
- Debugging crashes faster by unifying client-side and server-side metrics, traces, and logs
- Unifying full-stack monitoring in a single platform for frontend and backend teams

## Setup

### Collect RUM events

To start collecting Real User Monitoring events from your application, see [Android and Android TV Monitoring][2].

### Collect traces

To start sending your Android application's traces to Datadog, see [Connect RUM and Traces][3].

### Collect logs

To start forwarding your Android application's logs to Datadog, see [Android Log Collection][4].

## Data Collected

### Metrics

The Android integration does not include any metrics. To generate custom metrics from your RUM application, see [Generate Metrics][5]. 

### Events

For more information about events and attributes, see [RUM Android Data Collected][6].

### Service Checks

The Android integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog Support][7].

## Further Reading

Additional helpful documentation, links, and articles:

- [Android and Android TV Monitoring][8]

[1]: https://app.datadoghq.com/integrations/rum-android
[2]: https://docs.datadoghq.com/real_user_monitoring/android/?tabs=kotlin#setup
[3]: https://docs.datadoghq.com/real_user_monitoring/connect_rum_and_traces?tab=androidrum#setup-rum
[4]: https://docs.datadoghq.com/logs/log_collection/android/?tab=kotlin
[5]: https://docs.datadoghq.com/real_user_monitoring/generate_metrics
[6]: https://docs.datadoghq.com/real_user_monitoring/android/data_collected/
[7]: https://docs.datadoghq.com/help/
[8]: https://docs.datadoghq.com/real_user_monitoring/android/