# Agent Check: FoundationDB

## Overview

This check monitors [FoundationDB][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the FoundationDB check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build foundationdb` to build the package.

3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/foundationdb/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `foundationdb.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your foundationdb performance data. See the [sample foundationdb.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4].

### Validation

[Run the Agent's status subcommand][5] and look for `foundationdb` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

FoundationDB has a `can_connect` service check.

### Events

FoundationDB does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][7].

## Logging

1. FoundationDB has XML logs by default, to get JSON logs, add a `trace_format` key to your `foundationdb.conf`'s `fdbserver` section:

```
[fdbserver]
...
logdir = /var/log/foundationdb
trace_format = json
```

Then restart your server.

2. Enable log collection in the Datadog Agent, in your `datadog.yaml` file:

```yaml
logs_enabled: true
```

3. Add this configuration block to your foundationdb.d/conf.yaml file to start collecting your FoundationDB logs:

```yaml
logs:
  - type: file
    path: /usr/local/foundationdb/logs/*.json
    service: foundationdb
    source: foundationdb
```

The `path` here is the `logdir` in your configuration file. Make sure the datadog agent has the privileges required to list the directory and read its files.

4. Restart the agent

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/foundationdb/datadog_checks/foundationdb/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/foundationdb/metadata.csv
[7]: https://docs.datadoghq.com/help/
