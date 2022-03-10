# Blue Matador Integration

## Overview

Blue Matador's Datadog integration allows you to send Blue Matador events to the event stream in Datadog.

![eventstream_from_blue_matador][1]

You can use it to enhance your existing dashboards or to correlate with metrics you're collecting in Datadog.

![dashboard][2]

For a full list of events and metrics that Blue Matador monitors and that you can import into Datadog, see their [monitors page][3].

## Setup

To get Blue Matador events into Datadog, use a [Datadog API key][4] to create a new notification method in Blue Matador.

**Note**: Already existing events are not imported into Datadog, but new events appear as they occur.

## Data Collected

### Metrics

The Blue Matador integration does not include any metrics.

### Events

All events are sent to the Datadog event stream.

### Service Checks

The Blue Matador integration does not include any service checks.

[1]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bluematador/images/eventstream.png
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/bluematador/images/dashboard.png
[3]: https://www.bluematador.com/monitored-events
[4]: https://app.datadoghq.com/organization-settings/api-keys
