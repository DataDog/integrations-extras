# Agent Check: grpc_check

## Overview

This check monitors endpoints implementing [gRPC Health Checking Protocol][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

#### Host

To install the grpc_check check on your host:

```bash
sudo -u dd-agent datadog-agent integration install -t datadog-grpc-check==1.0.2
```

#### Dockerfile

Build the Agent image with this Dockerfile.

```Dockerfile
FROM datadog/agent:7
RUN agent integration install -r -t datadog-grpc-check==1.0.2 \
  && /opt/datadog-agent/embedded/bin/pip3 install grpcio grpcio-health-checking
```

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
[4]: https://github.com/DataDog/integrations-extras/blob/master/grpc_check/datadog_checks/grpc_check/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/grpc_check/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/grpc_check/assets/service_checks.json
[9]: help@datadoghq.com
[10]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
