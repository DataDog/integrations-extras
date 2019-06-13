# Traefik Integration

## Overview

This integration collects data from [Traefik][1] in order to check its health and monitor:

- Errors logs (4xx codes, 5xx codes)
- Number of requests
- Number of bytes exchanged

## Setup

### Installation

To install the Traefik check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][2].
2. Download the [`traefik.py` file][12] for Traefik.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit][3] on any machine.
2. Run `ddev release build traefik` to build the package.
3. [Download the Datadog Agent][2].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/traefik/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `traefik.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][4] to start collecting your Traefik [metrics](#metric-collection) and [logs](#log-collection).
  See the [sample traefik.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6]

#### Metric Collection

Add this configuration setup to your `traefik.yaml` file to start gathering your [metrics][7]:

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

[Restart the Agent][6] to begin sending Traefik metrics to Datadog.

#### Log Collection

**Available for Agent >6.0**

By default [Traefik logs][8] are sent to stdout. This should not be changed for containerized version, as the Datadog Agent is able to collect logs directly from container `stdout`/`stderr`.

To configure Traefik to log to a file, add the following in the Traefik configuration file:

```
[traefikLog]
  filePath = "/path/to/traefik.log"
```

The [common Apache Access format][9] is used by default and is supported by this integration.

1. Collecting logs is disabled by default in the Datadog Agent. Enable it in your `datadog.yaml` file with:

      ```yaml
      logs_enabled: true
      ```


2.  Add this configuration block to your `traefik.d/conf.yaml` file at the root of your [Agent's configuration directory][4] to start collecting your Traefik logs:

      ```yaml
      logs:
        - type: file
          path: /path/to/traefik.log
          source: traefik
          service: traefik
      ```

* Change the `path` and `service` parameter values and configure them for your environment.

* [Restart the Agent][6]

### Validation

[Run the Agent's `status` subcommand][10] and look for `traefik` under the Checks section:

```
  Checks
  ======
    [...]

    traefik
    -------
      - instance #0 [OK]
      - Collected 2 metrics, 0 events & 1 service check

    [...]
```

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Events

The Traefik check does not include any events.

### Service Checks

Query Traefik and expect `200` as return status code.

## Development

Refer to the [main documentation][11] for more details about how to test and develop Agent based integrations.

[1]: https://traefik.io
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[5]: https://github.com/DataDog/integrations-extras/blob/master/traefik/datadog_checks/traefik/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[7]: https://github.com/DataDog/integrations-extras/blob/master/traefik/metadata.csv
[8]: https://docs.traefik.io/configuration/logs/#traefik-logs
[9]: https://docs.traefik.io/configuration/logs/#clf-common-log-format
[10]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[11]: https://docs.datadoghq.com/developers/
[12]: https://github.com/DataDog/integrations-extras/blob/master/traefik/datadog_checks/traefik/traefik.py
