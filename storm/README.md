# Storm Integration

## Overview

Get metrics from Storm service in real time to:

* Visualize and monitor Storm cluster and topology metrics.
* Be notified about Storm failovers and events.

## Setup

The Storm check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Storm check on your host:

1. [Download the Datadog Agent][1].
2. Download the [`check.py` file][2] for Storm.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `storm.py`.

### Configuration

To configure the Storm check: 

1. Create a `storm/` folder in the `conf.d/` folder at the root of your Agent's directory. 
2. Create a `conf.yaml` file in the `storm/` folder previously created.
3. Consult the [sample storm.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `storm` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The Storm check does not include any events at this time.

### Service Checks
The Storm check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][6].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][7]

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/storm/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/storm/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://www.datadoghq.com/blog/