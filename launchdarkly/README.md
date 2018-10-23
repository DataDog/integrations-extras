# LaunchDarkly Integration

## Overview

This integration tracks metrics from [LaunchDarkly's relay proxy][1], such as number of proxied stream connections and proxied API route requests.

## Setup

### Configuration

After you've configured the [relay proxy][2], add the following section to your LaunchDarkly relay instance's `ld-relay.conf` file:

```
[datadog]
enabled=true
statsAddr="YOUR_STATS_ADDRESS"
```

## Data Collected

### Metrics

The relay collects metrics on the number of proxied stream connections and proxied API route requests. See [relay documentation][3] for more information.

### Events

The LaunchDarkly integration does not include any events at this time.

### Service Checks

The LaunchDarkly integration does not include any service checks at this time.

## Troubleshooting

Need help? Contact Datadog [Support][4].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][5].

[1]: https://docs.launchdarkly.com/docs/the-relay-proxy
[2]: https://github.com/launchdarkly/ld-relay#quick-setup
[3]: https://github.com/launchdarkly/ld-relay#exporting-metrics-and-traces
[4]: https://docs.datadoghq.com/help/
[5]: https://www.datadoghq.com/blog/
