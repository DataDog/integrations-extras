# nifi Integration

## Overview

[...]

* You can also use images here:

![snapshot](https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png)

## Setup

### Installation

[...]

### Configuration

Create a `nifi.yaml` in the Datadog Agent's `conf.d` directory.

#### Metric Collection

Add this configuration setup to your `nifi.yaml` file to start gathering your [metrics](#metrics):

```
init_config:

instances:
  - []
```

Configuration Options:

[...]

[Restart the Agent](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent) to begin sending Redis metrics to Datadog.

### Validation

[Run the Agent's `status` subcommand](https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information) and look for `nifi` under the Checks section:

```
  Checks
  ======
    [...]

    nifi
    -------
      - instance #0 [OK]
      - Collected 26 metrics, 0 events & 1 service check

    [...]
```

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv](metadata.csv) for a list of metrics provided by this integration.

### Events

The nifi check does not include any event at this time.

### Service Checks

[...]

## Troubleshooting

[...]

## Development

Please refer to the [main documentation](https://docs.datadoghq.com/developers/)
for more details about how to test and develop Agent based integrations.
