# Agent Check: php_opcache

## Overview

This check monitors [PHP OPcache][1] through the Datadog Agent.

## Setup

Follow the instructions below to install and configure this check for an Agent running on a host. For containerized environments, see the [Autodiscovery Integration Templates][2] for guidance on applying these instructions.

### Installation

To install the `php_opcache` check on your host:


1. Install the [developer toolkit][3].
 on any machine.

2. Run `ddev release build php_opcache` to build the package.

3. [Download the Datadog Agent][4].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/php_opcache/dist/<ARTIFACT_NAME>.whl`.

#### OPcache Setup


OPcache does not expose metrics by default so this integration includes a metric exporter, located here:

    ```
    /opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/php_opcache/assets/exporter/opcache-dd-handler.php
    ```

When you configure your Agent (the `instances` setting, described next), you can refer to the exporter directly. by this file name, or you can configure an alias for it on your web server. For example, if you're using Apache, the alias in the web server configuration file would look like this:

```
Alias /opcache-status /opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/php_opcache/assets/exporter/opcache-dd-handler.php
<Location /opcache-status>
    Require all denied
    Require local
</Location>
```

### Configuration

1. Edit the `php_opcache.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your `php_opcache` performance data. See the [sample `php_opcache.d/conf.yaml` file][5] for all available configuration options.
    ```
    instances
      - url: http://localhost/opcache-status
    ```
2. [Restart the Agent][6].

### Validation

[Run the Agent's status subcommand][7] and look for `php_opcache` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

`php_opcache` does not include any service checks.

### Events

`php_opcache` does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][9].

[1]: https://www.php.net/manual/en/book.opcache.php
[2]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://github.com/DataDog/integrations-extras/blob/master/php_opcache/datadog_checks/php_opcache/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/php_opcache/metadata.csv
[9]: https://docs.datadoghq.com/help/
