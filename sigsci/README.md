## Overview

Send Signal Sciences metrics and events to Datadog to monitor real-time attacks and abuse against your applications, APIs, and microservices, and to ensure Signal Sciences is functioning and inspecting traffic as expected.

![image-datadog-sigsci-dashboard][1]

![image-datadog-sigsci-security][2]

Get metrics and events from Signal Sciences in real-time to:

- See metrics from the WAF related to:

  - Total Requests
  - Top Types of Potential Attacks
  - Command Execution
  - SQL Injection
  - Cross Site Scripting
  - Path Scanning
  - Anomalous Traffic
  - Unknown Sources
  - Server 400/500s

- See IPs that Signal Sciences has blocked and/or flagged as malicious from any of the following activities:

  - OWASP Injection Attacks
  - Application DoS
  - Brute Force Attacks
  - Application Abuse & Misuse
  - Request Rate Limiting
  - Account Takeover
  - Bad Bots
  - Virtual Patching

- See alerts on Signal Sciences agent status

## Setup

To use the Signal Sciences-Datadog integration, you must be a customer of Signal Sciences. For more information about Signal Sciences, visit us at <https://www.signalsciences.com>.

### Configuration

#### Metrics collection

1. Install the [Signal Sciences agent][3].

2. Configure the Signal Sciences agent to use DogStatsD:

    Add the following line to each agent's agent.config file:

   ```shell
   statsd-type = "dogstatsd"
   ```

    When this is done the agent's StatsD client has tagging enabled and metrics such as `sigsci.agent.signal.<SIGNAL_TYPE>` are sent as `sigsci.agent.signal` and tagged with `signal_type:<SIGNAL_TYPE>`.

    _Example:_`sigsci.agent.signal.http404` => `sigsci.agent.signal` with tag `signal_type:http404`

    If using Kubernetes to run the Datadog Agent, make sure to enable DogStatsD non local traffic as described in the [Kubernetes DogStatsD documentation][4].

3. Configure the SigSci agent to send metrics to the Datadog Agent:

    Add the following line to each agent's `agent.config` file:

   ```shell
   statsd-address="<DATADOG_AGENT_HOSTNAME>:<DATADOG_AGENT_PORT>"
   ```

4. Click the button to install the integration.

5. In Datadog, verify that the "Signal Sciences - Overview" dashboard is created and starting to capture metrics.

#### Events collection

1. Within Datadog, [create an API key][5].

2. In your [Signal Sciences Dashboard][6] on the Site navigation bar, click Manage > Integrations and click Add next to the Datadog Event integration.

3. Enter the API Key in the _API Key_ field.

4. Click _Add_.

**Need more information?**

- [Here's a video][7] that covers the agent configuration and Datadog setup
- Read the full [Signal Sciences docs][8]

## Data Collected

### Metrics

See [metadata.csv][13] for a list of metrics provided by this integration.

### Events

All Signal Sciences events are sent to your [Datadog Event Stream][9]

### Service Checks

The Signal Sciences integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][10].

## Further Reading

Learn more about application security, DevOps, SecOps, and all the ops on [Signal Sciences blog][11].

To sign up for the Signal Sciences-Datadog Monitoring, a free service to see attacks against your applications, APIs, and microservices in real-time without a Signal Sciences subscription, visit our [registration page][12].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sigsci/images/datadog-sigsci-dashboard.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sigsci/images/datadog-sigsci-security.png
[3]: https://docs.signalsciences.net/install-guides/
[4]: https://docs.datadoghq.com/agent/kubernetes/dogstatsd/
[5]: https://app.datadoghq.com/account/settings#api
[6]: https://dashboard.signalsciences.net
[7]: https://player.vimeo.com/video/347360711
[8]: https://docs.signalsciences.net/integrations/datadog/
[9]: https://docs.datadoghq.com/events/
[10]: https://docs.datadoghq.com/help/
[11]: https://labs.signalsciences.com
[12]: https://info.signalsciences.com/datadog-security
[13]: https://github.com/DataDog/integrations-extras/blob/master/sigsci/metadata.csv
