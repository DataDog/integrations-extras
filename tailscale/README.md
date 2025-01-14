# Agent Check: Tailscale

## Overview

[Tailscale][1] is a peer-to-peer VPN service that simplifies and secures network connectivity.

With this integration, you can:

1. Control your Tailscale data retention.
2. Build custom widgets and dashboards.
3. Cross-reference Tailscale events with the data from other services in your stack.

This integration streams two log types from Tailscale:

[Configuration Audit Logs][4]:

Configuration audit logs let you identify who did what and when in your tailnet. These logs record actions that modify a tailnet's configuration, including the type of action, the actor, the target resource, and the time.

[Network Flow logs][5]:

Network flow logs tell you which nodes connected to which other nodes and when on your Tailscale network. You can export network logs for long-term storage, security analysis, threat detection, or incident investigation.

After parsing your Tailscale logs, Datadog then populates the out-of-the-box Tailscale overview dashboard with insights into security-related events from your physical and virtual traffic.

## Setup

To enable log streaming:

1. Login to your Tailscale admin console
2. Navigate to the Logs tab
3. Select the **Start streaming...** button
4. From the menu, select Datadog and add a URL + token or [API key][6]
5. Select the **Start streaming** button

## Data Collected

### Metrics

Tailscale does not include any metrics.

### Service Checks

Tailscale does not include any service checks.

### Events

Tailscale does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

## Further Reading

Additional helpful documentation, links, and articles:

- [Monitor the state of your Tailscale private network with Datadog][7]

[1]: https://tailscale.com/
[2]: https://app.datadoghq.com/account/settings/agent/latest
[3]: https://docs.datadoghq.com/help/
[4]: https://tailscale.com/kb/1203/audit-logging/
[5]: https://tailscale.com/kb/1219/network-flow-logs/
[6]: https://docs.datadoghq.com/account_management/api-app-keys/
[7]: https://www.datadoghq.com/blog/monitor-tailscale-with-datadog/
