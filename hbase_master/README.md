# Hbase_master Integration

## Overview

Get metrics from Hbase_master service in real time to:

- Visualize and monitor Hbase_master states.
- Be notified about Hbase_master failovers and events.

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Hbase_master check on your host. See our dedicated Agent guide for [installing community integrations][1] to install checks with the [Agent prior v6.8][2] or the [Docker Agent][3]:

1. Install the [developer toolkit][4].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `hbase_master` package, run:

   ```shell
   ddev -e release build hbase_master
   ```

5. [Download and launch the Datadog Agent][5].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_HBASE_MASTER_ARTIFACT_>/<HBASE_MASTER_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `hbase_master.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Hbase_master [metrics](#metrics). See the [sample hbase_master.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

### Log collection

1. Collecting logs is disabled by default in the Datadog Agent, you need to enable it in `datadog.yaml`:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `hbase_master.d/conf.yaml` file to start collecting your Hbase_master Logs:

   ```yaml
   logs:
     - type: file
       path: /path/to/my/directory/file.log
       source: hbase
   ```

   Change the `path` parameter value and configure it for your environment.
   See the [sample hbase_master.d/conf.yaml][8] for all available configuration options.

3. [Restart the Agent][9].

### Validation

[Run the Agent's `status` subcommand][10] and look for `hbase_master` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Events

The Hbase_master check does not include any events.

### Service Checks

The Hbase_master check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/hbase_master/datadog_checks/hbase_master/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[11]: https://github.com/DataDog/integrations-extras/blob/master/hbase_master/metadata.csv
[12]: http://docs.datadoghq.com/help
