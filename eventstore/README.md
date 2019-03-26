# EventStore Integration

## Overview

Get metrics from EventStore in real time to:

* Visualize and monitor EventStore queues
* Capture all available metrics within the stats API

## Setup

### Installation

To install the EventStore check on your host:

1. Install the [developer toolkit][1] on any machine.
2. Run `ddev release build eventstore` to build the package.
3. [Download the Datadog Agent][2].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/eventstore/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `eventstore.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][3] to start collecting your EventStore [metrics](#metric-collection) and [logs](#log-collection).
  See the [sample eventstore.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5]

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

Able to collect all numeric or datetime metrics supplied by the api, it will require you to add metric_definitions for new metrics, all current metrics are listed

### Events

The eventstore check does not include any events.

### Service Checks

The eventstore check does not include any service checks.

## Troubleshooting

Raise a ticket for the maintainer to assist with

[1]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/DataDog/integrations-extras/blob/master/eventstore/datadog_checks/eventstore/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
