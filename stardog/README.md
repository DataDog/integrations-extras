# Stardog Integration

## Overview

Get metrics from the Stardog service in real time to:

* Visualize and monitor Stardog states
* Be notified about Stardog failovers and events.


## Setup

The Stardog check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the Stardog check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][1].
2. Download the [`stardog.py` file][8] for Stardog.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:


1. Install the [developer toolkit][2] on any machine.
2. Run `ddev release build stardog` to build the package.
3. [Download the Datadog Agent][1].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/stardog/dist/<ARTIFACT_NAME>.whl`.

### Configuration

To configure the Stardog check:

1. Create a `stardog.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `stardog.d/` folder previously created.
3. Consult the [sample stardog.yaml][3] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][4].

## Validation

[Run the Agent's status subcommand][5] and look for `stardog` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][6] for a list of metrics provided by this check.

### Events
The Stardog check does not include any events.

### Service Checks
The Stardog check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][7].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/stardog/check.py
[3]: https://github.com/DataDog/integrations-extras/blob/master/stardog/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[5]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[6]: https://github.com/DataDog/integrations-extras/blob/master/stardog/metadata.csv
[7]: http://docs.datadoghq.com/help/
[8]: https://github.com/DataDog/integrations-extras/blob/master/stardog/datadog_checks/stardog/stardog.py
