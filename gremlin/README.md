# Gremlin Integration

## Overview

View, rerun, and halt Gremlin attacks directly from Datadog!

Pairing Gremlin with Datadog's [Events][1] is an effective way to add failure-testing context to your Datadog workflows.

- Overlay attack events on top of your dashboards to pinpoint exactly how and when Gremlin is impacting your metrics.
- Show, Rerun, and Halt Gremlin attacks from your Datadog [Event Stream][2]

![snapshot][3]

## Setup

### Configuration

To activate this integration, you need to pass your Datadog API key to Gremlin. This is done on the [Integrations Page][4], by clicking the **Add** button on the row for **Datadog**. You are prompted for your **Datadog API key**. Once entered, the integration is initialized.

- API key: <span class="hidden-api-key">\${api_key}</span>

You should start seeing events from this integration in your [Event Stream][2].

## Data Collected

### Metrics

The Gremlin integration does not provide any metrics.

### Events

The Gremlin integration sends events to your [Datadog Event Stream][4] when attacks are started or stopped on Gremlin.

### Service Checks

The Gremlin integration does not include any service checks.

## Troubleshooting

Need help? Contact [Datadog support][5].

## Further Reading

Additional helpful documentation, links, and articles:

- [How Gremlin monitors its own Chaos Engineering service with Datadog][6]

[1]: https://docs.datadoghq.com/getting_started/#events
[2]: https://app.datadoghq.com/event/stream
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/gremlin/images/events-overlay.png
[4]: https://app.gremlin.com/settings/integrations
[5]: https://docs.datadoghq.com/help/
[6]: https://www.datadoghq.com/blog/gremlin-datadog/
