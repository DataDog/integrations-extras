# Agent Check: Aqua

## Overview

This check monitors [Aqua][1].

The Aqua check will alert the user if total high-severity vulnerability is reached, or if a container is running inside a host not registered by Aqua.  Aqua will also send data alerts regarding blocked events in runtime, and it is possible to trigger a webhook to scale infrastructure if more Aqua scanners are required.

## Setup

The Aqua check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Installation

To install the Aqua check on your host:

1. [Download the Datadog Agent][2].
2. Download the [`aqua.py` file][2] for Aerospike.
3. Place it in the Agent's `checks.d` directory.

### Configuration

To configure the Aqua check: 

1. Create a `aqua.d/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `conf.yaml` file in the `aqua.d/` folder previously created.
3. Consult the [sample conf.yaml][3] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file with your Aqua API credentials.
5. [Restart the Agent][4].

### Validation

[Run the Agent's `status` subcommand][5] and look for `aqua` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Service Checks

**aqua.can_connect**:

Returns CRITICAL if the Agent cannot connect to Aqua to collect metrics. Returns OK otherwise.

### Events

Aqua does not include any events.

## Troubleshooting

Need help? Contact [Datadog Support][7].

[1]: https://www.aquasec.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-extras/blob/master/aqua/datadog_checks/aqua/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[5]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/aqua/metadata.csv
[7]: https://docs.datadoghq.com/help/
[8]: https://github.com/DataDog/integrations-extras/blob/master/aqua/datadog_checks/aqua/aqua.py
