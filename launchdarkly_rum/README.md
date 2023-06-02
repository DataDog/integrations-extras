# LaunchDarkly Feature flag tracking integration

## Overview

LaunchDarkly's feature flag tracking integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

## Setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][9] guide.

1. Update your Browser RUM SDK version 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize LaunchDarkly's SDK and create an inspector reporting feature flag evaluations to Datadog using the snippet of code shown below.

```
const client = LDClient.initialize("<APP_KEY>", "<USER_ID>", {
  inspectors: [
    {
      type: "flag-used",
      name: "dd-inspector",
      method: (key: string, detail: LDClient.LDEvaluationDetail) => {
        datadogRum.addFeatureFlagEvaluation(key, detail.value);
      },
    },
  ],
});
```
## Further Reading

Learn more about [LaunchDarkly][1] and the [Datadog feature flag tracking integration][4].

[1]: https://launchdarkly.com
[2]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
