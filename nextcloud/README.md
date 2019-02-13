# Agent Check: Nextcloud

## Overview

This check monitors [Nextcloud][1].

## Setup

### Installation

The Nextcloud check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `nextcloud.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your nextcloud performance data.
   See the [sample nextcloud.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3]

### Validation

[Run the Agent's `status` subcommand][4] and look for `nextcloud` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this check.

### Service Checks

**`nextcloud.can_connect`**

The check returns:

* `OK` if Nextcloud is reachable.
* `CRITICAL` if Nextcloud is unreachable.


### Events

Nextcloud does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][6].

[1]: https://nextcloud.com/
[2]: https://github.com/DataDog/integrations-core/blob/master/nextcloud/datadog_checks/nextcloud/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/integrations-extras/blob/master/nextcloud/metadata.csv
[5]: https://docs.datadoghq.com/help/
