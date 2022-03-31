# Apptrail

## Overview

[Apptrail][1] is the comprehensive SaaS audit logs platform. SaaS companies use Apptrail to add full-featured customer-facing audit logs to their products. Customers can view, query, analyze, and export audit logs from all of their SaaS vendors using Apptrail.

Apptrail's audit event streaming feature ([_trails_][11]) lets you deliver audit logs to dozens of popular destinations.

The Apptrail Datadog integration allows you to continously export your SaaS audit logs from Apptrail to Datadog in realtime. You can use Datadog to analyze, archive, monitor, and alert on your SaaS audit logs.

## Setup

As a prerequisite, you should be signed up by your SaaS vendor for Apptrail.

To get started, create a delivery trail in the Apptrail Portal and choose Datadog as the configured destination.

### Steps

View the [Creating a trail][4] documentation for general documentation on creating trails.

1. Navigate to the [**Trails**][5] page in the Apptrail Portal.
2. Click the **Create a new trail** button at the top right.
3. Enter a **Trail name** and configure any **rules**.
4. Click next and select **Datadog** from the list of destinations.
5. Provide your [Datadog **Region/Site**][6] to use. For example, `EU` for app.datadoghq.eu or `US1` for app.datadoghq.com.
6. Enter your [Datadog API key][7].
7. Click **Create trail** to create the trail.

### Validation

To view Apptrail audit logs in Datadog:

1. Navigate to **Logs** > **Live Tail**.
2. See Apptrail audit logs by setting `source:apptrail`.

For more details, read the [Apptrail Datadog delivery documentation][2].

## Data Collected

### Log collection

Any Apptrail [trail][11] with a Datadog destination will continously send all logs matched by the configured [trail rules][12] to Datadog. For the Apptrail audit log format, see [Event Format][10].

## Support

Need help? Contact [Datadog support][3] or reach out to [Apptrail support](mailto:support@apptrail.com).

## Further Reading

- [Apptrail customer documentation][13]
- [Apptrail Datadog Log delivery documentation][2]
- [Apptrail audit log format][10]
- [Apptrail event delivery trails][11]

[1]: https://apptrail.com
[2]: https://apptrail.com/docs/consumers/guide/event-delivery/integrations/datadog
[3]: https://docs.datadoghq.com/help/
[4]: https://apptrail.com/docs/consumers/guide/event-delivery/working-with-trails#creating-a-trail
[5]: https://portal.apptrail.com/trails
[6]: https://docs.datadoghq.com/getting_started/site/
[7]: https://app.datadoghq.com/organization-settings/api-keys
[10]: https://apptrail.com/docs/consumers/guide/event-format
[11]: https://apptrail.com/docs/consumers/guide/event-delivery/#trails
[12]: https://apptrail.com/docs/consumers/guide/event-delivery/working-with-trails#selecting-events-using-trail-rules
[13]: https://apptrail.com/docs/consumers/guide
