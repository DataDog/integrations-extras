# Agent Check: filemage

## Overview

This check monitors [filemage][1].

## Setup

### Building

1. Install the [Datadog Developer Toolkit][3].

2. Clone the `integrations-extras` repository:

```shell
git clone https://github.com/DataDog/integrations-extras.git.
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

### Installing

Once you built the package wheel, install it on a host:

1. If the datadog agent is not installed yet [Install the Datadog Agent][2].

2. Install the package:

```shell
chown dd-agent:dd-agent filemage/dist/datadog_filemage*.whl
sudo -u dd-agent datadog-agent integration install -w filemage/dist/datadog_filemage*.whl
```

### Configuration

1. Edit the config file `/etc/datadog-agent/conf.d/filemage.d/conf.yaml.example` per your settings.  
   An example config can be found [here][5].  
   Save the modified file as `/etc/datadog-agent/conf.d/filemage.d/conf.yaml`.

2. [Restart the Agent][6].

### Validation

1. Check the [agent status][7] and make sure `filemage` is listed under the Checks section.

## Data Collected

### Metrics

Currently this integration tracks the number of times each FTP command is run.    
For more information see [metadata.csv][9] where possible metrics are defined.  

### Service Checks

1. services_up - validates the filemage services are running properly
2. metrics_up  - validates the metrics were sent to datadog successfully

For more information see [service_checks.json][8] for the service check definitions. 

### Events

The filemage agent does not include any events.

## Troubleshooting

Need help? Contact [dOpenSource][4].

[1]: https://www.filemage.io/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://dopensource.com/
[5]: https://github.com/DataDog/integrations-extras/blob/master/filemage/datadog_checks/filemage/data/conf.yaml.example
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[7]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[8]: https://github.com/DataDog/integrations-extras/blob/master/filemage/assets/service_checks.json
[9]: https://github.com/DataDog/integrations-extras/blob/master/filemage/metadata.csv
