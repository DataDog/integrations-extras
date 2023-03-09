# Agent Check: Flagsmith

{{< callout url="#" btn_hidden="true" header="Join the Feature Flag Tracking Beta!">}}
To enrich your RUM data with your Flagsmith feature flags and get visibility into performance monitoring and behavioral changes, join the <a href="https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/">Feature Flag Tracking</a> private beta. To request access, contact Datadog Support at support@datadoghq.com.

{{< /callout >}}

## Overview

[Flagsmith][1] facilitates feature management across web, mobile, and server side applications. The Datadog Flagsmith integration enables you to view information about flag changes directly within Datadog.

Flagsmith provides the following integrations with Datadog:

### Events integration

All flag change events are sent to Datadog. These events are tagged with the environment they were changed in.

### Feature flag tracking integration

Flagsmith's feature flag tracking integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

## Setup

In the [Flagsmith Dashboard][2], select the Integrations Menu and then add the Datadog Integration. Enter your [Datadog API Key][3]. For Base URL, enter `https://api.datadoghq.com` if you are using the US Datadog site, or `https://api.datadoghq.eu` if you are using the EU Datadog site.

### Feature flag tracking setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][6] guide.

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

## Data Collected

### Metrics

The Flagsmith integration does not include any metrics.

### Service Checks

The Flagsmith integration does not include any service checks.

### Events

All Flagsmith events are sent to the Datadog event stream.

## Troubleshooting

Need help? See the [Flagsmith documentation][4] or contact [Datadog Support][5].

[1]: https://www.flagsmith.com/
[2]: https://app.flagsmith.com/
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://docs.flagsmith.com/integrations/datadog/
[5]: https://docs.datadoghq.com/help/
[6]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/