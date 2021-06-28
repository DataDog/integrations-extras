# NS1 Integration

## Overview

This integration monitors [NS1][1] services through the Datadog Agent

![Snap](https://raw.githubusercontent.com/DataDog/integrations-extras/master/ns1/images/overview.png)

## Setup

Download and install the [Datadog Agent][2], then follow the instructions below to install and configure this integration for an Agent running on a host.


## Installation

Refer to Datadog’s [community integrations installation][3] page for the specific steps to install the NS1 integration as an add-on, since it is not packaged and built into the Datadog Agent. 

**Note**: The minimum Agent version required for supporting integrations is 7.21.0. NS1 recommends using the latest version of the Datadog Agent.

When running the installation process, make sure to do so using the following variables specific to the NS1 integration:


* <INTEGRATION_NAME>:  NS1
* <INTEGRATION_VERSION>:  0.0.3



## Configuration

To configure and activate the NS1 integration, follow the steps [here][4]. 

See the [sample ns1.d/conf.yaml][5] for all available configuration options.


### Validation

To validate your Agent and integration configuration, [run the Agent's status subcommand][6] and look for ns1 under the Checks section.


## Data Collected

## Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

## Service Checks

The NS1 integration sends the following service check after each run:

`ns1.can_connect` returns CRITICAL if the Agent fails to receive a 200 response code from the NS1 API endpoint or returns OK if all endpoints respond properly.


## Events

The NS1 integration does not include any events.


## Troubleshooting

Need help? Contact [Datadog support][8].

For more details about this integration, see the [NS1 + Datadog Integration][9] article in the NS1 Help Center.

[1]: https://ns1.com/
[2]: https://app.datadoghq.com/account/settings#agent/overview
[3]: https://docs.datadoghq.com/agent/guide/community-integrations-installation-with-docker-agent/?tab=agentabovev68
[4]: https://docs.datadoghq.com/getting_started/integrations/#configuring-agent-integrations
[5]: https://github.com/DataDog/integrations-extras/blob/master/ns1/datadog_checks/ns1/data/conf.yaml.example
[7]: hhttps://github.com/DataDog/integrations-extras/blob/master/ns1/metadata.csv
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/ns1/metadata.csv
[8]: https://docs.datadoghq.com/help/
[9]: https://help.ns1.com/hc/en-us/articles/4402752547219