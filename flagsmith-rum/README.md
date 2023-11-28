# Agent Check: Flagsmith / Datadog RUM

## Overview

[Flagsmith][1] facilitates feature management across web, mobile, and server side applications.

The Datadog Flagsmith RUM integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

## Setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][2] guide.

1. Update your Browser RUM SDK version to 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize Flagsmith's SDK with the `datadogRum` option, which reports feature flag evaluations to Datadog using the snippet of code shown below.

```javascript
flagsmith.init({
     datadogRum: {
        client: datadogRum,
        trackTraits: true,
    },
    ...
})
```

## Troubleshooting

Need help? See the [Flagsmith documentation][3] or contact [Datadog Support][4].

[1]: https://flagsmith.com/
[2]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
[3]: https://docs.flagsmith.com/clients/javascript#datadog-rum-javascript-sdk-integration
[4]: https://docs.datadoghq.com/help/
