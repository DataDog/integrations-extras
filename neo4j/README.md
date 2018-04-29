# Neo4j Integration

## Overview

Get metrics from neo4j service in real time to:

* Visualize and monitor neo4j states.
* Be notified about neo4j failovers and events.

## Setup

### Configuration

Edit the `neo4j.yaml` file to configure the servers to monitor:

* neo4j_url: set to the url of the server (i.e `http://ec2-54-85-23-10.compute-1.amazonaws.com`)
* port: set to the http port used by neo4j. Default is 7474
* username: set to a valid neo4j username
* password: set to the password for the username
* connect_timeout: setting for the length of time to attempt to connect to the neo4j server
* server_name: set to what should be displayed in DataDog
* version: set to the neo4j versin

### Validation

[Run the Agent's `status` subcommand][1] and look for `neo4j` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Neo4j check does not include any events at this time.

### Service Checks
The Neo4j check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].


[1]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[2]: https://github.com/DataDog/integrations-extras/blob/master/neo4j/metadata.csv
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
