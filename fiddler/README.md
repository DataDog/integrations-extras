# Agent Check: Fiddler

## Overview
Fiddler's Model Performance Management platform monitors Machine Learning model performance by sending real-time alerts when model performance metrics drop, allowing users to analyze inference data to understand why model performance is degrading. This integration includes metrics and an out-of-the-box dashboard that displays performance metrics such as accuracy, traffic, and drift.


## Setup

The Fiddler check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Fiddler check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   /opt/datadog-agent/embedded/bin/pip install fiddler-client
   datadog-agent integration install -t datadog-fiddler==1.0.0
   ```

2. Configure your integration similar to Agent-based [integrations][4].

### Configuration

1. Edit the `fiddler.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your Fiddler performance data. See the [sample `fiddler.d/conf.yaml`][5] for all available configuration options.  The `url`, `org`, and `fiddler_api_key` parameters will need to be updated respective of the Fiddler environment you wish the integration to query. Fiddler also suggests setting the `minimum_collection_interval` setting in the conf.yaml file to 300, or 5 minutes.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `fiddler` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].

[1]: https://fiddler.ai
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/fiddler/datadog_checks/fiddler/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/fiddler/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/fiddler/assets/service_checks.json
[10]: https://docs.datadoghq.com/help/

