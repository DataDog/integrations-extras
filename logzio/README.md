## Overview

Integrate with Logz.io alerts to see events taking place in real-time

*   Import alerts into Datadog

![import_alert_from_logz](https://raw.githubusercontent.com/DataDog/integrations-extras/master/logzio/images/import_alert_from_logz.jpg)

*   Incorporate the events into a dashboard to identify correlations with metrics

![dashboard](https://raw.githubusercontent.com/DataDog/integrations-extras/master/logzio/images/dashboard.png)

## Setup
### Configuration

_To import alerts into Datadog, you need to take the following steps:_

1.  Use a Datadog API key to create a new alert endpoint in Logz.io.
2.  Create a new alert in Logz.io for a specific query.

For a more detailed setup description, see [the logz.io dedicated datadog documentation](http://logz.io/blog/log-correlation-datadog/).

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/logzio/metadata.csv) for a list of metrics provided by this integration.

### Events
Send your logz.io events into your [Datadog Even Stream](https://docs.datadoghq.com/graphing/event_stream/) 

### Service Checks
The Logz.io check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).