# LaunchDarkly integration

## Overview

LaunchDarkly provides the following integrations with Datadog: 

### Events integration

The [LaunchDarkly][1] events integration for Datadog brings flag event markers to your monitoring dashboards, so you can see the effects of your LaunchDarkly feature deployments on your customer's services or systems. For instance, if a deployed feature causes a service to slow down, you can see the cause within Datadog. 

### Dashboard widget

LaunchDarkly's dashboard widget lets you pin a subset feature flag targeting toggles to your Datadog dashboards to seamlessly monitor and perform a feature go-live from a single window.

### Relay proxy metrics integration

If you are using the [LaunchDarkly Relay Proxy](2), you can configure it to export metrics, such as active and cumulative connections, to Datadog.
## Setup

### Events integration

The LaunchDarkly events integration uses a [Datadog API key][3], which can be created by a Datadog admin. Once you obtain a Datadog API key, visit the [LaunchDarkly documentation for the Datadog integration][4] to learn how to setup the LaunchDarkly events integration for Datadog.

### Dashboard widget

1. In Datadog, navigate to an existing dashboard or create a new one.
2. Press the **Add Widgets** button to expose the widget drawer.
3. Search for **LaunchDarkly** to find the LaunchDarkly widget in the *Apps** section of the widget drawer.
4. Click or drag the LaunchDarkly widget icon to add it your your dashboard and open the **LaunchDarkly editor** modal.
5. Press the **Connect** button to connect your LaunchDarkly account. A new window opens prompting you to authorize Datadog.
6. Click **Authorize**. You are returned to Datadog.
7. Next, configure the following widget options in the **LaunchDarkly editor**:

    * **LaunchDarkly project**: The name of the LaunchDarkly project you wish to associate with the dashboard widget.
    * **LaunchDarkly environment**: The name of the LaunchDarkly environment you wish to associate with the dashboard widget.
    * **Environment template variable**: An optional [Datadog template variable](https://docs.datadoghq.com/dashboards/template_variables/) used to override the **LaunchDarkly environment** option.
    * **LaunchDarkly tag filter**: An optional `+` separated list tags used to filter the feature flags displayed in the widget. If multiple tags are included, only flags that match **all** included tags appear in the widget. If omitted, all of the project's feature flags appear in the widget.
    * **Sort**: The order the flags will be displayed in the widget. Defaults to **Newest**.
8. Optionally give the widget a title.
9. Press **Save** to finish configuring the Datadog dashboard widget.

### Relay Proxy metrics

Follow the Relay Proxy's [Metrics integrations documentation](5), to configure this feature.
## Data Collected

### Metrics

The LaunchDarkly Relay Proxy can be configured to send the following metrics are sent to datadog:

- **`connections`**: The number of currently existing stream connections from SDKs to the Relay Proxy.
- **`newconnections`**: The cumulative number of stream connections that have been made to the Relay Proxy since it started up.
- **`requests`**: The cumulative number of requests received by all of the Relay Proxy's [service endpoints](6) (except for the status endpoint) since it started up.

### Events

The LaunchDarkly integration sends flag, project, and environment events from LaunchDarkly to Datadog.

### Service Checks

The LaunchDarkly integration does not include any service checks.

## Support

Need help? Contact [Datadog Support][7].

## Further Reading

Learn more about [LaunchDarkly][1] and [this integration][3].

[1]: https://launchdarkly.com
[2]: https://docs.launchdarkly.com/home/relay-proxy
[3]: https://app.datadoghq.com/account/settings#api
[4]: https://docs.launchdarkly.com/integrations/datadog/events
[5]: https://github.com/launchdarkly/ld-relay/blob/v6/docs/metrics.md
[6]: https://github.com/launchdarkly/ld-relay/blob/v6/docs/endpoints.md
[7]: https://docs.datadoghq.com/help/
