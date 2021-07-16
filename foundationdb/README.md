# Agent Check: FoundationDB

## Overview

This check monitors [FoundationDB][1] through the Datadog Agent. Aside from
checking the FoundationDB cluster is healthy, it also collects numerous metrics
and, optionally, FoundationDB transaction logs.

## Setup

Both the check and the metrics apply to the FoundationDB cluster as a whole,
and so should only be installed on one host (which need not be one that is
running FoundationDB, but just one with access to it). The host chosen to
collect the metrics is required to have the [FoundationDB client][8]
installed. It is possible to monitor multiple FoundationDB clusters if
desired, by adding multiple instances in the configuration file.

By contrast, logs are written on each machine, and thus for collecting logs it
is necesary to configure FoundationDB log collection on every host.

Follow the instructions below to install and configure this check or log
collection. For containerized environments, see the [Autodiscovery
Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the FoundationDB check on your host:

1. If you do not already have the Datadog agent installed, [Download the
   Datadog Agent][9].

2. Install the [Datadog agent developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
   on any machine.

3. Run `ddev release build foundationdb` to build the package.

4. Upload the build artifact to any host with an Agent and
   run `datadog-agent integration install -w
    path/to/foundationdb/dist/<ARTIFACT_NAME>.whl`.

### Configuration

### For service check and metrics

Edit the `foundationdb.d/conf.yaml` file, in the `conf.d/` folder at
the root of your Agent's configuration directory to start collecting
FoundationDB metrics. See the [sample foundationdb.d/conf.yaml][3] for
all available configuration options.

The details of the cluster to check are found under the `instances`
section. Some hints:

* The `base_command` is correct by default if the `fdbcli` command is in
  your `PATH` and the FoundationDB instance is on the current machine.
  If you have `fdbcli` installed in a container, then you could modify
  this command to execute it inside of the container.
* The `cluster_file` is where `fdbcli` finds the cluster connection
  details. If this is not specified, then it will be searched for in
  the [default location][10]. Ensure that your cluster file is in
  that location, and set this property if it is located elsewhere.

To check more than one FoundationDB cluster, add an extra item to the
`instances` list. In this sitaution, at least one of the instances must
specify a `cluster_file` property.

If the cluster is [configured to use TLS][1], further properties should
be set in the configuration. These properties follow the names of the
options given to `fdbcli` to connect to such a cluster.

Be sure to **[restart the Agent][4]** after changing the configuration.

### For logging

FoundationDB writes XML logs by default, however the Datadog integration
expects JSON logs instead. Thus a configuration change shall be needed to
FoundationDB itself first.

1. Locate your `foundationdb.conf` file. Under the `fdbserver` section, add
   or change the key `trace_format` to have the value `json`. Also make a
   note of the `logdir`.

```
[fdbserver]
...
logdir = /var/log/foundationdb
trace_format = json
```

2. Restart the FoundationDB server so the changes take effect. Verify that
   logs in the logdir are now being written in JSON.

2. Ensure that log collection in the Datadog Agent is enabled. In your
   `datadog.yaml` file, make sure this appears:

```yaml
logs_enabled: true
```

3. In the `foundationdb.d/conf.yaml` file, uncomment the `logs` section
   and set the path to that found in your FoundationDB configuration file,
   appending `*.json`.

```yaml
logs:
  - type: file
    path: /var/log/foundationdb/*.json
    service: foundationdb
    source: foundationdb
```

4. Make sure the Datadog agent has the privileges required to list the
   directory and read its files.

5. Restart the Datadog agent.

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

[1]: https://www.foundationdb.org/
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://github.com/DataDog/integrations-extras/blob/master/foundationdb/datadog_checks/foundationdb/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/foundationdb/metadata.csv
[7]: https://docs.datadoghq.com/help/
[8]: https://www.foundationdb.org/download/
[9]: https://app.datadoghq.com/account/settings#agent
[10]: https://apple.github.io/foundationdb/administration.html#default-cluster-file
[11]: https://apple.github.io/foundationdb/tls.html
