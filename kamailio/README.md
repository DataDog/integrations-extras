# Agent Check: kamailio

## Overview

This check monitors [Kamailio][1].

## Setup

### Installing the package

For the Datadog Agent v7.21 or v6.21 and later, follow these instructions to install the Filemage integration on your host.  
See [Use Community Integrations][13] to install it with the Docker Agent or earlier versions of the Datadog Agent.  

1. Run the following command to install the Agent integration:

```shell
datadog-agent integration install -t datadog-filemage==1.0.0
```

If you need a specific version simply change the version number in the command above.

2. Configure your integration similar to an Agent-based [integration][3].

### Configuration

1. Determine how your Kamailio configuration exposes the RPC API.  
   The Kamailio insteegration supports connecting via JSONRPC or BINRPC (i.e. `kamcmd`).  
   For more information see the Kamailio documentation on the [jsonrpcs][14] and [ctl][15] modules.

2. Configure the integration to communicate with Kamailio via the RPC API you identified above.  
   **If** you are using the JSONRPC interface, you need to update the `jsonrpc_config` parameter to match your connection settings.  
   This setting is configured in the `kamailio.d/conf.yaml.example` file in the `conf.d/` folder at the root of your [Agent Configuration Directory][12].  
   **If** you are using the BINRPC interface, you need to allow the `dd-agent` user to access your BINRPC interface.  
   The simplest way to do this is to use the pre-configured *sudoers* config bundled with this integration.  
   First, ensure `sudo` is installed on your system, then run the following command:

```shell
cp /opt/datadog-agent/embedded/lib/python*/site-packages/datadog_checks/kamailio/sudoers.d/dd-agent-kamcmd /etc/sudoers.d/
```

   **If** your Kamailio configuration does not load the `kex` module you need to enable the `get_modules_from_mmaps` parameter.  
   This setting is also located in the `kamailio.d/conf.yaml.example` configuration file.  
   You wil also need to allow the `dd-agent` user to read the loaded modules from memory.  
   Another pre-configured *sudoers* config bundled can handle this.  
   To do so run the following command:

```shell
cp /opt/datadog-agent/embedded/lib/python*/site-packages/datadog_checks/kamailio/sudoers.d/dd-agent-procmaps /etc/sudoers.d/
```

3. Now you can edit any optional parameters in `kamailio.d/conf.yaml.example` to suit your environement.  
   Once complete, save the modified file as `kamailio.d/conf.yaml`.  
   See the [sample kamailio conf.yaml][7] for all available configuration options.

4. [Restart the Agent][8].

### Validation

Run the [Agent's `status` subcommand][9] and look for `kamailio` under the Running Checks section.

```shell
sudo -u dd-agent datadog-agent status
```

Here is an example of what the output should look like when the installed succeeded: 

```text
  Running Checks
  ==============

    kamailio (1.0.0)
    ----------------
      Instance ID: kamailio:c1229bbb6f8bedb9 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kamailio.d/conf.yaml
      Total Runs: 141
      Metric Samples: Last Run: 82, Total: 11,562
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 2, Total: 282
      Average Execution Time : 19ms
      Last Execution Date : 2023-01-12 23:10:48 EST / 2023-01-13 04:10:48 UTC (1673583048000)
      Last Successful Execution Date : 2023-01-12 23:10:48 EST / 2023-01-13 04:10:48 UTC (1673583048000)
```

## Data Collected

The data collected depends on what modules are loaded in your Kamailio configuration.  
The intent is that all statistics that can help you better manage your system are forwarded for processing.

### Metrics

See [metadata.csv][11] for the full list of possible metrics provided by this check.

### Service Checks

See [service_checks.json][10] for a list of service checks provided by this integration.

### Events

The Kamailio integration does not include any events.

## Troubleshooting

Need help? Contact [dOpenSource][4].

## Contributing

Have a feature or update to add to this integration?    
Here is how to get started.

1. Install the [Datadog Developer Toolkit][3].

2. Clone the `integrations-extras` repository:

```shell
git clone https://github.com/DataDog/integrations-extras.git
```

3. Update your `ddev` config with the repo path:

```shell
cd integrations-extras
ddev config set extras $(pwd)
```

4. Make your earth-shattering changes.  
   Make sure to follow the recommendations in the [Integration Developer Documentation][16].

5. Run the tests. For example:

```shell
source venv/bin/activate &&
ddev test -fs kamailio &&
ddev validate ci --fix && 
ddev -x validate config -s kamailio && 
ddev validate models kamailio -s && 
ddev test --cov --junit kamailio &&
ddev validate all kamailio
```

At this point you should also test the package on a live system.  
To do this build the package:

```shell
ddev -e release build kamailio
```

Ensure that the [Datadog Agent][2] is installed on your test system.  
Then install the integration:

```shell
chown dd-agent:dd-agent datadog_kamailio-*.whl
sudo -u dd-agent datadog-agent integration install -w datadog_kamailio-*.whl
```

6. Once all the tests pass, update the integration [Version File][17] and open a pull request.

[1]: https://www.kamailio.org/w/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[4]: https://dopensource.com/
[6]: https://www.kamailio.org/wiki/cookbooks/5.5.x/core#statistics
[7]: ./datadog_checks/kamailio/data/conf.yaml.example
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[9]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[10]: ./assets/service_checks.json
[11]: ./metadata.csv
[12]: https://docs.datadoghq.com/agent/guide/agent-configuration-files/#agent-configuration-directory
[13]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
[14]: https://kamailio.org/docs/modules/stable/modules/jsonrpcs.html
[15]: https://kamailio.org/docs/modules/stable/modules/ctl.html
[16]: https://docs.datadoghq.com/developers/integrations/
[17]: ./datadog_checks/kamailio/__about__.py