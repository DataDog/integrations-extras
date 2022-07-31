# Agent Check: grpc_check

## Overview

This check monitors endpoints implementing [gRPC Health Checking Protocol][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

To install the grpc_check check on your host:

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit) on any machine.

2. Run `ddev release build grpc_check` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
   run `datadog-agent integration install -w path/to/grpc_check/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `grpc_check.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your grpc_check performance data. See the [sample grpc_check.d/conf.yaml][4] for all available configuration options.

2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `grpc_check` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The grpc_check integration does not include any events.

### Service Checks

The grpc_check integration does not include any service checks.

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://github.com/grpc/grpc/blob/master/doc/health-checking.md
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-core/blob/master/check/datadog_checks/check/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/check/metadata.csv
[8]: https://github.com/DataDog/integrations-core/blob/master/check/assets/service_checks.json
[9]: help@datadoghq.com


INSTALLED PIP

grpcio
grpc
grpcio-health-checking
