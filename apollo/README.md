# Apollo

## Overview

The Apollo Datadog integration allows you to forward the performance metrics that are available to you in Graph Manager to Datadog. Datadog additionally supports the advanced function API, allowing teams to create graphs and alerts for their GraphQL metrics.

![Metrics][1]

The Datadog metrics forwarded by Graph Manager are:

- `apollo.engine.operations.count` - the number of GraphQL operations that were executed. This includes queries, mutations, and operations that resulted in an error.
- `apollo.engine.operations.error_count` - the number of GraphQL operations that resulted in an error. This includes GraphQL execution errors, and HTTP errors if Graph Manager failed to connect to your server.
- `apollo.engine.operations.cache_hit_count` - the number of GraphQL queries whose result was served from Apollo Server's full query cache.
- A histogram of GraphQL operation response times, measured in milliseconds. Due to Graph Manager's aggregation method (logarithmic binning), these values are accurate to +/- 5%:

  - `apollo.engine.operations.latency.min`
  - `apollo.engine.operations.latency.median`
  - `apollo.engine.operations.latency.95percentile`
  - `apollo.engine.operations.latency.99percentile`
  - `apollo.engine.operations.latency.max`
  - `apollo.engine.operations.latency.avg`

All metrics forwarded to Datadog are aggregated in 60-second intervals and tagged with the GraphQL operation name as `operation:<QUERY_NAME>`. Unique query signatures with the same operation name are merged, and queries without an operation name are ignored.

All of the metrics are also tagged with the Graph Manager graph ID as `service:<GRAPH_ID>` and the variant name as `variant:<VARIANT_NAME>`, so multiple graphs from Graph Manager can send data to the same Datadog account. If you have not set a variant name, then "current" will be used.

If you're reporting metrics to Graph Manager through the Engine proxy, Datadog will merge your statistics across multiple instances of the proxy (per-host metrics are not available). Just like in the Graph Manager UI, each operation inside a query batch is counted individually.

## Setup

### Configuration

Getting set up with the Apollo Datadog integration is as simple as providing a Datadog API key to Graph Manager. There's no further configuration required.

1. Go to the [Datadog integrations page][2] and click on the Apollo tile. Go to the **Configuration** tab, scroll to the bottom, and press **Install Integration**.

2. Go to the [Datadog APIs page][3] and create an API key.

3. In [Graph Manager][4], go to the integrations page for your graph.

   ![IntegrationsPage][5]

4. Toggle the Datadog integration to turn it on. Paste the API key, and press **Save**. You can use the same API key for all your graphs, since all metrics are tagged with the graph ID (`service:<GRAPH_ID>`).

   ![IntegrationsToggle][6]

5. Go to the Datadog metrics explorer and start to see the metrics flow in! Please allow up to five minutes for metrics to be visible.

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
[2]: https://app.datadoghq.com/account/settings
[3]: https://app.datadoghq.com/account/settings#api
[4]: https://www.apollographql.com/docs/graph-manager/#viewing-graph-information
[5]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/apollo/images/settings-link.png
[6]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/apollo/images/settings-toggle.png
[7]: https://www.apollographql.com/docs/graph-manager/datadog-integration/
[8]: https://github.com/DataDog/integrations-extras/blob/master/apollo/metadata.csv
[9]: https://docs.datadoghq.com/help
[10]: https://www.datadoghq.com/blog
