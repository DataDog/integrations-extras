# Agent Check: AWS Pricing

## Overview

This check pulls in pricing information [published by AWS][1] to make it easier to measure cost of resource utilization in within Datadog.

<div>Icons made by <a href="https://www.flaticon.com/authors/eucalyp" title="Eucalyp">Eucalyp</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

## Setup

### Installation

The AWS Pricing check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `aws_pricing.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting AWS pricing data. See the [sample aws_pricing.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `aws_pricing` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this check..

### Service Checks

`aws_pricing.status`:

Returns `Critical` if the Agent encounters an error when using the Boto3 pricing client to collect metrics.

Returns `Warning` if a rate code was defined in `aws_pricing.d/conf.yaml` which couldn't be found using the Boto3 pricing client.

Returns `OK` if no errors were encountered and all desired service rate code pricing data was collected.

### Events

AWS Pricing does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://aws.amazon.com/pricing/
[2]: https://github.com/DataDog/integrations-core/blob/master/aws_pricing/datadog_checks/aws_pricing/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help
[6]: ttps://github.com/DataDog/integrations-extras/blob/master/aws_pricing/metadata.csv
