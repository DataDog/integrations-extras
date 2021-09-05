# Agent Check: AWS Pricing

## Overview

This check pulls pricing information [published by AWS][1] to make it easier to measure cost of resource utilization within Datadog.

## Setup

The AWS Pricing check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the AWS Pricing check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-aws_pricing==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

1. Edit the `aws_pricing.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting AWS pricing data. See the sample [aws_pricing.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `aws_pricing` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Events

AWS Pricing does not include any events.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][10].


[1]: https://aws.amazon.com/pricing/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://github.com/DataDog/integrations-extras/blob/master/aws_pricing/datadog_checks/aws_pricing/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/aws_pricing/metadata.csv
[9]: https://github.com/DataDog/integrations-extras/blob/master/aws_pricing/assets/service_checks.json
[10]: https://docs.datadoghq.com/help/
