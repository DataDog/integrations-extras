# Storm Integration

## Overview

Get metrics from Storm service in real time to:

* Visualize and monitor Storm cluster and topology metrics.
* Be notified about Storm failovers and events.

## Setup

The Storm check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Storm check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][1].
2. Download the [`storm.py` file][8] for Storm.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit][7] on any machine.
2. Run `ddev release build storm` to build the package.
3. [Download the Datadog Agent][1].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/storm/dist/<ARTIFACT_NAME>.whl`.

**Note**: The `integration` command is only available for Agent 6.8+.


### Configuration

To configure the Storm check:

1. Create a `storm.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `storm.d/` folder previously created.
3. Consult the [sample storm.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `storm` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Storm check does not include any events.

### Service Checks
**`topology_check.{TOPOLOGY NAME}`**

The check returns:

* `OK` if the topology is active.
* `CRITICAL` if the topology is not active.

## Troubleshooting
Need help? Contact [Datadog support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/storm/datadog_checks/storm/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/storm/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://github.com/DataDog/integrations-core/blob/master/docs/dev/new_check_howto.md#developer-toolkit
[8]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/datadog_checks/eventstore/eventstore.py
