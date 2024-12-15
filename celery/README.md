# Agent Check: Celery

## Overview

This check monitors [Celery][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][3] for guidance on applying these instructions.

### Installation

To install the integration, follow the instructions for [Community Integrations][10].  
This integration requires the python-package `celery` to be available. Currently, 
the `datadog-agent integration install` command doesn't automatically install dependencies. So you need to install it 
manually. To do so, follow the instructions on how to [add a custom python-package to the agent][11].  
If you are using Redis as a broker for celery, install the python-package `redis` 
or `celery[redis]` instead of `celery`.

### Configuration

1. Edit the `celery.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your celery performance data. See the [sample celery.d/conf.yaml][4] for all available configuration options.
2. [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][6] and look for `celery` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The Celery integration does not include any events.

### Service Checks

The Celery integration does not include any service checks.

See [service_checks.json][8] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][9].


[1]: https://docs.celeryq.dev/ 
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-core/blob/master/celery/datadog_checks/celery/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-core/blob/master/celery/metadata.csv
[8]: https://github.com/DataDog/integrations-core/blob/master/celery/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[11]: https://docs.datadoghq.com/developers/guide/custom-python-package/
