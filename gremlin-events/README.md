## Overview

View, rerun, and halt Gremlin attacks directly from Datadog!

Pairing Gremlin with Datadog's [Events][1] is an effective way to add context failure testing context to your Datadog workflows. 

* Overlay attack events on top of your dashboards to pinpoint exactly how and when Gremlin is impacting your metrics.
* Show, Rerun, and Halt Gremlin attacks from your Datadog [Event Stream][2]

![snapshot][3]

## Setup

### Configuration

In order to activate this integration, you will need to pass your Datadog API key to Gremlin. This is done on the [Integrations Page][4], by clicking the **Add** button on the row for **Datadog**. You will be prompted for your **Datadog API key**. Once entered, the integration will be initialized!

* API key: <span class="hidden-api-key">${api_key}</span>

<li>Once you've configured your Datadog profile, you will need to assign the profile to a contact group located under Alerting>Contacts. The profile is assigned at the Push Notifications field within the contact group.</li> 
</ul>

## Data Collected

### Metrics

The Gremlin Events integration does not provide any metrics at this time.

### Events

The Gremlin Events integration sends events to your [Datadog Event Stream][4] when attacks are started and stopped on Gremlin.

### Service Checks

The Gremlin Events integration does not include any service checks at this time.

## Troubleshooting

Need help? Contact [Datadog Support][5].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][6].

[1]: https://docs.datadoghq.com/getting_started/#events
[2]: https://app.datadoghq.com/event/stream
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/gremlin-events/images/events-overlay.png
[4]: https://app.gremlin.com/settings/integrations
[5]: http://docs.datadoghq.com/help/
[6]: https://www.datadoghq.com/blog/
