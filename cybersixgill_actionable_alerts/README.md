# Agent Check: cybersixgill_actionable_alerts

## Overview

Cybersixgill actionable alerts monitors critical assets across the deep, dark, and surface web 
such as IP addresses, domains, vulnerabilities, and VIPs. This integration provides an out-of-
the-box dashboard to prioritize and respond to threats.

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
1. Provide Client Id and Client Secret in Configuration.yaml file, once you contact 
info@cybersixgill.com you will receive a welcome email with access to Cybersixgill 
developer portal and then creating the client ID and secret there.
2. Provide the min collection interval in seconds. `min_collection_interval: 3600`

### Validation
1. Verify that [events][12] are generated in your account.

## Data Collected

### Service Checks
See assets/service_checks.json for a list of service checks provided by this integration.

### Events
This integration sends events into Datadog.

## Troubleshooting
Need help? Contact [Datadog support][3] or [Cybersixgill support][13].

[1]: https://www.cybersixgill.com/
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/help/
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

