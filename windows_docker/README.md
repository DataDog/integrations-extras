# Agent Check: windows_docker

## Overview

This check monitors [windows_docker][1] through the Datadog Agent.

## Setup

### Installation

The windows_docker check is not included in the [Datadog Agent][2] package, so it must
be installed manually.

### Configuration

1. Edit the `windows_docker.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your windows_docker performance data. See the [sample windows_docker.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `windows_docker` under the Checks section.

## Data Collected

### Metrics

windows_docker does not include any metrics.

### Service Checks

windows_docker does not include any service checks.

### Events

windows_docker does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://github.com/DataDog/integrations-core/blob/master/windows_docker/datadog_checks/windows_docker/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#start-stop-and-restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#agent-status-and-information
[5]: https://docs.datadoghq.com/help


#### FIXME JAY
**Docker Windows Agent Check**
> Information:

This custom agent check will connect to the Datadog agent running on your local Windows host to connect to your Windows Docker containers. Once connected this check will collect health based metrics around the Windows containers that are running and report the data to your Datadog instance.

> Setup:

Within your Windows computer you must have the Datadog agent installed, (version 6+). More information about this can be found, [here.](https://docs.datadoghq.com/agent/basic_agent_usage/windows/?tab=agentv6)

Once the Datadog agent has been installed onto your Windows computer, the next thing that you will want to do is navigate to: `C:\ProgramData\Datadog`. Within the `/checks.d` copy and past the `win_docker.py` file, (which can be found within this repo).

Next, navigate to the `/conf.d` directory and create a new folder called `win_docker.d`. Within the `/conf.d/win_docker.d` directory copy & paste the `conf.yaml` file, (which can be found in this repo).

Finally, you will need to restart your Datadog agent and within a few moments the newly discovered Windows Docker container metrics will begin to report into Datadog.
