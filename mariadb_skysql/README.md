# Agent Check: MariaDB SkySQL

## Overview

This check monitors [MariaDB SkySQL][1]. SkySQL is a multi-cloud database-as-a-service offering from MariaDB Plc.

The MariaDB SkySQL integration allows full monitoring of all your MariaDB SkySQL server deployments: Enterprise Server (Single and Replicated), Xpand, Columnstore, as well as MaxScale. Database administrators can track system resource metrics, such as memory, CPU, disk, and network utilization in addition to database specific telemetry such as query performance, connections, threads, cluster, replication status, and many others.



## Setup

### Installation

To install the MariaDB SkySQL check on your host:

1. Install the [developer toolkit][10] on any machine.

2. Run `ddev release build mariadb_skysql` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -t datadog-mariadb_skysql==0.0.1`
 This command assumes that the build directory is in ./integration-extras/mariadb_skysql/dist. You may need to modify this path to match your agent environment settings.

### Configuration

1. Edit the `mariadb_skysql.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][3] to start collecting your MariaDB [metrics](#metric-collection). See the [mariadb_skysql.d/conf.yaml.example][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

1. [Run the Agent's status subcommand][6] and look for `mariadb_skysql` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by MariaDB SkySQL.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by MariaDB SkySQL.

### Events

MariaDB SkySQL does not include any events.

## Troubleshooting

Need help? Contact [MariaDB SkySQL support][9].

[1]: https://skysql.mariadb.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-extras/blob/master/mariadb_skysql/datadog_checks/mariadb_skysql/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/mariadb_skysql/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/mariadb_skysql/assets/service_checks.json
[9]: https://cloud.mariadb.com/csm
[10]: https://docs.datadoghq.com/developers/integrations/python/#install-the-datadog-agent-integration-developer-tool
