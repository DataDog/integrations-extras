# Agent Check: Neutrona

## Overview

This check monitors [Neutrona][1] cloud connectivity services to:
 - Azure (ExpressRoute)

## Setup

### Installation

The Neutrona check is not included in the [Datadog Agent][2] package, so you
need to install it.

Copy the check files manually or run the `_install.sh_` script if you are running the [Datadog Agent][2] on Debian/Ubuntu. This copies both the check script and sample configuration file and **restarts** the [Datadog Agent][2]. 


### Configuration

1. Edit the `neutrona.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your neutrona performance data.
   See the [sample neutrona.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3].

### Validation

[Run the Agent's status subcommand][4] and look for `neutrona` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Service Checks

Neutrona does not include any service checks at this time.

### Events

Neutrona does not include any events at this time.

## Troubleshooting

Need help? Contact [Datadog support][5].

[1]: https://telemetry.neutrona.com
[2]: https://github.com/DataDog/integrations-core/blob/master/neutrona/datadog_checks/neutrona/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help/
[6]: https://github.com/DataDog/integrations-core/blob/master/neutrona/metadata.csv
