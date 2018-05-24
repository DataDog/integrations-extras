# Storm Integration

## Overview

Get metrics from Storm service in real time to:

* Visualize and monitor storm cluster and topology metrics.
* Be notified about storm failovers and events.

## Setup

### Configuration

Edit the `storm.yaml` file to point to your server and port, set the masters to monitor.

### Validation

[Run the Agent's `status` subcommand][1] and look for `storm` under the Checks section.

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Storm check does not include any events at this time.

### Service Checks
The Storm check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].

[1]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[2]: https://github.com/DataDog/integrations-extras/blob/master/storm/metadata.csv
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
