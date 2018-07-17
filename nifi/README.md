# Nifi Integration

## Overview

![snapshot][1]

## Setup
### Installation

### Configuration

Create a `nifi.yaml` in the Datadog Agent's `conf.d` directory.

1. Edit the `nifi/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory.
    See the sample `conf.yaml.example` file for all available configuration options:

    ```yaml
      instances:
        - url: http://localhost:8080
          tags: []
    ```

2. [Restart the Agent][2] to begin sending Nifi metrics to Datadog.

### Validation

[Run the Agent's `status` subcommand][3] and look for `nifi` under the Checks section:

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

## Data Collected
### Metrics

See [metadata.csv](metadata.csv) for a list of metrics provided by this integration.

### Events

The nifi check does not include any event at this time.

### Service Checks

`nifi.instance.http_check`:

Returns `CRITICAL` if the Agent check is unable to connect to the monitored Nifi instance. 
Returns `WARNING` if the attempt to connect timeout, returns `OK` otherwise.

## Troubleshooting


## Development

Please refer to the [main documentation][4]
for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png
[2]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[4]: https://docs.datadoghq.com/developers
