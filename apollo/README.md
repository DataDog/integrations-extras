# Apollo

## Overview

The Apollo Datadog integration enables you to forward Studio performance metrics to your Datadog account. Datadog supports an advanced function API, which enables you to create graphs and alerts for GraphQL metrics.

![Metrics][1]

Studio forwards the following metrics to Datadog:

- `apollo.operations.count` - The number of GraphQL operations that were executed. This includes queries, mutations, and operations that resulted in an error.
- `apollo.operations.error_count` - The number of GraphQL operations that resulted in an error. This includes GraphQL execution errors, and HTTP errors if Studio failed to connect to your server.
- `apollo.operations.cache_hit_count` - The number of GraphQL queries for which the result was served from Apollo Server's full query cache.
- A histogram of GraphQL operation response times, measured in milliseconds. Due to Studio's aggregation method (logarithmic binning), these values are accurate to +/- 5%:

  - `apollo.operations.latency.min`
  - `apollo.operations.latency.median`
  - `apollo.operations.latency.95percentile`
  - `apollo.operations.latency.99percentile`
  - `apollo.operations.latency.max`
  - `apollo.operations.latency.avg`

These metrics are aggregated in 60-second intervals and tagged with the GraphQL operation name as `operation:<query-name>`. Unique query signatures with the same operation name are merged, and queries without an operation name are ignored.

These metrics are also tagged with both the associated Studio graph ID (as `graph:<graph-id>`) and the associated variant name (as `variant:<variant-name>`), so multiple graphs from Studio can send data to the same Datadog account. If you haven't set a variant name, then `current` is used.

(Integrations set up prior to October 2020 have metric names starting with `apollo.engine.operations` instead of `apollo.operations` and use a `service` tag instead of `graph`. You can migrate to the new metric names in your graph's Integrations page in Apollo Studio.)

## Setup

### Configuration

Getting set up with the Apollo Datadog integration is as simple as providing a Datadog API key and region to Studio. There's no further configuration required.

1. Go to your [Datadog Integrations page][2] and click on the Apollo tile. Then go to the **Configuration** tab and click **Install Integration** at the bottom.

2. Go to your [Datadog APIs page][3] and create an API key.

3. Determine your Datadog API region by looking at your browser's address bar:
- If the domain name is `app.datadoghq.com`, then your API region is `US`.
- If the domain name is `app.datadoghq.eu`, then your API region is `EU`.

4. In [Studio][4], go to your graph's Integrations page:

   ![IntegrationsPage][5]

5. In the Datadog Forwarding section, click **Configure**. Provide your API key and region, then click **Enable**. Because all forwarded metrics are tagged with the corresponding graph's ID (`graph:<graph-id>`), you can use the same API key for all of your graphs.

   ![IntegrationsToggle][6]

6. Go to the Datadog metrics explorer and start to see the metrics flow in! Please allow up to five minutes for metrics to be visible.

### Usage

Please refer to the [Apollo integrations docs][7] for more detailed usage information.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this integration.

### Events

The Apollo integration does not include any events at this time.

### Service Checks

The Apollo integration does not include any service checks at this time.

## Troubleshooting

Need help? Contact [Datadog Support][9].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][10].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/apollo/images/metrics.png
[2]: https://app.datadoghq.com/account/settings#integrations
[3]: https://app.datadoghq.com/account/settings#api
[4]: https://www.apollographql.com/docs/studio/org/graphs/#viewing-graph-information
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/apollo/images/settings-link.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/apollo/images/settings-toggle.png
[7]: https://www.apollographql.com/docs/studio/datadog-integration/
[8]: https://github.com/DataDog/integrations-extras/blob/master/apollo/metadata.csv
[9]: https://docs.datadoghq.com/help/
[10]: https://www.datadoghq.com/blog
