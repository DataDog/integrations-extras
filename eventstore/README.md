# EventStore Integration

## Overview

Get metrics from EventStore in real time to:

* Visualize and monitor EventStore queues
* Capture all available metrics within the stats API

## Setup

### Installation

To install the EventStore check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][2].
2. Download the [`eventstore.py` file][8] for EventStore.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit][1] on any machine.
2. Run `ddev release build eventstore` to build the package.
3. [Download the Datadog Agent][2].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/eventstore/dist/<ARTIFACT_NAME>.whl`.

**Note**: The `integration` command is only available for Agent 6.8+.

### Configuration

1. Edit the `eventstore.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][3] to start collecting your EventStore [metrics](#metric-collection) and [logs](#log-collection).
  See the [sample eventstore.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

Run the Agent's `status` subcommand and look for `eventstore` under the Checks section:

       Checks
       ======

       eventstore
       -----------
        - instance #0 [OK]
        - Collected 50 metrics, 0 events & 0 service checks


## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The eventstore check does not include any events.

### Service Checks

The eventstore check does not include any service checks.

## Troubleshooting

Need help? Contact the [maintainer][6] of this integration.

[1]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/datadog_checks/eventstore/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-restart-the-agent
[6]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/manifest.json
[7]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/datadog_checks/eventstore/eventstore.py
