# Agent Check: SpiceDB

## Overview

[SpiceDB][1]is an open source, [Google Zanzibar][zanzibar]-inspired database system for creating and managing security-critical application permissions.

Developers create a schema that models their permissions requirements. Then, they use any of the official or community maintained client libraries to apply the schema to the database and insert data into the database. They can query the data to efficiently check permissions in their applications.

SpiceDB metrics allow developers and SREs to monitor their SpiceDB deployments, including request latency metrics, cache metrics such as size and hit/miss metrics, and datastore connection and query metrics. These will allow developers and SREs to diagnose performance problems and tune performance characteristics of their SpiceDB clusters.

## Setup

### Installation

#### Host-level installation
To install the SpiceDB check on your host:

1. Download and install the [Datadog Agent][2].
1. Install the SpiceDB integration on the agent on the host where it's running
   ```shell
   datadog-agent integration install -t datadog-spicedb==<INTEGRATION_VERSION>
   ```

#### With the Agent sidecar container
1. Build a custom image with the agent installed:
    ```dockerfile
    FROM gcr.io/datadoghq/agent:latest
    RUN agent integration install -t datadog-spicedb==<INTEGRATION_VERSION>
    # Optionally include the configuration in the image
    COPY spicedb.yaml /conf.d/spicedb.d/conf.yaml
    ```
1. Deploy that image as a sidecar (or whatever makes sense for your topology).

### Configuration

A full list of configuration options are available in the [example configuration][example-conf].
This integration wraps the Datadog Openmetrics configuration, so the [openmetrics documentation][openmentrics-docs]
may be helpful as well.

### Validation

[Run the Agent's status subcommand][6] and look for `spicedb` under the Checks section.

## Data Collected

### Metrics

The integration collects metrics through the [SpiceDB prometheus endpoint][spicedb-prometheus].

For a full list of metrics this integration provides, see the [metadata.csv][metadata.csv] file.

### Service Checks

Service check `spicedb.openmetrics.health` is submitted in the base check.

### Events

SpiceDB does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://authzed.com/spicedb
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/spicedb/datadog_checks/spicedb/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/spicedb/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/spicedb/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[zanzibar]: https://authzed.com/zanzibar
[metadata.csv]: https://github.com/DataDog/integrations-extras/blob/master/spicedb/metadata.csv
[example-conf]: https://github.com/DataDog/integrations-extras/blob/master/spicedb/datadog_checks/spicedb/data/conf.yaml.example
[spicedb-prometheus]: https://authzed.com/docs/spicedb/ops/observability#prometheus
[openmetrics-docs]: https://docs.datadoghq.com/integrations/openmetrics/
