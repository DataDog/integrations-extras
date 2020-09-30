# HBase RegionServer Integration

## Overview

Get metrics from the HBase RegionServer service in real time to:

- Visualize and monitor HBase RegionServer states.
- Be notified about HBase RegionServer failovers and events.

## Setup

The HBase RegionServer check is **NOT** included in the [Datadog Agent][1] package.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the HBase RegionServer check on your host. See our dedicated Agent guide for [installing community integrations][2] to install checks with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

   ```shell
   git clone https://github.com/DataDog/integrations-extras.git.
   ```

3. Update your `ddev` config with the `integrations-extras/` path:

   ```shell
   ddev config set extras ./integrations-extras
   ```

4. To build the `hbase_regionserver` package, run:

   ```shell
   ddev -e release build hbase_regionserver
   ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -w <PATH_OF_HBASE_REGIONSERVER_ARTIFACT_>/<HBASE_REGIONSERVER_ARTIFACT_NAME>.whl
   ```

7. Configure your integration like [any other packaged integration][7].

### Configuration

1. Edit the `hbase_regionserver.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][8] to start collecting your HBase RegionServer [metrics](#metrics). See the [sample hbase_regionserver.d/conf.yaml][9] for all available configuration options.

2. [Restart the Agent][10]

### Log collection

1. Collecting logs is disabled by default in the Datadog Agent, you need to enable it in `datadog.yaml`:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `hbase_regionserver.d/conf.yaml` file to start collecting your Hbase_regionserver Logs:

   ```yaml
   logs:
     - type: file
       path: /path/to/my/directory/file.log
       source: hbase
   ```

   Change the `path` parameter value and configure it for your environment.
   See the [sample hbase_regionserver.d/conf.yaml][9] for all available configuration options.

3. [Restart the Agent][10].

## Validation

[Run the Agent's `status` subcommand][11] and look for `hbase_regionserver` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this check.

### Events

The HBase RegionServer check does not include any events.

### Service Checks

The HBase RegionServer check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][13].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[9]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/datadog_checks/hbase_regionserver/data/conf.yaml.example
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[11]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[12]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv
[13]: http://docs.datadoghq.com/help
