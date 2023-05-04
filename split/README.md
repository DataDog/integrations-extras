# Split

{{< callout url="#" btn_hidden="true" header="Join the Feature Flag Tracking Beta!">}}
To enrich your RUM data with your Split feature flags and get visibility into performance monitoring and behavioral changes, join the <a href="https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/">Feature Flag Tracking</a> private beta. To request access, contact Datadog Support at support@datadoghq.com.

{{< /callout >}}

## Overview

[Split][1] is a platform for [controlled rollouts][2], helping businesses of all sizes deliver exceptional user experiences and mitigate risk by providing an easy, secure way to target features to customers.

Integrate Split with Datadog to:

- See feature changes in context by including Split changelogs in your event stream
- Correlate feature impact with application performance
- Avoid critical issues before they happen. Disable features proactively based on Datadog metrics and alerts
- Enrich RUM data with your Split feature flags to get visibility into performance monitoring and behavioral changes

## Setup

- **In Datadog**: Create an API Key <span class="hidden-api-key">\${api_key}</span>

- **In Split**: Go to **Admin Settings** and click **Integrations** and navigate to the Marketplace. Click Add next to Datadog.<br/>

![Split Screenshot][3]

- Paste your Datadog API Key and click Save.

![Split Screenshot][4]

Split data should be flowing into Datadog.

### Feature Flag Tracking integration
Split's feature flag tracking integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][7] guide.

1. Update your Browser RUM SDK version to 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize Split's SDK and create an impression listener reporting feature flag evaluations to Datadog using the following snippet of code.

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

## Data Collected

### Metrics

The Split check does not include any metrics.

### Events

Push your Split listing/de-listing events into your [Datadog Event Stream][5].

### Service Checks

The Split check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: http://www.split.io
[2]: http://www.split.io/articles/controlled-rollout
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/split/images/in-split.png
[4]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/split/images/integrations-datadog.png
[5]: https://docs.datadoghq.com/events/
[6]: https://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
