# Agent Check: hikaricp

## Overview
[Hikaricp][1] is a lightweight and fast JDBC connection pooling framework.
This check monitors HikariCP through the Datadog Agent.

## Setup

### Installation

To install the HikariCP check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build hikaricp` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/hikaricp/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Edit the `hikaricp/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your hikaricp performance data. See the [sample hikaricp/conf.yaml][4] for all available configuration options.

### Validation

<Steps to validate integration is functioning as expected>

## Data Collected

### Metrics

hikaricp does not include any metrics.

### Service Checks

hikaricp does not include any service checks.

### Events

hikaricp does not include any events. 

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://github.com/brettwooldridge/HikariCP
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/hikaricp/datadog_checks/hikaricp/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/hikaricp/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/hikaricp/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/

