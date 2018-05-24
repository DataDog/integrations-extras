## Overview

RBLTracker provides easy-to-use, real-time blacklist monitoring, for your email, website, and social media.

Connect your [RBLTracker][1] account to Datadog to:

*   Push listing events from RBLTracker to your dashboard.
*   Push de-listing events from RBLTracker to your dashboard.

## Setup

Setting up RBLTracker using webhooks:

1.  In Datadog, copy your API key from the **Integrations -> APIs** section.
2.  In [RBLTracker][1], create a new Datadog contact type from the **Manage -> Contacts** section of the RBLTracker portal.
3.  Paste the Datadog **API Key**.
4.  (optional) adjust the contact schedule for this new contact.

RBLTracker will send listing and delisting alerts to your Datadog events dashboard. Click [here][2] for a full integration guide.

## Data Collected
### Metrics
The RBLTracker check does not include any metrics at this time.

### Events
Push your RBLTracker listing/de-listing events into your [Datadog Event Stream][3].

### Service Checks
The RBLTracker check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][4].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][5].


[1]: https://rbltracker.com/
[2]: https://rbltracker.com/docs/adding-a-datadog-contact-type/
[3]: https://docs.datadoghq.com/graphing/event_stream/
[4]: http://docs.datadoghq.com/help/
[5]: https://www.datadoghq.com/blog/
