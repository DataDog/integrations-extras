# Traefik Integration

## Overview

This integration collects data from [Traefik][1] in order to check its health and monitor:

- Errors logs (4xx codes, 5xx codes)
- Number of requests
- Number of bytes exchanged

## Setup

### Installation

If you are using Agent v6.8+ follow the instructions below to install the Traefik check on your host. See our dedicated Agent guide about [how to install Community integration][2] to see how to install them with the [Agent prior v6.8][3] or the [Docker Agent][4]:

1. Install the [developer toolkit][5].
2. Clone the integrations-extras repository:

    ```
    git clone https://github.com/DataDog/integrations-extras.git.
    ```

3. Update your `ddev` config with the `integrations-extras/` path:

    ```
    ddev config set extras ./integrations-extras
    ```

4. To build the `traefik` package, run:

    ```
    ddev -e release build traefik
    ```

5. [Download and launch the Datadog Agent][6].
6. Run the following command to install the integrations wheel with the Agent:

    ```
    datadog-agent integration install -w <PATH_OF_TRAEFIK_ARTIFACT_>/<TRAEFIK_ARTIFACT_NAME>.whl
    ```

7. Configure your integration like [any other packaged integration][7].
8. [Restart the Agent][8].

### Configuration

1. Edit the `traefik.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][9] to start collecting your Traefik [metrics](#metric-collection) or [logs](#log-collection).
  See the [sample traefik.d/conf.yaml][10] for all available configuration options.

2. [Restart the Agent][11]

#### Metric Collection

Add this configuration setup to your `traefik.yaml` file to start gathering your [metrics][12]:

```
init_config:

instances:
  - host: 10.1.2.3
    port: "8080"
    path: "/health"
```

Configuration Options:

- host: Traefik endpoint to query. __Required__
- port: API listener of Traefik endpoint. Default value `8080`. _Optional_
- path: Path of Traefik health check endpoint. Default `/health`. _Optional_

[Restart the Agent][11] to begin sending Traefik metrics to Datadog.

#### Log Collection

**Available for Agent >6.0**

By default [Traefik logs][13] are sent to stdout. This should not be changed for containerized version, as the Datadog Agent is able to collect logs directly from container `stdout`/`stderr`.

To configure Traefik to log to a file, add the following in the Traefik configuration file:

```
[traefikLog]
  filePath = "/path/to/traefik.log"
```

The [common Apache Access format][14] is used by default and is supported by this integration.

1. Collecting logs is disabled by default in the Datadog Agent. Enable it in your `datadog.yaml` file with:

      ```yaml
      logs_enabled: true
      ```


2.  Add this configuration block to your `traefik.d/conf.yaml` file at the root of your [Agent's configuration directory][9] to start collecting your Traefik logs:

      ```yaml
      logs:
        - type: file
          path: /path/to/traefik.log
          source: traefik
          service: traefik
      ```

* Change the `path` and `service` parameter values and configure them for your environment.

* [Restart the Agent][11]

### Validation

[Run the Agent's `status` subcommand][15] and look for `traefik` under the Checks section.

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][12] for a list of metrics provided by this integration.

### Events

The Traefik check does not include any events.

### Service Checks

Query Traefik and expect `200` as return status code.

## Development

Refer to the [main documentation][16] for more details about how to test and develop Agent based integrations.

[1]: https://traefik.io
[2]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentpriorto68
[4]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=docker
[5]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[6]: https://app.datadoghq.com/account/settings#agent
[7]: https://docs.datadoghq.com/getting_started/integrations
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#restart-the-agent
[9]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[10]: https://github.com/DataDog/integrations-extras/blob/master/traefik/datadog_checks/traefik/data/conf.yaml.example
[11]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[12]: https://github.com/DataDog/integrations-extras/blob/master/traefik/metadata.csv
[13]: https://docs.traefik.io/configuration/logs/#traefik-logs
[14]: https://docs.traefik.io/configuration/logs/#clf-common-log-format
[15]: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6#service-status
[16]: https://docs.datadoghq.com/developers
