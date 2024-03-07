# Agent Check: Zenoh router

## Overview

This check monitors Zenoh router.

[Zenoh][1] is an open source Zero Overhead Network Protocol.

Zenoh (/zeno/) is a pub/sub/query protocol unifying data in motion, data at rest, and computations. It elegantly blends traditional pub/sub with geo distributed storage, queries, and computations, while retaining a level of time and space efficiency that is well beyond any of the mainstream stacks.

The Zenoh router integration allows you to monitor router metrics and router/peer/client connection statuses in Datadog.

## Setup

### Installation with the Datadog Agent (v7.21+ and v6.21+)

For Agent v7.21+ / v6.21+, follow the instructions below to install Zenoh router check on your host.

1. On your host, run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-zenoh_router==<INTEGRATION_VERSION>
   ```

### Installation from the source code

To install the Zenoh router check on your host:

1. Install the [developer toolkit][11] on any machine.

2. Run `ddev release build zenoh_router` to build the package.

3. Upload the build artifact to any host with [the Agent installed][3]

4. On the host, run `datadog-agent integration install -w path/to/zenoh_router/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Make sure that the [Zenoh REST API plugin][2] is enabled.

2. Edit the `zenoh_router.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][10] to start collecting your Zenoh router [metrics](#metrics).
See the [sample zenoh_router.d/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

### Validation

Run the [Agent's status subcommand][6] and look for `zenoh_router` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this check.

### Events

Zenoh router does not include any events.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://zenoh.io/
[2]: https://zenoh.io/docs/apis/rest/
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://github.com/DataDog/integrations-extras/blob/master/zenoh_router/datadog_checks/zenoh_router/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/zenoh_router/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/zenoh_router/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[11]: https://docs.datadoghq.com/developers/integrations/python/
