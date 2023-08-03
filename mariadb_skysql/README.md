# Agent Check: MariaDB SkySQL

## Overview

This check monitors [MariaDB SkySQL][1]. SkySQL is the only database-as-a-service that combines the ease and innovation of MariaDB with the limitless scalability, high performance and availability, and the security of the cloud.. Build faster, deploy easily, and manage all of your databases from a single pane via DataDog.  Designed for a hybrid and multi-cloud future, built on Kubernetes, and engineered for mission-critical transactional and analytical deployments, it’s the database-as-a-service you’ve been waiting for.  Ensure your data and cloud scale to your innovating data utilization needs, in an efficient, economical manner.

## Setup

### Installation

To install the MariaDB SkySQL check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build mariadb_skysql` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/mariadb_skysql/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `mariadb_skysql.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][3] to start collecting your MariaDB [metrics](#metric-collection). See the [sample mariadb_skysql.d/conf.yaml][4] for all available configuration options.

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

Need help? Contact [Datadog support][9].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-extras/blob/master/mariadb_skysql/datadog_checks/mariadb_skysql/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/mariadb_skysql/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/mariadb_skysql/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
