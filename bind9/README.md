
# bind9_check Integration

## Overview

Get metrics from bind9 DNS Server

* Visualize and monitor bind9 stats
![Snap](https://github.com/ashuvyas45/integrations-extras/raw/bind9/bind9_check/images/snapshot.png)

## Setup

### Installation



### Configuration

Create a `bind9_check/bind9_check.yaml` in the Datadog Agent's `conf.d` directory.



#### Metric Collection

Add this configuration setup to your `bind9_check.yaml` file to start gathering your [metrics][2]:

```
init_config:

instances:
  - URL : #DNS Statistical-Channel URL
```

Configuration Options:



[Restart the Agent][3] to begin sending Redis metrics to Datadog.

### Validation

[Run the Agent's `status` subcommand][4] and look for `bind9_check` under the Checks section:

```
  Checks
  ======
    [...]

    bind9_check
    -------
      - instance #0 [OK]
      - Collected 145 metrics, 0 events & 1 service check

    [...]
```

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Events

The bind9_check check does not include any event at this time.

### Service Checks

`bind9_check.BIND_SERVICE_CHECK` : Returns `OK` If Statistics-channel URL of DNS is present in Instance.
`bind9_check.BIND_SERVICE_CHECK` : Returns `CRITICAL` If URL Errors occurs.
## Troubleshooting



## Development

Please refer to the [main documentation][6]
for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png
[2]: #metrics
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[6]: https://docs.datadoghq.com/developers/
