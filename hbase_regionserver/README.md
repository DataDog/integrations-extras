# HBase RegionServer Integration

## Overview

Get metrics from the HBase RegionServer service in real time to:

- Visualize and monitor HBase RegionServer states.
- Be notified about HBase RegionServer failovers and events.

## Setup

The HBase RegionServer check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the HBase RegionServer check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-hbase_regionserver==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `hbase_regionserver.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][6] to start collecting your HBase RegionServer [metrics](#metrics). See the [sample hbase_regionserver.d/conf.yaml][7] for all available configuration options.

2. [Restart the Agent][8]

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
   See the [sample hbase_regionserver.d/conf.yaml][7] for all available configuration options.

3. [Restart the Agent][8].

## Validation

[Run the Agent's `status` subcommand][9] and look for `hbase_regionserver` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Events

The HBase RegionServer check does not include any events.

### Service Checks

The HBase RegionServer check does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][11].


[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[6]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[7]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/datadog_checks/hbase_regionserver/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[10]: https://github.com/DataDog/integrations-extras/blob/master/hbase_regionserver/metadata.csv
[11]: http://docs.datadoghq.com/help
