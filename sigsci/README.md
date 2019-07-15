## Overview

Send Signal Sciences metrics and events to Datadog to monitor real-time attacks and abuse against your applications, APIs, and microservices, and to ensure Signal Sciences is functioning and inspecting traffic as expected.

![image-datadog-sigsci-dashboard][11]

![image-datadog-sigsci-security][1]

Get metrics and events from Signal Sciences in real-time to:

* See metrics from the WAF related to:
  - Total Requests
  - Top Types of Potential Attacks
  - Command Execution
  - SQL Injection
  - Cross Site Scripting
  - Path Scanning
  - Anomalous Traffic
  - Unknown Sources
  - Server 400/500s

* See IPs that Signal Sciences has blocked and/or flagged as malicious from any of the following activities:
  - OWASP Injection Attacks
  - Application DoS
  - Brute Force Attacks
  - Application Abuse & Misuse
  - Request Rate Limiting
  - Account Takeover
  - Bad Bots
  - Virtual Patching

* See alerts on Signal Sciences agent status

## Setup

To use the Signal Sciences-Datadog integration, you must be a customer of Signal Sciences. For more information about Signal Sciences, visit us at <https://www.signalsciences.com>.

### Configuration

**Metrics Integration**

- Install the [Signal Sciences agent][8]

- Configure the Signal Sciences agent to use DogstatsD:

    Add the following line to each agent's agent.config file:
    ```
    statsd-type = "dogstatsd"
    ```

    When this is done the agent's statsd client will have tagging enabled and metrics such as `sigsci.agent.signal.<signal_type>` will be sent as `sigsci.agent.signal` and tagged with `signal_type:<signal_type>`.

    *Example:* `sigsci.agent.signal.http404` => `sigsci.agent.signal` with tag `signal_type:http404`

- Configure the SigSci agent to send metrics to the Datadog agent:

  Add the following line to each agent's agent.config file:
  ```
  statsd-address=<datadog agent hostname:port>
  ```

- In Datadog, verify that the "Signal Sciences - Overview" dashboard is created and starting to capture metrics

**Events Integration**

- Within Datadog, [create an API key][2].

- In your [Signal Sciences Dashboard][3] on the Site navigation bar, click Manage > Integrations and click Add next to the Datadog Event integration.

- Enter the API Key in the API Key field.

- Click Add


**Need more information?**

- [Here's a video][9] that covers the agent configuration and Datadog setup
- Read the full [Signal Sciences docs][10]

## Data Collected
### Metrics

```
sigsci.agent.waf.total
sigsci.agent.waf.error
sigsci.agent.waf.allow
sigsci.agent.waf.block
sigsci.agent.waf.perf.decision_time
sigsci.agent.waf.perf.queue_time
sigsci.agent.rpc.connections.open
sigsci.agent.runtime.cpu_pct
sigsci.agent.runtime.mem.sys_bytes
sigsci.agent.runtime.uptime
sigsci.agent.signal
```

### Events

All Signal Sciences events are sent to your [Datadog Event Stream][4]

### Service Checks

The Signal Sciences integration does not include any service checks.

## Troubleshooting
Need help? Contact [Datadog support][5].

## Further Reading

Learn more about application security, DevOps, SecOps, and all the ops on [Signal Sciences blog][6].

To sign up for the Signal Sciences-Datadog Monitoring, a free service to see attacks against your applications, APIs, and microservices in real-time without a Signal Sciences subscription, visit our [registration page][7].

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/sigsci/images/datadog-sigsci-security.png
[2]: https://app.datadoghq.com/account/settings#api
[3]: https://dashboard.signalsciences.net
[4]: https://docs.datadoghq.com/graphing/event_stream
[5]: https://docs.datadoghq.com/help
[6]: https://labs.signalsciences.com
[7]: https://info.signalsciences.com/datadog-security
[8]: https://docs.signalsciences.net/install-guides/
[9]: https://player.vimeo.com/video/347360711
[10]: https://docs.signalsciences.net/integrations/datadog/
[11]: https://raw.githubusercontent.com/DataDog/integrations-extras/dhruv/sigsci_dashboard/sigsci/images/datadog-sigsci-dashboard.png
