# LaunchDarkly Integration

## Overview

Deploying features with LaunchDarkly is great, but it can be difficult to see
the effects of these deployments on users' services or systems. Datadog's
monitoring and analytics tools for modern DevOps teams allow their customers to
observe the health of their systems over time. The LaunchDarkly integration with
Datadog exposes LaunchDarkly events in context with events gathered by the
Datadog agents. This makes it easier to reason about changes to customers'
systems as a result of feature deployments. For example, if a feature gets
deployed that causes a service to slow down, a DevOps engineer can see the cause
within Datadog.

![LaunchDarkly events in Datadog][2]

### Setup

#### Configuration

This integration will need a [Datadog API key][1]. Only Datadog admins can
create an API key. Once you've obtained a Datadog API key, visit the
[LaunchDarkly documentation for the Datadog integration][3] for further
instructions on how to register the API key in LaunchDarkly.

### Data Collected

The LaunchDarkly integration sends the following data to Datadog:

#### Metrics

The LaunchDarkly integration does not include any metrics.

#### Events

This integration sends LaunchDarkly flag, project, environment events to
Datadog. These events can be used to correlate with other metrics available in
Datadog.

#### Service Checks

The LaunchDarkly integration does not include any service checks.

### Troubleshooting

Need help? Contact [LaunchDarkly Support][4].

### Further Reading

Learn more about [LaunchDarkly][5] and this integration [here][3].

[1]: https://app.datadoghq.com/account/settings#api
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/launchdarkly/assets/image/ld-datadog-hover.gif
[3]: https://docs.launchdarkly.com/docs/datadog
[4]: https://support.launchdarkly.com/hc/en-us/requests/new
[5]: https://launchdarkly.com
