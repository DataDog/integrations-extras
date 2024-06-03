# DevCycle integration

## Overview

DevCycle provides the following integrations with Datadog:

### Feature flag tracking integration

DevCycle's feature flag tracking integration enriches your RUM data with your feature's variable evaluations to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a specific user experience and if it is negatively affecting the user's performance.

## Setup

### Feature flag tracking setup

Feature flag tracking is available in the RUM Browser SDK. For detailed setup instructions, visit the [Getting started with Feature Flag data in RUM][4] guide.

1. Update your Browser RUM SDK version 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize DevCycle's SDK and subscribe to the `variableEvaluated` event, calling `addFeatureFlagEvaluation` from within the subscription callback.

```
// initialize the dvcClient

const user = { user_id: "my_user" };
const dvcOptions = { logLevel: "debug" };
const dvcClient = initialize("<DVC_CLIENT_SDK_KEY>", user, dvcOptions); 

// for all variable evaluations

dvcClient.subscribe(
    "variableEvaluated:*",
    (key, variable) => {
        datadogRum.addFeatureFlagEvaluation(key, variable.value);
    }
)

// for a particular variable's evaluations

dvcClient.subscribe(
    "variableEvaluated:my-variable-key",
    (key, variable) => {
        datadogRum.addFeatureFlagEvaluation(key, variable.value);
    }
)
```

## Data Collected

### Metrics

The DevCycle integration does not include any metrics.

### Events

The DevCycle integration does not include any events.

### Service Checks

The DevCycle integration does not include any service checks.

## Support

Need help? Contact [Datadog Support][3].

[1]: https://devcycle.com
[2]: https://docs.devcycle.com/tools-and-integrations/datadog-rum
[3]: https://docs.datadoghq.com/help/
[4]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/