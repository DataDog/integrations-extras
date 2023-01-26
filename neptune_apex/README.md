# Agent Check: Neptune Apex

## Overview

This check monitors [Neptune Apex][1].

## Setup

### Installation

To install the Neptune Apex check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build neptune_apex` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/neptune_apex/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit your `/etc/datadog-agent/conf.d/neptune_apex.d/conf.yaml` and add your entry to your in-network apex controller.
2. At a minimum, specify the `address`, which is generally `http://your_apex_controller_ip`.

### Validation

1. First, ensure your `address` is correct. You can use `curl` or a browser and load `http://your_apex_controller_ip/cgi-bin/status.xml`. This should load an xml document.
2. Use `datadog-agent status` and search for the `neptune_apex` status line to indicate any errors collecting.

## Data Collected

### Metrics

Neptune Apex includes several metrics on your available probes and outlets. This includes watts and amperes for 120V outlets or any 
device that draws power. For alarms, an additional metric of the "status" is available if the alarm is configured.

### Service Checks

Neptune Apex includes one service check, which is the ability to connect to the device. Monitor this service check to receive an alert if your whole Apex controller suddenly goes offline.

### Events

Neptune Apex includes outlet events. Outlet events happen if you turn outlets on or off.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://apexfusion.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/neptune_apex/datadog_checks/neptune_apex/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/neptune_apex/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/neptune_apex/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/

