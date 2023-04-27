# Agent Check: Flagsmith

{{< callout url="#" btn_hidden="true" header="Join the Feature Flag Tracking Beta!">}}
To enrich your RUM data with your Flagsmith feature flags and get visibility into performance monitoring and behavioral changes, join the <a href="https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/">Feature Flag Tracking</a> private beta. To request access, contact Datadog Support at support@datadoghq.com.

{{< /callout >}}

## Overview

[Flagsmith][1] facilitates feature management across web, mobile, and server side applications.

The Datadog Flagsmith RUM integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

### Feature flag tracking setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][1] guide.

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

Need help? See the [Flagsmith documentation][4] or contact [Datadog Support][2].

[1]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
[2]: https://docs.datadoghq.com/help/
