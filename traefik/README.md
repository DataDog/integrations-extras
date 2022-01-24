# Traefik Integration

## Overview

Send [Traefik][1] metrics, logs, and traces to Datadog to monitor your Traefik services.

## Setup

The Traefik check is not included in the [Datadog Agent][2] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Traefik check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-traefik==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

### Configuration

<!-- xxx tabs xxx -->
<!-- xxx tab "v2" xxx -->

#### About v2
For information about the changes from v1 to v2, see the [Traefik migration guide][5]. For information about the latest version, see the [Traefik documentation][6].

#### Metric collection

Follow [Traefix's documentation][7] to send [Traefix metrics][8] to Datadog.

#### Log collection

**Available for Agent >6.0**

By default, [Traefik logs][9] are sent to stdout. This should not be changed for containerized version, because the Datadog Agent can collect logs directly from the container `stdout`/`stderr`.

1. To configure [Traefik to log to a file][9], add the following in the Traefik configuration file:

   ```conf
    log:
      filePath: "/path/to/traefik.log"
    ```
    
    The [common Apache Access format][10] is used by default and is supported by this integration.

2. Collecting logs is disabled by default in the Datadog Agent. Enable it in your `datadog.yaml` file with:

   ```yaml
   logs_enabled: true
   ```

3. Add this configuration block to your `traefik.d/conf.yaml` file at the root of your [Agent's configuration directory][11] to start collecting your Traefik logs:

    ```yaml
    logs:
      - type: file
        path: /path/to/traefik.log
        source: traefik
        service: traefik
    ```

      Change the `path` and `service` parameter values and configure them for your environment.

4. [Restart the Agent][12]

#### Trace collection

1. [Enable APM][13] for Datadog, if needed.
2. Follow [Traefix's documentation][14] to send [traces][15] to Datadog.

<!-- xxz tab xxx -->
<!-- xxx tab "v1" xxx -->

#### About v1

See [Traefik documentation][16] for information about v1. For information about the changes from v1 to v2, see the [Traefik migration guide][17]. 

#### Metric collection

1. To collect Traefik [metrics][17], open the `traefik.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][18]. 

2. Add this configuration setup to your `traefik.d/conf.yaml` file to start gathering your [metrics][17]:

    ```yaml
    init_config:

    instances:
    - host: 10.1.2.3
        port: "8080"
        path: "/health"
        scheme: "http"
    ```

    Configuration Options:

    - host: Traefik endpoint to query. **Required**
    - port: API listener of Traefik endpoint. Default value `8080`. _Optional_
    - path: Path of Traefik health check endpoint. Default `/health`. _Optional_
    - scheme: Scheme of Traefik health check endpoint. Default `http`. _Optional_

3. [Restart the Agent][19] to begin sending Traefik metrics to Datadog.

See the [sample traefik.d/conf.yaml][20] for all available configuration options.

#### Log collection

**Available for Agent >6.0**

By default, [Traefik logs][21] are sent to stdout. This should not be changed for containerized version, as the Datadog Agent is able to collect logs directly from container `stdout`/`stderr`.

1. To configure [Traefik to log to a file][21], add the following in the Traefik configuration file:

    ```conf
    [traefikLog]
    filePath = "/path/to/traefik.log"
    ```

    The [common Apache Access format][22] is used by default and is supported by this integration.

2. Collecting logs is disabled by default in the Datadog Agent. Enable it in your `datadog.yaml` file with:

   ```yaml
   logs_enabled: true
   ```

3. Add this configuration block to your `traefik.d/conf.yaml` file at the root of your [Agent's configuration directory][18] to start collecting your Traefik logs:

    ```yaml
    logs:
      - type: file
        path: /path/to/traefik.log
        source: traefik
        service: traefik
    ```

      Change the `path` and `service` parameter values and configure them for your environment.

4. [Restart the Agent][19]

#### Trace collection

**Available for Traefik v1.7+**

1. [Enable APM][23] for Datadog, if needed.
2. Follow [Traefix's documentation][24] to send traces to Datadog.

<!-- xxz tab xxx -->
<!-- xxz tabs xxx -->

### Validation

[Run the Agent's `status` subcommand][25] and look for `traefik` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

**Metrics**

For v2, see the list of [Traefik metrics][26] sent to Datadog.

For v1, see the list of [metrics][27] provided by the integration.

## Data Collected

### Metrics

See [metadata.csv][28] for a list of metrics provided by this integration.

### Events

The Traefik check does not include any events.

### Service Checks

See [service_checks.json][29] for a list of service checks provided by this integration.

## Troubleshooting

Need help? Contact [Datadog support][30].

[1]: https://traefik.io
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[4]: https://docs.datadoghq.com/getting_started/integrations/
[5]: https://doc.traefik.io/traefik/v2.0/migration/v1-to-v2/
[6]: https://doc.traefik.io/traefik/
[7]: https://doc.traefik.io/traefik/observability/metrics/datadog/
[8]: https://doc.traefik.io/traefik/observability/metrics/overview/
[9]: https://doc.traefik.io/traefik/observability/logs/#filepath
[10]: https://doc.traefik.io/traefik/observability/logs/#format
[11]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[12]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[13]: https://docs.datadoghq.com/getting_started/tracing/#enable-apm
[14]: https://doc.traefik.io/traefik/observability/tracing/datadog/
[15]: https://doc.traefik.io/traefik/observability/tracing/overview/
[16]: https://doc.traefik.io/traefik/v1.7/
[17]: https://github.com/DataDog/integrations-extras/blob/master/traefik/metadata.csv
[18]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[19]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[20]: https://github.com/DataDog/integrations-extras/blob/master/traefik/datadog_checks/traefik/data/conf.yaml.example
[21]: https://doc.traefik.io/traefik/v1.7/configuration/logs/#traefik-logs
[22]: https://doc.traefik.io/traefik/v1.7/configuration/logs/#clf-common-log-format
[23]: https://docs.datadoghq.com/getting_started/tracing/#enable-apm
[24]: https://doc.traefik.io/traefik/v1.7/configuration/tracing/#datadog
[25]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[26]: https://doc.traefik.io/traefik/observability/metrics/overview/
[27]: https://docs.datadoghq.com/integrations/traefik/#metrics
[28]: https://github.com/DataDog/integrations-extras/blob/master/traefik/metadata.csv
[29]: https://github.com/DataDog/integrations-extras/blob/master/traefik/assets/service_checks.json
[30]: https://docs.datadoghq.com/help
