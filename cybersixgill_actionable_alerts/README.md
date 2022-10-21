# Agent Check: cybersixgill_actionable_alerts

## Overview
By integrating Cybersixgill actionable alerts, Datadog customers gain a premium,
automated threat intelligence solution based on the most comprehensive data sources from the deep, dark and surface web. 
It is customizable, enabling users to define key assets relevant to their brand, industry, and geolocation. Users can covertly 
monitor critical assets such as IP addresses, domains, vulnerabilities, and VIPs for activity on the underground and closed sources - and 
prioritize, as well as respond to threats directly from the Siemplify dashboard.
This check monitors [cybersixgill_actionable_alerts][1].

## Setup

### Installation

To install the cybersixgill_actionable_alerts check on your host:


1. Install the [developer toolkit][11] on any machine.

2. To build the package, run the command: `ddev release build cybersixgill_actionable_alerts` 

3. [Install the Datadog Agent][10] on your host.

4. Once the Agent is installed, upload the build artifact by running the command: `datadog-agent integration install -w
 path/to/cybersixgill_actionable_alerts/dist/datadog_cybersixgill_actionable_alerts-0.0.1-py3-none-any.whl`.

### Configuration

1. Provide Client Id and Client Secret in Configuration.yaml file which you will get it info@cybersixgill.com2.
2. Provide the min collection interval in seconds. `min_collection_interval: 3600`

### Validation

1. Verify that [events][12] are generated in your account 

## Data Collected

### Metrics

cybersixgill_actionable_alerts does not include any metrics.

### Service Checks

See assets/service_checks.json for a list of service checks provided by this integration..

### Events

cybersixgill_actionable_alerts does include events.

## Troubleshooting

Need help? Contact [Datadog support][3] or [Cybersixgill support][13].

[1]: https://www.cybersixgill.com/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/datadog_checks/cybersixgill_actionable_alerts/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
[10]: https://docs.datadoghq.com/getting_started/agent/
[11]: https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit
[12]: https://app.datadoghq.com/event/explorer
[13]: support@cybersixgill.com

