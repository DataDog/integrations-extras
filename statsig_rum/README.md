# Agent Check: statsig-rum

## Overview

Statsig is a modern feature management and experimentation platform that empowers teams to 10x their experimentation velocity, shipping every feature in a data-driven way. Statsig's feature flag tracking integration enriches your Datadog RUM data with feature gate information, allowing you to measure causality between your product features and your system and performance metrics to derisk your product releases. 

## Setup

### Feature flag tracking setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit [Getting started with feature flag data in RUM](https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection).

1. Update your Browser RUM SDK version 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize Statsig's SDK (`>= v4.34.0`) and implement the `gateEvaluationCallback` option as shown below:

```js
await statsig.initialize('client-<STATSIG CLIENT KEY>',
  {userID: '<USER ID>'},
  {     
    gateEvaluationCallback: (key, value) => {
      datadogRum.addFeatureFlagEvaluation(key, value);
    }
  }
); 
```