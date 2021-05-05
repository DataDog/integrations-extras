# Hasura Cloud Integration

## Overview

[Hasura Cloud][1] provides a scalable, highly available, globally distributed,
secure production ready GraphQL API instantly over your data sources.

The Datadog integration is an observability feature of Hasura Cloud that exports
your Hasura Cloud project's operation logs and metrics to your Datadog dashboard. 

## Setup

Getting set up with the Hasura Cloud Datadog integration for your Hasura Cloud project is as simple as providing a Datadog API key and region to Hasura Cloud. 

Refer to the [Hasura Cloud documentation][3] to configure the Datadog Integration for your Hasura Cloud project. 

Once the above is done, go to **Logs** tab on Datadog dashboard and create facets for the following top level fields: 

* `operation_name`
* `operation_type`
* `error_code`
* `is_error`

Read [Datadog docs][4] on how to create facets from logs. 

## Data Collected

### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration.

### Service Checks

Hasura Cloud Integration check does not include any service checks.

### Events

Hasura Cloud Integration check does not include any events.

## Troubleshooting

Need help? Reach out to Hasura Cloud support at support@hasura.io  or login to your Hasura Cloud account and use the live chat widget.

[1]: https://hasura.io/cloud/
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/algorithmia/images/algorithmia-insights-datadog.png
[3]: https://hasura.io/docs/latest/graphql/cloud/metrics/integrations/datadog.html
[4]: https://docs.datadoghq.com/logs/explorer/facets/#create-facets
