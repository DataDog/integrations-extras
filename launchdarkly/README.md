# LaunchDarkly Integration

There are currently two integrations with LaunchDarkly:

- [Events Integration](#launchdarkly-events-integration)
- [LD Relay Integration](#ld-relay-integration)

## LaunchDarkly Events Integration

### Overview

Deploying features with LaunchDarkly is great, but sometimes it's difficult to
see the effects of these feature deployments on the customer's services or
systems. Datadog's monitoring and analytics tools for modern DevOps teams allow
their customers to observe the health of their systems over time. The
LaunchDarkly integration with Datadog exposes the LaunchDarkly events in context
with events gathered by the Datadog agents. This makes it easier to reason about
changes to customers' systems as a result of feature deployments that took
place. For example, if a feature gets deployed that causes a service to slow
down, a DevOps engineer will now be able to see the cause within Datadog.

![LaunchDarkly events in Datadog][7]

### Setup

#### Configuration

As a prerequisite, this integration will need a [Datadog API
key][6]. Note, only Admin users can create an API key. Once you've obtained a Datadog API key, visit the [LaunchDarkly documentation for the Datadog integration][8].

### Data Collected

#### Metrics

The LaunchDarkly integration does not include any metrics.

#### Events

This integration sends LaunchDarkly flag, project, environment events to Datadog. These events can be used to correlate with other metrics available in Datadog.

#### Service Checks

The LaunchDarkly integration does not include any service checks.

### Troubleshooting

Need help? Contact [LaunchDarkly Support][9].

### Further Reading

Learn more about [LaunchDarkly] and this integration [here][8].

---

## LD Relay Integration

### Overview

This integration tracks metrics from [LaunchDarkly's relay proxy][1], such as
number of proxied stream connections and proxied API route requests.

### Setup

#### Configuration

After you've configured the [relay proxy][2], add the following section to your
LaunchDarkly relay instance's `ld-relay.conf` file:

```
[datadog]
enabled=true
statsAddr="YOUR_STATS_ADDRESS"
```

### Data Collected

#### Metrics

The relay collects metrics on the number of proxied stream connections and
proxied API route requests. See [relay documentation][3] for more information.

#### Events

The LaunchDarkly integration does not include any events.

#### Service Checks

The LaunchDarkly integration does not include any service checks.

### Troubleshooting

Need help? Contact Datadog [Support][4].

### Further Reading

Learn more about infrastructure monitoring and all our integrations on [our
blog][5].

[1]: https://docs.launchdarkly.com/docs/the-relay-proxy
[2]: https://github.com/launchdarkly/ld-relay#quick-setup
[3]: https://github.com/launchdarkly/ld-relay#exporting-metrics-and-traces
[4]: https://docs.datadoghq.com/help
[5]: https://www.datadoghq.com/blog
[6]: https://app.datadoghq.com/account/settings#api
[7]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/launchdarkly/assets/image/ld-datadog-hover.gif
[8]: https://docs.launchdarkly.com/docs/datadog
[9]: https://support.launchdarkly.com/hc/en-us/requests/new
