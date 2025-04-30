# Agent Check: filemage

## Overview

This check monitors [FileMage][1].

## Setup

### Installing the package

For the Datadog Agent v7.21 or v6.21 and later, follow these instructions to install the Filemage integration on your host.  
See [Use Community Integrations][11] to install it with the Docker Agent or earlier versions of the Datadog Agent.  

1. Run the following command to install the Agent integration:

```shell
datadog-agent integration install -t datadog-filemage==1.0.0
```

2. Configure your integration similar to an Agent-based [integration][3].

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

    filemage (1.0.0)
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
[2]: /account/settings/agent/latest
[3]: https://docs.datadoghq.com/getting_started/integrations/
[4]: https://dopensource.com/
[5]: https://github.com/DataDog/integrations-extras/blob/master/filemage/datadog_checks/filemage/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/filemage/assets/service_checks.json
[9]: https://github.com/DataDog/integrations-extras/blob/master/filemage/metadata.csv
[10]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[11]: https://docs.datadoghq.com/agent/guide/use-community-integrations/

