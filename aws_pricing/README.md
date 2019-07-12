# Agent Check: AWS Pricing

## Overview

This check pulls pricing information [published by AWS][1] to make it easier to measure cost of resource utilization within Datadog.

Icon made by [Eucalyp](https://www.flaticon.com/authors/eucalyp) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)

## Setup

### Installation

The AWS Pricing check is not included in the [Datadog Agent][2] package, so you need to install it yourself using [the official community integration installation instructions][7].

### Configuration

1. Edit the `aws_pricing.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting AWS pricing data. See the [sample aws_pricing.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `aws_pricing` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check.

### Service Checks

`aws_pricing.status`:

Returns `CRITICAL` if the Agent encounters an error when using the Boto3 pricing client to collect metrics.

Returns `WARNING` if a rate code was defined in `aws_pricing.d/conf.yaml` which couldn't be found using the Boto3 pricing client.

Returns `OK` if no errors were encountered and all desired service rate code pricing data was collected.

### Events

AWS Pricing does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://aws.amazon.com/pricing/
[2]: https://github.com/DataDog/integrations-core/blob/master/aws_pricing/datadog_checks/aws_pricing/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/guide/agent-commands/#restart-the-agent
[4]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-information
[5]: https://docs.datadoghq.com/help
[6]: https://github.com/DataDog/integrations-extras/blob/master/aws_pricing/metadata.csv
[7]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
