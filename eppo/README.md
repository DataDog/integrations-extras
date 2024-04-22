# Agent Check: Eppo / Datadog RUM

## Overview

[Eppo][1] is the experimentation and feature management platform that makes advanced A/B testing accessible to everyone in your organization.

The Datadog Eppo RUM integration enriches your Datadog RUM data with your feature flag information, including flag name and variation, to provide visibility into performance monitoring and behavioral changes. You can use this to determine which users are shown a feature and if it is negatively affecting the user's performance.

## Setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][2] guide.

1. Update your Browser RUM SDK version to 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize Eppo's SDK with the `datadogRum` option, which reports feature flag evaluations to Datadog. 

The following is a JavaScript example:

```typescript
const assignmentLogger: IAssignmentLogger = {
  logAssignment(assignment) {
    // Send the assignment event to customers' event logging
    analytics.track({
      userId: assignment.subject,
      event: "Eppo Randomized Assignment",
      type: "track",
      properties: { ...assignment },
    });

    // Assuming `exposure` is defined in this context and has a property `variation`
    datadogRum.addFeatureFlagEvaluation(assignment.experiment, exposure.variation);
  },
};

await eppoInit({
  apiKey: "<API_KEY>",
  assignmentLogger,
});
```

## Troubleshooting

Need help? See the [Eppo documentation][3].

[1]: https://www.geteppo.com/
[2]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
[3]: https://docs.geteppo.com/sdks/datadog