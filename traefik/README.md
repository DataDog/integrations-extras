# traefik Integration

## Overview

This collect for Traefik and check it health.

## Setup

### Installation

[...]

### Configuration

Create a `traefik.yaml` in the Datadog Agent's `conf.d` directory.

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

[Restart the Agent][3] to begin sending Traefil metrics to Datadog.

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

The traefik check does not include any event at this time.

### Service Checks

Query Traefik and expect `200` as return status code.

## Troubleshooting

[...]

## Development

Please refer to the [main documentation][6]
for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png
[2]: #metrics
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[6]: https://docs.datadoghq.com/developers/