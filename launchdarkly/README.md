# LaunchDarkly integration

## Overview


The [LaunchDarkly][1] app for Datadog brings flag event markers to your monitoring dashboards, so you can see the effects of your LaunchDarkly feature deployments on your customer's services or systems. For instance, if a deployed feature causes a service to slow down, you can see the cause within Datadog. Additionally you can use the LaunchDarkly flags dashboard widget to seamlessly monitor and perform a feature go-live from a single window. 

## Setup

This integration uses a [Datadog API key][2], which can be created by a Datadog admin. Once you obtain a Datadog API key, visit the [LaunchDarkly documentation for the Datadog integration][3] to learn how to setup the LaunchDarkly integration for Datadog.


## Data Collected

### Metrics

The LaunchDarkly integration does not include any metrics.

### Events

The LaunchDarkly integration sends flag, project, and environment events from LaunchDarkly to Datadog.

### Service Checks

The LaunchDarkly integration does not include any service checks.

## Support

Need help? Contact [Datadog Support][4].

## Further Reading

Learn more about [LaunchDarkly][1] and [this integration][3].

[1]: https://launchdarkly.com
[2]: https://app.datadoghq.com/account/settings#api
[3]: https://docs.launchdarkly.com/docs/datadog
[4]: https://docs.datadoghq.com/help/
