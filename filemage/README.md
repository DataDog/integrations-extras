# Agent Check: filemage

## Overview

This check monitors [FileMage][1].

## Setup

### Building the package

1. Install the [Datadog Developer Toolkit][3].

2. Clone the `integrations-extras` repository:

```shell
git clone https://github.com/DataDog/integrations-extras.git
```

3. Update your `ddev` config with the repo path:

```shell
cd integrations-extras/
ddev config set extras $(pwd)
```

4. Build the `datadog-filemage` package:

```shell
ddev -e release build filemage
```

### Installing the package

Once you've built the wheel package, install it on a host:

1. Ensure that the [Datadog Agent][2] is installed.

2. Install the package:

```shell
chown dd-agent:dd-agent filemage/dist/datadog_filemage*.whl
sudo -u dd-agent datadog-agent integration install -w filemage/dist/datadog_filemage*.whl
```

### Configuration

1. Edit the `filemage.d/conf.yaml.example` file in the `conf.d/` folder at the root of your [Agent Configuration Directory][10] to start collecting your FileMage [metrics](#metrics).  
   Once complete, save the modified file as `filemage.d/conf.yaml`.  
   See the [sample filemage conf.yaml][5] for all available configuration options.

2. [Restart the Agent][6].

### Validation

Run the [Agent's `status` subcommand][7] and look for `filemage` under the Running Checks section.


```text
...

  Running Checks
  ==============

    ...

    filemage (0.0.1)
    ----------------
      Instance ID: filemage:ac55127bf7bd70b9 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/filemage.d/conf.yaml
      Total Runs: 1,298
      Metric Samples: Last Run: 0, Total: 0
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 2, Total: 2,594
      Average Execution Time : 41ms
      Last Execution Date : 2022-11-23 15:59:22 EST / 2022-11-23 20:59:22 UTC (1669237162000)
      Last Successful Execution Date : 2022-11-23 15:59:22 EST / 2022-11-23 20:59:22 UTC (1669237162000)
```


## Data Collected

This integration tracks the number of times each FTP command is run.

### Metrics

See [metadata.csv][9] for the full list of possible metrics provided by this check.

### Service Checks

See [service_checks.json][8] for a list of service checks provided by this integration. 

### Events

The FileMage integration does not include any events.

## Troubleshooting

Need help? Contact [dOpenSource][4].

[1]: https://www.filemage.io/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://dopensource.com/
[5]: ./datadog_checks/filemage/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: ./assets/service_checks.json
[9]: ./datadog_checks/filemage/metadata.csv
[10]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
