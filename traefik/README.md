# traefik Integration

## Overview

This integration collects data from Traefik in order to check its health and monitor:

- Errors logs (4xx codes, 5xx codes)
- Number of requests
- Number of bytes exchanged


## Setup

### Installation

To install the Traefik check on your host:
1. [Download the Datadog Agent][12].
2. Download the [`check.py` file][11] for Traefik.
3. Place it in the Agent's `checks.d` directory.
4. Rename it to `traefik.py`.

### Configuration

1. Edit the `traefik.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][7] to start collecting your Traefik [metrics](#metric-collection) and [logs](#log-collection).
  See the [sample traefik.d/conf.yaml][8] for all available configuration options.

2. [Restart the Agent][3]

#### Metric Collection

Add this configuration setup to your `traefik.yaml` file to start gathering your [metrics][2]:

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

[Restart the Agent][3] to begin sending Traefik metrics to Datadog.

#### Log Collection

**Available for Agent >6.0**

By default [Traefik logs][9] are sent to stdout. This should not be changed for containerized version, as the Datadog Agent is able to collect logs directly from container `Stdout`/`Stderr`.

To configure Traefik to log to a file, add the following in the Traefik configuration file:

```
[traefikLog]
  filePath = "/path/to/traefik.log"
```

The [common Apache Access format][10] is used by default and is supported by this integration.

1. Collecting logs is disabled by default in the Datadog Agent. Enable it in your `datadog.yaml` file with:

      ```yaml
      logs_enabled: true
      ```


2.  Add this configuration block to your `traefik.d/conf.yaml` file  at the root of your [Agent's configuration directory][7] to start collecting your Traefik logs:

      ```yaml
      logs:
        - type: file
          path: /path/to/traefik.log
          source: traefik
          service: traefik
      ```

* Change the `path` and `service` parameter values and configure them for your environment. 

* [Restart the Agent][3]

### Validation

[Run the Agent's `status` subcommand][4] and look for `traefik` under the Checks section:

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

See [metadata.csv][5] for a list of metrics provided by this integration.

### Events

The Traefik check does not include any events.

### Service Checks

Query Traefik and expect `200` as return status code.

## Development

Refer to the [main documentation][6] for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png
[2]: #metrics
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[6]: https://docs.datadoghq.com/developers/
[7]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[8]: https://github.com/DataDog/integrations-extras/blob/master/traefik/conf.yaml.example
[9]: https://docs.traefik.io/configuration/logs/#traefik-logs
[10]: https://docs.traefik.io/configuration/logs/#clf-common-log-format
[11]: https://github.com/DataDog/integrations-extras/blob/master/traefik/datadog_checks/traefik/traefik.py
[12]: https://app.datadoghq.com/account/settings#agent
