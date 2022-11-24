# Hasura Cloud Integration

## Overview

[Hasura Cloud][1] provides a scalable, highly available, globally distributed,
secure, production-ready GraphQL API over your data sources.

The Datadog integration is an observability feature of Hasura Cloud that exports
your Hasura Cloud project's operation logs, metrics, and traces to your Datadog dashboard. 

## Setup

To set up the Hasura Cloud Datadog integration for your Hasura Cloud project, provide a Datadog API key and region to Hasura Cloud.

See the [Hasura Cloud documentation][3] for how to configure the Datadog integration for your Hasura Cloud project.

Once the above is done, go to the [Logs section][5] in Datadog and create facets for the following top level fields:

* `operation_name`
* `operation_type`
* `error_code`
* `is_error`

See the [Datadog Log Facets documentation][4] for information regarding creating facets from logs.

Logs, metrics, and traces from your Hasura Cloud project are automatically sent to Datadog when your project receives traffic.

## Data Collected

### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration.

### Service Checks

The Hasura Cloud integration does not include any service checks.

### Events

The Hasura Cloud integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://hasura.io/cloud/
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/algorithmia/images/algorithmia-insights-datadog.png
[3]: https://hasura.io/docs/latest/observability/integrations/datadog/
[4]: https://docs.datadoghq.com/logs/explorer/facets/#create-facets
[5]: http://app.datadoghq.com/logs
[6]: https://docs.datadoghq.com/help/
