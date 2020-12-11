# Agent Check: php_apcu

## Overview

This check monitors [PHP APCu][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the `php_apcu` check on your host:


1. Install the [developer toolkit][3].
 on any machine.

2. Run `ddev release build php_apcu` to build the package.

3. [Download the Datadog Agent][4].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/php_apcu/dist/<ARTIFACT_NAME>.whl`.

#### APCu Setup

Provide a URL to the collection program.

APCu does not have a metric output by itself.

* /opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/php_apcu/assets/exporter/apcu-dd-handler.php

It will work if you refer to it as a php file, but you may want to configure it as follows

```
Alias /apcu-status /opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/php_apcu/assets/exporter/apcu-dd-handler.php
<Location /apcu-status>
    Require all denied
    Require local
</Location>
```

### Configuration

1. Edit the `php_apcu.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your `php_apcu` performance data. See the [sample `php_apcu.d/conf.yaml` file][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `php_apcu` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

`php_apcu` does not include any service checks.

### Events

`php_apcu` does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://www.php.net/manual/en/book.apcu.php
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/php_apcu/datadog_checks/php_apcu/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/php_apcu/metadata.csv
[9]: https://docs.datadoghq.com/help/
