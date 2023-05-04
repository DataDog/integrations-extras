# Twingate

## Overview

[Twingate][1] is a zero trust network access platform that allows fast growing companies to quickly and easily provide secure access to their AWS environment. By incorporating modern technologies such as NAT traversal, QUIC, private proxies, and split tunneling, Twingate can replace a traditional or cloud VPN while improving user performance and overall security.

This integration allows organizations to monitor a user's resource access activities in real time.

## Setup
### Prerequisites
1. You have the Datadog Agent installed on the Twingate Connector server. You must be able to connect to that host and edit the files to configure the Agent and YAML Integration Configs. To install the Datadog Agent, see [Getting Started with the Agent][11].
2. You must deploy the Twingate Connector. To enable real-time connection logs, see the [Twingate documentation][3].

### Configure the Datadog Agent
#### Systemd Connector
1. Set up [Datadog journald integration][5].
2. Replace the content of `journald.d/conf.yaml` with [this][17]
3. Add the `dd-agent` user to the `systemd-journal` group by using `usermod -a -G systemd-journal dd-agent`.
4. Restart the Datadog Agent by running `service datadog-agent restart`
5. Confirm that the Twingate Analytic log appears in the [Log Explorer][10]


#### Docker Connector
1. Set up [Datadog Docker integration][13]
      1. For host agent
         * Add additional configuration `container_exclude: ["image:.*"]` and `container_include: ["image:twingate/connector"]` to the configuration file `datadog.yaml`
         * See example configuration [here][16]
         * Add the `dd-agent` user to the `docker` group by using `usermod -a -G docker dd-agent`
      2. For container agent
         * add additional parameters `-e DD_CONTAINER_EXCLUDE="image:.*"` and `-e DD_CONTAINER_INCLUDE="image:twingate/connector"` in the docker run command
      3. See example docker run command [here][18]
      4. see [Container Discovery Management][14] for details
2. Set up Twingate Connector with additional docker parameters
   1. Additional label `com.datadoghq.ad.logs` is required by the Twingate Connector container
   2. The Twingate Connector container needs to be recreated to add the additional label 
   3. See example Twingate connector deployment command with the additional label `com.datadoghq.ad.logs` [here][19]
   5. See [Container Log Integration][15] for more details

### Twingate Analytics Dashboard
1. Go to the Datadog [Dashboard List][12].
2. Search for the Twingate Analytics dashboard.

## Troubleshooting
Need help? Contact [Twingate Support][2].

[1]: https://www.twingate.com/
[2]: https://help.twingate.com/hc/en-us
[3]: https://docs.twingate.com/docs/connector-real-time-logs
[4]: https://app.datadoghq.com/account/settings#agent
[5]: https://docs.datadoghq.com/agent/logs/?tab=journald
[6]: https://docs.datadoghq.com/logs/explorer/facets/#manage-facets
[7]: https://docs.datadoghq.com/logs/log_configuration/pipelines/?tab=source#create-a-pipeline
[8]: https://raw.githubusercontent.com/Twingate-Labs/datadog-integrations-extras/master/twingate/images/dashboard.png
[9]: https://docs.datadoghq.com/logs/explorer/facets/#measures
[10]: https://app.datadoghq.com/logs
[11]: https://docs.datadoghq.com/getting_started/agent/
[12]: https://app.datadoghq.com/dashboard/lists
[13]: https://docs.datadoghq.com/containers/docker/log/?tab=containerinstallation#installation
[14]: https://docs.datadoghq.com/agent/guide/autodiscovery-management/?tab=agent_
[15]: https://docs.datadoghq.com/containers/docker/log/?tab=containerinstallation#log-integrations
[16]: https://gist.github.com/chenbishop/3f1b9833f274716949a40af385e2f5c2
[17]: https://gist.github.com/chenbishop/7df60e074e7e856e17d867b31f6e95a1
[18]: https://gist.github.com/chenbishop/3be2bcc90d7d77288a843de469f0b3d0
[19]: https://gist.github.com/chenbishop/a5405cc00bc1ac50fdbd86ef4ad23599