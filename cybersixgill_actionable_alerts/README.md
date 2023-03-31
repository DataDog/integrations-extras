# Agent Check: cybersixgill_actionable_alerts

## Overview
The Cybersixgill actionable alerts check monitors critical assets across the deep, dark, and surface web such as IP addresses, domains, vulnerabilities, and VIPs. Receive alerts with context including severity, threat type, description, post snippet, recommendations, and assessments. This integration provides an out-of-the-box dashboard to prioritize and respond to threats.

## Setup


### Installation

To install the Cybersixgill actionable alerts check on your host:
1. Install the [developer tool][2] on any machine.
2. To build the package, run the command: `ddev release build cybersixgill_actionable_alerts`.
3. [Install the Datadog Agent][1] on your host.
4. Once the Agent is installed, run the following command to install the integration:
```
datadog-agent integration install -t datadog-Cybersixgill Actionable Alerts==1.0.0
```

### Configuration
5. Reach out to [Cybersixgill Support][4] and request access to the Cybersixgill Developer Platform.
6. Receive the welcome email with access to the Cybersixgill developer platform.
7. Within the Cybersixgill developer platform, create the Client ID and Client secret.
8. Copy the Client ID and Client secret and paste them into the Configuration.yaml file.
9. Provide the minimum collection interval in seconds. For example, `min_collection_interval: 3600`

### Validation
Verify that Cybersixgill events are generated in the [Datadog Events Explorer][3].

## Data Collected

### Service Checks
See [service_checks.json][5] for a list of service checks provided by this integration.

### Events
This integration sends API-type events to Datadog.

## Troubleshooting
Need help? Contact [Cybersixgill support][4].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://docs.datadoghq.com/developers/integrations/new_check_howto/?tab=configurationtemplate#configure-the-developer-tool
[3]: https://app.datadoghq.com/event/explorer
[4]: mailto:support@cybersixgill.com
[5]: https://github.com/DataDog/integrations-extras/blob/master/cybersixgill_actionable_alerts/assets/service_checks.json

