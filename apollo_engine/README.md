# Apollo Engine

## Overview

Apollo Engine is designed to monitor the performance of your GraphQL infrastructure. If you already have Datadog set up to monitor the rest of your stack, you can easily forward metrics collected by Engine through this integration.

![Metrics](https://github.com/DataDog/integrations-extras/blob/master/apollo-engine/images/metrics.png)

The Datadog metrics provided are:

* `apollo.engine.operations.count` – the number of GraphQL operations that were executed. This includes queries, mutations, and operations that resulted in an error.
* `apollo.engine.operations.error_count`-  the number of GraphQL operations that resulted in an error. This includes GraphQL execution errors, and HTTP errors if Engine failed to connect to your server.
* `apollo.engine.operations.cache_hit_count` - the number of GraphQL queries whose result was served from Apollo Engine's full query cache.
* A histogram of GraphQL operation response times, measured in milliseconds. Due to Engine's aggregation method (logarithmic binning), these values are accurate to +/- 5%:
  * `apollo.engine.operations.latency.min`
  * `apollo.engine.operations.latency.median`
  * `apollo.engine.operations.latency.95percentile`
  * `apollo.engine.operations.latency.99percentile`
  * `apollo.engine.operations.latency.max`
  * `apollo.engine.operations.latency.avg`

All of Engine's Datadog metrics are tagged with the GraphQL operation name, as `operation:<query-name>`. Unique query signatures with the same operation name are merged, and queries without an operation name are ignored. All of the metrics are also tagged with the Engine service ID, `service:<service-id>`, so multiple Apollo Engine services can send data to the same Datadog account.

Engine sends metrics to Datadog in 60 second intervals. Data is forwarded with a 60 second delay to allow for reports from Engine proxies to be collected, even in the case of temporary network failures.
Since Datadog metrics merge statistics from multiple instances of the proxy, per-host metrics are not available. Just like in Apollo Engine, each operation inside a query batch is counted individually.

## Setup

### Configuration

Getting set up with Engine's Datadog integration is as simple as providing a Datadog API key to Engine. There's no further configuration required!

1. Copy your Datadog API key:

```
${api_key}
```

2. Navigate to the [Apollo Engine service(s)](https://engine.apollographql.com/) you would like to enable Datadog metrics for. Go to the /settings page for that service:

![SettingsLink](https://github.com/DataDog/integrations-extras/blob/master/apollo-engine/images/settings-link.png)

3. You should see an Integrations section at the bottom of the page. Toggle the Datadog integration to turn it on:

![Settings](https://github.com/DataDog/integrations-extras/blob/master/apollo-engine/images/settings-toggle.png)

4. Paste the API key, and press **Done**. You can use the same API key for all Apollo Engine services as all metrics are tagged with a service ID (`service:<service-id>`).

5. Go to your Datadog metric explorer and start to see the metrics flow in! Please allow up to five minutes for metrics to be visible.

### Usage

Please refer to the [Apollo Engine docs](https://www.apollographql.com/docs/engine/datadog.html) for more detailed usage information.

## Data Collected

### Metrics

See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/apollo-engine/metadata.csv) for a list of metrics provided by this integration.

### Events

The Apollo Engine integration does not include any events at this time.

### Service Checks

The Apollo Engine integration does not include any service checks at this time.

## Troubleshooting

Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).
