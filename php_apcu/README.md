# Agent Check: php_apcu

## Overview

This check monitors [PHP APCu][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

If you are using Agent v6.8+ follow the instructions below to install the `php_apcu` check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior to version 6.8][4] or the [Docker Agent][5]:

1. [Download the Datadog Agent][6].

2. Run the following command to install the integrations wheel with the Agent:

   ```shell
      datadog-agent integration install -t datadog-php_apcu==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][7].

#### APCu

APCu does not expose metrics by default so this integration includes a metric exporter, located here:

```
/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/php_apcu/assets/exporter/apcu-dd-handler.php
```
You can download the exporter [here][5].

When you configure your Agent (the `instances` setting, described next), you can refer to the exporter directly by this file name, or you can configure an alias for it on your web server. For example, if you're using Apache, the alias in the web server configuration file would look like this:

```
Alias /apcu-status /opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/php_apcu/assets/exporter/apcu-dd-handler.php
<Location /apcu-status>
    Require all denied
    Require local
</Location>
```

### Configuration

1. Edit the `php_apcu.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your `php_apcu` performance data. See the [sample `php_apcu.d/conf.yaml` file][8] for all available configuration options.
    ```
    instances
      - url: http://localhost/apcu-status
    ```

2. [Restart the Agent][9].

### Validation

[Run the Agent's status subcommand][10] and look for `php_apcu` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][11] for a list of metrics provided by this check.

### Events

The PHP APCu integration does not include any events.

### Service Checks

See [service_checks.json][13] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][12].


[1]: https://www.php.net/manual/en/book.apcu.php
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[5]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations/
[8]: https://github.com/DataDog/integrations-extras/blob/master/php_apcu/datadog_checks/php_apcu/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[10]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[11]: https://github.com/DataDog/integrations-extras/blob/master/php_apcu/metadata.csv
[12]: https://docs.datadoghq.com/help/
[13]: https://github.com/DataDog/integrations-extras/blob/master/php_apcu/assets/service_checks.json
