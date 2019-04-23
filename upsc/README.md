# UPSC Stats Collector Integration

## Overview

Get metrics from UPSD service via UPSC in real time to:

* Visualize and monitor UPS battery health and states
* Be notified about UPS failovers and events.

## Setup

The UPSC check is **NOT** included in the [Datadog Agent][1] package.

### Installation

To install the UPSC check on your host:

1. Install the [developer toolkit][7] on any machine.
2. Run `ddev release build upsc` to build the package.
3. [Download the Datadog Agent][1].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/upsc/dist/<ARTIFACT_NAME>.whl`.


### Configuration

To configure the UPSC check:

1. Create a `upsc.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `upsc.d/` folder previously created.
3. Consult the [sample upsc.yaml][2] file and copy its content in the `conf.yaml` file.
4. Edit the `conf.yaml` file to point to your server and port, set the masters to monitor.
5. [Restart the Agent][3].

## Validation

[Run the Agent's `status` subcommand][4] and look for `upsc` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][5] for a list of metrics provided by this check.

### Events
The UPSC check does not include any events.

### Service Checks
The UPSC check does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][6].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/upsc/datadog_checks/upsc/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/upsc/metadata.csv
[6]: http://docs.datadoghq.com/help/
[7]: https://github.com/DataDog/integrations-core/blob/master/docs/dev/new_check_howto.md#developer-toolkit
