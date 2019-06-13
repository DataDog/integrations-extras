# Sortdb Integration

## Overview

Get metrics from [Sortdb][1] service in real time to:

* Visualize and monitor Sortdb stats.
* Be notified about Sortdb failovers.
* Check health of and get stats from multiple instances

## Installation

To install the Sortdb check on your host:

On Agent versions <= 6.8:

1. [Download the Datadog Agent][2].
2. Download the [`sortdb.py` file][7] for Sortdb.
3. Place it in the Agent's `checks.d` directory.

On Agent 6.8+:

1. Install the [developer toolkit][3] on any machine.
2. Run `ddev release build sortdb` to build the package.
3. [Download the Datadog Agent][2].
4. Upload the build artifact to any host with an Agent and run `datadog-agent integration install -w path/to/sortdb/dist/<ARTIFACT_NAME>.whl`.

## Configuration

1. Edit the `sortdb.d/conf.yaml` file in the `conf.d/` folder at the root of your [Agent's configuration directory][4] to start collecting your Sortdb [metrics](#metric-collection) and [logs](#log-collection).
  See the [sample sortdb.d/conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6]

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        sortdb
        -----------
          - instance #0 [OK]
          - Collected 28 metrics, 0 events & 1 service checks

## Compatibility

The sortdb check is compatible with all major platforms

[1]: https://github.com/jehiah/sortdb
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
[5]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/datadog_checks/sortdb/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[7]: https://github.com/DataDog/integrations-extras/blob/master/sortdb/datadog_checks/sortdb/sortdb.py
