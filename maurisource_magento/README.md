# Agent Check: Maurisource Magento Integration

## Overview

This Integration collects Prometheus Metrics exposed by [Magento2 Prometheus Exporter][1].

## Setup

### Install Magento2 Prometheus Exporter

Install the Module via composer by running:

```php
composer require run-as-root/magento2-prometheus-exporter
php bin/magento setup:upgrade
```

### Configuration: Magento2 Prometheus Exporter

The modules system configuration is located under `Stores -> Configuration -> Prometheus -> Metric Configuration`. You can enable or disable specific metrics by using the multiselect.

### Installation

For Agent v7.33.0+, follow the instructions below to install the maurisource_mangento check on your host. See [Use Community and Marketplace Integrations][2] to install with the Docker Agent or earlier versions of the Agent.

1; Run the following command to install the Agent integration:

   ```bash
   datadog-agent integration install -t datadog-maurisource_mangento==<INTEGRATION_VERSION>
   ```

### Configuration

<!-- xxx tabs xxx -->
<!-- xxx tab "Host" xxx -->

#### Host

Configure the Agent running on a host to collect Magento logs and Magento2 Prometheus Exporter Metrics:

##### Metric collection

1; Add this configuration block to your `maurisource_mangento.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][3] to start gathering your [maurisource_mangento Metrics](#metrics). See the [sample maurisource_mangento.d/conf.yaml][4] for all available configuration options.

```yaml
init_config:

instances:
    ## @param openmetrics_endpoint - string - required
    ## The URL exposing metrics in the OpenMetrics format.
    #
    - openmetrics_endpoint: http://localhost:8001/metrics
```

2; [Restart the Agent][5].

##### Log collection

_Available for Agent versions >6.0_

Magento logs files are found in ```/var/log``` directory within your root Magento installation.

1. Collecting logs is disabled by default in the Datadog Agent, enable it in your `datadog.yaml` file:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `maurisource_mangento.d/conf.yaml` file to start collecting your Magento Logs:

   ```yaml
   logs:
     - type: file
       path: /var/log/cron.log
       service: '<SERVICE>'
       source: mangento

     - type: file
       path: /var/log/debug.log
       service: '<SERVICE>'
       source: mangento
   ```

    Change the `path` and `service` parameter values and configure them for your environment. See the [sample maurisource_mangento.d/conf.yaml][4] for all available configuration options.

3. [Restart the Agent][5].

<!-- xxz tab xxx -->
<!-- xxx tab "Containerized" xxx -->

#### Containerized

For containerized environments, see the [Container Monitoring][6] for guidance on applying the parameters below.

##### Metric collection

| Parameter            | Value                                                 |
| -------------------- | ----------------------------------------------------- |
| `<INTEGRATION_NAME>` | `maurisource_mangento`                                |
| `<INIT_CONFIG>`      | blank or `{}`                                         |
| `<INSTANCE_CONFIG>`  | `{"openmetrics_endpoint": "http://%%host%%:<magento_port>/metrics"}` |

##### Log collection

_Available for Agent versions >6.0_

1; Follow the [Custom Log Collection documentation][8] to tail files for logs.

To gather logs from your <APP_NAME> application stored in <PATH_LOG_FILE>/<LOG_FILE_NAME>.log create a <APP_NAME>.d/conf.yaml file at the root of your [Agent's configuration directory][3] with the following content.[sample maurisource_mangento.d/conf.yaml][4] for log configuration options.:

```yaml
   logs:
     - type: file
       path: /var/log/<log_file>
       service: '<SERVICE>'
       source: mangento
```

2; [Restart the Agent][5].

### Validation

[Run the Agent's status subcommand][9] and look for `maurisource_mangento` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Service Checks

See [service_checks.json][11] for a list of service checks provided by this integration.

### Events

This Integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][12].

[1]: https://github.com/run-as-root/magento2-prometheus-exporter
[2]: https://docs.datadoghq.com/agent/guide/use-community-integrations
[3]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[4]: https://github.com/MaurisourceINC/datadog-integrations-extras/blob/master/maurisource_mangento/datadog_checks/maurisource_mangento/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/containers/
[7]: https://docs.datadoghq.com/containers/docker/log/?tab=hostagentwithcustomlogging#
[8]: https://docs.datadoghq.com/agent/logs/#custom-log-collection
[9]: https://docs.datadoghq.com/agent/configuration/agent-commands/#agent-status-and-information
[10]: https://github.com/MaurisourceINC/datadog-integrations-extras/blob/master/maurisource_mangento/datadog_checks/maurisource_mangento/metadata.csv
[11]: https://github.com/MaurisourceINC/datadog-integrations-extras/blob/master/maurisource_mangento/datadog_checks/maurisource_mangento/assets/service_checks.json
[12]: https://docs.datadoghq.com/help/
https://app.datadoghq.com/account/settings/agent/latest
https://maurisource.com/
[4]: https://github.com/MaurisourceINC/datadog-integrations-extras.git