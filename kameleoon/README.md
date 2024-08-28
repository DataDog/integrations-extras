## Overview

Kameleoon empowers teams to manage and optimize feature releases across web, mobile, and server-side applications with precision.

Integrate with Datadog RUM to monitor feature deployments and releases with real-time performance data, helping you understand the direct impact of specific features on user behavior and application metrics.

## Setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit [Getting started with feature flag data in RUM][1].

1. Update your Browser RUM SDK version to 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize [Kameleoon's SDK][2] and define `onEvent` handler to watch `Evaluation` events.

```javascript
client.onEvent(EventType.Evaluation, ({ featureKey, variation }) => {
  datadogRum.addFeatureFlagEvaluation(featureKey, variation.key);
});
```

## Support

For more information see [Kameleoon SDK documentation][2] or join [Kameleoon Slack community][3] for support on Kameeloon Datadog integration.

[1]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
[2]: https://developers.kameleoon.com/feature-management-and-experimentation/web-sdks/js-sdk/
[3]: https://join.slack.com/t/kameleooncommunity/shared_invite/zt-1s6m8s09e-~yA1EUgn5pLWW_mrgf8TrQ
