# LaunchDarkly integration for Datadog

## Overview

[LaunchDarkly](https://launchdarkly.com/) is the world's leading Feature Management Platform serving over 20 trillion feature flags daily to help software teams build better software, faster.

The LaunchDarkly integration for Datadog brings flag event markers to your monitoring dashboards, so you can see the effects of your LaunchDarkly feature deployments on your customer's services or systems. For instance, if a deployed feature causes a service to slow down, you would be able to see the cause within Datadog. Additionally you can employ the LaunchDarkly flags dashboard widget to seamlessly monitor and perform a feature go-live from a single window. 

## Setup

This integration will need a [Datadog API key][2]. Only Datadog admins can create an API key. Once you've obtained a Datadog API key, visit the [LaunchDarkly documentation for the Datadog integration][3] to learn how to setup the LaunchDarkly integration for Datadog.

**Note**: In order to set it up, you need a valid [Datadog API key][2].

## Data Collected

### Metrics

The LaunchDarkly integration does not include any metrics.

### Events

The LaunchDarkly integration sends flag, project, and environment events from LaunchDarkly to Datadog.

### Service Checks

The LaunchDarkly integration does not include any service checks.

## Troubleshooting

Need help? Contact [LaunchDarkly Support][3].

## Further Reading

Learn more about [LaunchDarkly][1] and this integration [here][3].

[1]: https://launchdarkly.com
[2]: https://app.datadoghq.com/account/settings#api
[3]: https://docs.launchdarkly.com/docs/datadog
[4]: https://support.launchdarkly.com/hc/en-us/requests/new
[5]: https://launchdarkly.com
