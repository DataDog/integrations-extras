# LaunchDarkly Integration

## Overview

The Datadog-LaunchDarkly integration allows you to see the effects of your LaunchDarkly feature deployments on your customer's services or systems. For instance, if a deployed feature causes a service to slow down, you would be able to see the cause within Datadog.

![LaunchDarkly events in Datadog][2]

## Setup

This integration will need a [Datadog API key][1]. Only Datadog admins can create an API key. Once you've obtained a Datadog API key, visit the [LaunchDarkly documentation for the Datadog integration][3] to learn how to setup the Datadog-LaunchDarkly integration.

**Note**: In order to set it up, you need a valid [Datadog API key][1].

## Data Collected

### Metrics

The LaunchDarkly integration does not include any metrics.

### Events

The LaunchDarkly integration sends flag, project, and environment events from LaunchDarkly to Datadog.

### Service Checks

The LaunchDarkly integration does not include any service checks.

## Troubleshooting

Need help? Contact [LaunchDarkly Support][4].

## Further Reading

Learn more about [LaunchDarkly][5] and this integration [here][3].

[1]: https://app.datadoghq.com/account/settings#api
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/launchdarkly/images/ld-datadog-hover.gif
[3]: https://docs.launchdarkly.com/docs/datadog
[4]: https://support.launchdarkly.com/hc/en-us/requests/new
[5]: https://launchdarkly.com
