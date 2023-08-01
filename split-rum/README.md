
## Overview

[Split][1] is an Intelligent Feature Management [platform][2] that pairs the speed and reliability of feature flags with data to measure the impact of every feature. With Split, organizations have a secure way to release features, target them to customers, and measure the impact of features on their customer experience metrics.

With The Datadog Split RUM integration, product teams can view feature flag information overlaid on RUM data. This enables proactive monitoring of the real-time activity and experience of individual users and, if necessary, quick roll back or shut off of features that may be causing degradations.

## Setup

Feature flag tracking is available in the RUM Browser SDK. For detailed setup instructions, see the [Getting started with Feature Flag data in RUM][3] guide.

1. Update your Browser RUM SDK version to 4.25.0 or later.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize Split SDK and create an impression listener, reporting feature flag evaluations to Datadog using the following snippet of code:


```javascript
const factory = SplitFactory({
    core: {
      authorizationKey: "<APP_KEY>",
      key: "<USER_ID>",
    },
    impressionListener: {
      logImpression(impressionData) {              
          datadogRum
              .addFeatureFlagEvaluation(
                   impressionData.impression.feature,
                   impressionData.impression.treatment
              );
     },
  },
});

const client = factory.client();
```

## Troubleshooting

Need help? See [Split JavaScript SDK documentation documentation][4] or contact [Datadog Support][5].

[1]: https://split.io
[2]: https://www.split.io/product/
[3]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
[4]: https://help.split.io/hc/en-us/articles/360020448791-JavaScript-SDK#2-instantiate-the-sdk-and-create-a-new-split-client
[5]: https://docs.datadoghq.com/help/
