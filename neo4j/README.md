# Neo4j Integration

## Overview

Get metrics from Neo4j service in real time to:

* Visualize and monitor Neo4j states.
* Be notified about Neo4j failovers and events.

## Setup

The Neo4j check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Neo4j check on your host:

1. [Download the Datadog Agent][1].
2. Download the [`check.py` file][2] for Neo4j.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `neo4j.py`.

### Configuration

To configure the Neo4j check:

1. Create a `neo4j.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `neo4j.d/` folder previously created.
3. Consult the [sample neo4j.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to configure the servers to monitor:

    * `neo4j_url`: Set to the url of the server (i.e `http://ec2-54-85-23-10.compute-1.amazonaws.com`)
    * `port`: Set to the http port used by Neo4j. *Default is 7474*
    * `username`: Set to a valid Neo4j username
    * `password`: Set to the password for the username
    * `connect_timeout`: Setting for the length of time to attempt to connect to the Neo4j server
    * `server_name`: Set to what should be displayed in DataDog
    * `version`: Set to the Neo4j version

5. [Restart the Agent][3].

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
[2]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/metadata.csv
[6]: http://docs.datadoghq.com/help/
