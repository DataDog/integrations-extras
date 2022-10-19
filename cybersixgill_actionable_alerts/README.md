# Agent Check: cybersixgill_actionable_alerts

## Overview

This check monitors [cybersixgill_actionable_alerts][1].

## Setup

### Installation

To install the cybersixgill_actionable_alerts check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
 on any machine.

2. Run `ddev release build cybersixgill_actionable_alerts` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/cybersixgill_actionable_alerts/dist/<ARTIFACT_NAME>.whl`.

### Configuration

1. Provide Client Id and Client Secret in Configuration.yaml file
2. Provid the min collection interval in seconds.

### Validation

1. If your agent is able to generate events then credentials are working

## Data Collected

### Metrics

cybersixgill_actionable_alerts does not include any metrics.

### Service Checks

cybersixgill_actionable_alerts does not include any service checks.

### Events

cybersixgill_actionable_alerts does include events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: **LINK_TO_INTEGRATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/datadog_checks/cybersixgill_actionable_alerts/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/

