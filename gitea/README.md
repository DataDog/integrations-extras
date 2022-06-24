# Gitea Integration

## Overview

[Gitea][1] is a community managed lightweight code hosting solution written in Go.

This integration monitors Gitea instances through the Datadog [Agent][2].

## Setup

### Prerequisite

Gitea doesn't expose its internal metrics by default. You need to enable the built-in HTTP server that exposes the metrics endpoint in your `app.ini` configuration file.

```ini
[metrics]
ENABLED = true
```

See the official [documentation][3] for more information.

### Installation

The Gitea integration is not included in the [Datadog Agent][4] package by default, so you need to install it.

For Agent v7.36+, follow the instructions below to install the Gitea check on your host. See [Use Community Integrations][5] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

```shell
datadog-agent integration install -t datadog-gitea==<INTEGRATION_VERSION>
```

2. Configure your integration similar to core [integrations][6].

### Configuration

1. Edit the `gitea.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Gitea data. See the [sample gitea.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8].

### Validation

[Run the Agent's status subcommand][9] and look for `gitea` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Events

The Gitea check does not include any events.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://docs.gitea.io/en-us/ 
[2]: https://docs.datadoghq.com/agent/
[3]: https://docs.gitea.io/en-us/
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://github.com/DataDog/integrations-extras/blob/master/gitea/datadog_checks/gitea/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/gitea/metadata.csv
[11]: https://github.com/DataDog/integrations-extras/blob/master/gitea/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
