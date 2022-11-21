# Agent Check: kamailio

## Overview

This check monitors [kamailio][1].

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

4. Build the `datadog-kamailio` package:

```shell
ddev -e release build kamailio
```

### Installing

Once you built the package wheel, install it on a host:

1. If the datadog agent is not installed yet [Install the Datadog Agent][2].

2. Install the package:

```shell
chown dd-agent:dd-agent kamailio/dist/datadog_kamailio*.whl
sudo -u dd-agent datadog-agent integration install -w kamailio/dist/datadog_kamailio*.whl
```

### Configuration

1. Edit the config file `/etc/datadog-agent/conf.d/kamailio.d/conf.yaml.example` per your settings.  
   An example config can be found [here][7].  
   Save the modified file as `/etc/datadog-agent/conf.d/kamailio.d/conf.yaml`.

2. [Restart the Agent][8].

### Validation

1. Check the [agent status][9] and make sure `kamailio` is listed under the Checks section.

## Data Collected

### Metrics

Currently all statistics produced from kamailio are forwarded to datadog.  
See the [kamailio modules][5] documentation for information on statistics produced by each module.    
To see what statistics your kamailio instance will produce run:

```shell
kamcmd stats.get_statistics all
```

For more information see [metadata.csv][11] for an example of metrics that may be collected.

### Service Checks

1. services_up - validates the kamailio services are running properly
2. metrics_up  - validates the metrics were sent to datadog successfully

For more information see [service_checks.json][10] for the service check definitions. 

### Events

The kamailio agent does not include any events.

## Troubleshooting

Need help? Contact [dOpenSource][4].

[1]: https://www.kamailio.org/w/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://dopensource.com/
[5]: https://kamailio.org/docs/modules/5.5.x/
[6]: https://www.kamailio.org/wiki/cookbooks/5.5.x/core#statistics
[7]: https://github.com/DataDog/integrations-extras/blob/master/kamailio/datadog_checks/kamailio/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: https://github.com/DataDog/integrations-extras/blob/master/kamailio/assets/service_checks.json
[11]: https://github.com/DataDog/integrations-extras/blob/master/kamailio/metadata.csv
