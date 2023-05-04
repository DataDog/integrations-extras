# Agent Check: Flagsmith

{{< callout url="#" btn_hidden="true" header="Join the Feature Flag Tracking Beta!">}}
To enrich your RUM data with your Flagsmith feature flags and get visibility into performance monitoring and behavioral changes, join the [Feature Flag Tracking][1] private beta. To request access, contact Datadog Support at support@datadoghq.com.

{{< /callout >}}

## Overview

[Flagsmith][2] facilitates feature management across web, mobile, and server side applications. The Datadog Flagsmith integration enables you to view information about flag changes directly within Datadog.

Flagsmith provides the following integrations with Datadog:

### Events integration

All flag change events are sent to Datadog. These events are tagged with the environment they were changed in.

### Feature flag tracking integration

Flagsmith's feature flag tracking integration enriches your RUM data with your feature flags to provide visibility into performance monitoring and behavioral changes. Determine which users are shown a user experience and if it is negatively affecting the user's performance.

### Dashboard widget

Flagsmith's dashboard widget lets you view your Flagsmith Flags and Audit Logs directly in Datadog.

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

### Flagsmith Dashboard widget

1. On the [Flagsmith integration tile][5], make sure the integration is installed.
2. Make sure you are logged into Flagsmith with the account you want to see in Datadog.
3. In Datadog, navigate to an existing dashboard or create a new one.
4. Press the **Add Widgets** button to expose the widget drawer.
5. Search for **Flagsmith** to find the Flagsmith widget in the **Apps** section of the widget drawer.
6. Select the **Flagsmith widget icon** to add it your your dashboard and open the **Flagsmith editor** modal. You can choose to add either the Flag or Audit log viewer widget.
7. Select the Flagsmith Organization, Project and Environment you want to add to your dashboard.
8. Once selected, copy and paste the **Project ID** and **Environment ID** into Datadog.
9. Select the page size and, optionally, a widget title and Flagsmith Tag to filter on.
10. Click **Save** to finish configuring the dashboard widget.

## Data Collected

### Metrics

The Flagsmith integration does not include any metrics.

### Service Checks

The Flagsmith integration does not include any service checks.

### Events

All Flagsmith events are sent to the Datadog event stream.

## Troubleshooting

Need help? See the [Flagsmith documentation][6] or contact [Datadog Support][7].

[1]: https://www.flagsmith.com/
[2]: https://app.flagsmith.com/
[3]: https://app.datadoghq.com/organization-settings/api-keys
[4]: https://app.datadoghq.com/integrations/flagsmith
[5]: https://docs.flagsmith.com/integrations/datadog/
[6]: https://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection/
