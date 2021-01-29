# Traefik Integration

## Overview

This integration collects data from [Traefik][1] in order to check its health and monitor:

- Errors logs (4xx codes, 5xx codes)
- Number of requests
- Number of bytes exchanged

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Traefik check on your host. See the dedicated Agent guide for [installing community integrations][3] to install checks with the [Agent prior v6.8][4] or the [Docker Agent][5]:

1. [Download and launch the Datadog Agent][5].
2. Run the following command to install the integrations wheel with the Agent:

   ```shell
   datadog-agent integration install -t datadog-traefik==<INTEGRATION_VERSION>
   ```

3. Configure your integration like [any other packaged integration][6].

### Configuration

1. Edit the `traefik.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Traefik [metrics](#metric-collection) or [logs](#log-collection). See the [sample traefik.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][9]

#### Metric Collection

Add this configuration setup to your `traefik.yaml` file to start gathering your [metrics][10]:

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

[Restart the Agent][9] to begin sending Traefik metrics to Datadog.

#### Log Collection

**Available for Agent >6.0**

By default [Traefik logs][11] are sent to stdout. This should not be changed for containerized version, as the Datadog Agent is able to collect logs directly from container `stdout`/`stderr`.

To configure Traefik to log to a file, add the following in the Traefik configuration file:

```conf
[traefikLog]
  filePath = "/path/to/traefik.log"
```

The [common Apache Access format][12] is used by default and is supported by this integration.

1. Collecting logs is disabled by default in the Datadog Agent. Enable it in your `datadog.yaml` file with:

   ```yaml
   logs_enabled: true
   ```

2. Add this configuration block to your `traefik.d/conf.yaml` file at the root of your [Agent's configuration directory][7] to start collecting your Traefik logs:

    ```yaml
    logs:
      - type: file
        path: /path/to/traefik.log
        source: traefik
        service: traefik
    ```

      Change the `path` and `service` parameter values and configure them for your environment.

3. [Restart the Agent][9]

### Validation

[Run the Agent's `status` subcommand][13] and look for `traefik` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this integration.

### Events

The Traefik check does not include any events.

### Service Checks

Query Traefik and expect `200` as return status code.

## Development

Refer to the [main documentation][14] for more details about how to test and develop Agent based integrations.

[1]: https://traefik.io
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://app.datadoghq.com/account/settings#agent
[6]: https://docs.datadoghq.com/getting_started/integrations/
[7]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/traefik/datadog_checks/traefik/data/conf.yaml.example
[9]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[10]: https://github.com/DataDog/integrations-extras/blob/master/traefik/metadata.csv
[11]: https://docs.traefik.io/configuration/logs/#traefik-logs
[12]: https://docs.traefik.io/configuration/logs/#clf-common-log-format
[13]: https://docs.datadoghq.com/agent/guide/agent-commands/#service-status
[14]: https://docs.datadoghq.com/developers/
