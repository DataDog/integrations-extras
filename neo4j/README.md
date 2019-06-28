# Neo4j Integration

## Overview

Get metrics from Neo4j service in real time to:

* Visualize and monitor Neo4j states.
* Be notified about Neo4j failovers and events.

## Setup

The Neo4j check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Neo4j check on your host. See our dedicated Agent guide about [how to install Community integration](https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/) to see how to install them with the [Agent prior v6.8](https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68) or the [Docker Agent](https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker):

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit).
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `neo4j` package, run:

    ```
    ddev -e release build neo4j
    ```

5. [Download and launch the Datadog Agent](https://app.datadoghq.com/account/settings#agent).
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_NEO4J_ARTIFACT_>/<NEO4J_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration](https://docs.datadoghq.com/getting_started/integrations).
8. [Restart the Agent](https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#restart-the-agent).

### Configuration

1. Edit the `neo4j.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6#agent-configuration-directory) to start collecting your Neo4j [metrics](#metric-collection).
  See the [sample neo4j.d/conf.yaml](https://github.com/DataDog/integrations-extras/blob/master/neo4j/datadog_checks/neo4j/data/conf.yaml.example) for all available configuration options.

2. [Restart the Agent](https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent)

## Validation

[Run the Agent's `status` subcommand][4] and look for `neo4j` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Neo4j check does not include any events.

### Service Checks
This Neo4j check tags all service checks it collects with:

  * `server_name:<server_name_in_yaml>`
  * `url:<neo4j_url_in_yaml>`

`neo4j.can_connect`:
Returns `CRITICAL` if the Agent fails to receive a 200 from the _monitoring_ endpoint, otherwise returns `OK`.

## Troubleshooting
Need help? Contact [Datadog support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/datadog_checks/neo4j/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[5]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[8]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/datadog_checks/neo4j/neo4j.py
