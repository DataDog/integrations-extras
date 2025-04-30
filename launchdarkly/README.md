# LaunchDarkly integration

## Overview

<!-- partial
{{% site-region region="gov" %}}
**The LaunchDarkly integration is not supported for the Datadog {{< region-param key="dd_site_name" >}} site**.
{{% /site-region %}}
partial -->

LaunchDarkly provides the following integrations with Datadog:

### Events integration

The [LaunchDarkly][1] events integration for Datadog brings flag event markers to your monitoring dashboards, so you can see the effects of your LaunchDarkly feature deployments on your customer's services or systems. For instance, if a deployed feature causes a service to slow down, you can see the cause within Datadog.

### Feature flag tracking integration

LaunchDarkly's feature flag tracking integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

### Relay proxy metrics integration

If you are using the [LaunchDarkly Relay Proxy][2], you can configure it to export metrics, such as active and cumulative connections, to Datadog.

## Setup

### Events integration

The LaunchDarkly events integration uses a [Datadog API key][3], which can be created by a Datadog admin. Once you obtain a Datadog API key, see the [LaunchDarkly documentation for the Datadog integration][4] to learn how to setup the LaunchDarkly events integration for Datadog.

### Feature flag tracking setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit the [Getting started with Feature Flag data in RUM][8] guide.

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

### Relay Proxy metrics

Follow the Relay Proxy's [Metrics integrations documentation][5] to configure this feature.

## Data Collected

### Metrics

The LaunchDarkly Relay Proxy can be configured to send the following metrics to Datadog:

- **`connections`**: The number of currently existing stream connections from SDKs to the Relay Proxy.
- **`newconnections`**: The cumulative number of stream connections that have been made to the Relay Proxy since it started up.
- **`requests`**: The cumulative number of requests received by all of the Relay Proxy's [service endpoints][6] (except for the status endpoint) since it started up.

### Events

The LaunchDarkly events integration sends flag, project, and environment events from LaunchDarkly to Datadog.

### Service Checks

The LaunchDarkly integration does not include any service checks.

## Support

Need help? Contact [Datadog Support][7].

## Further Reading

Learn more about [LaunchDarkly][1] and the [Datadog events integration][4].

[1]: https://launchdarkly.com
[2]: https://docs.launchdarkly.com/home/relay-proxy
[3]: /organization-settings/api-keys
[4]: https://docs.launchdarkly.com/integrations/datadog/events
[5]: https://github.com/launchdarkly/ld-relay/blob/v6/docs/metrics.md
[6]: https://github.com/launchdarkly/ld-relay/blob/v6/docs/endpoints.md
[7]: https://docs.datadoghq.com/help/
[8]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
