
# Bind9 check Integration

## Overview

Get metrics from Bind9 DNS Server.

* Visualize and monitor bind9 stats
![Snap](https://raw.githubusercontent.com/DataDog/integrations-extras/master/bind9/images/snapshot.png)

## Setup

The Bind9 check is **NOT** included in the [Datadog Agent](https://app.datadoghq.com/account/settings#agent) package.

### Installation

To install the Bind9 check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][7].
2. Download the [`bind9.py` file][8] for Bind9.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit](https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit) on any machine.
2. Run `ddev release build bind9` to build the package.
3. [Download the Datadog Agent](https://app.datadoghq.com/account/settings#agent).
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w <BIND9_DIST_PATH>/<ARTIFACT_NAME>.whl`.

### Configuration

To configure the bind9 check:

1. Create a `bind9.d/` folder in the `conf.d/` folder at the root of your Agent's directory.
2. Create a `conf.yaml` file in the `bind9.d/` folder previously created.
3. Consult the [sample bind9.yaml][2] file and copy its content in the `conf.yaml` file.
4. [Restart the Agent][3].

#### Metric Collection

Add this configuration setup to your `conf.yaml` file to start gathering your [metrics][2]:

```
init_config:

instances:
  - URL : <BIND_9_STATS_URL>
```

### Validation

[Run the Agent's `status` subcommand][4] and look for `bind9` under the Checks section.

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

## Development

Please refer to the [main documentation][6] for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png
[2]: #metrics
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[6]: https://docs.datadoghq.com/developers/
[7]: https://app.datadoghq.com/account/settings#agent
[8]: https://github.com/DataDog/integrations-extras/blob/master/bind9/datadog_checks/bind9/bind9.py
