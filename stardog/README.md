# Stardog Integration

## Overview

Get metrics from Stardog service in real time to:

* Visualize and monitor Stardog states
* Be notified about Stardog failovers and events.

## Setup

### Configuration

Edit the `stardog.yaml` file to point to your server and set the admin username and password.

### Validation

[Run the Agent's `info` subcommand][1], you should see something like the following:

    Checks
    ======

        stardog
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The Stardog check is compatible with all major platforms.

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Stardog check does not include any events at this time.

### Service Checks
The Stardog check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog][4].

[1]: https://docs.datadoghq.com/agent/faq/agent-status-and-information/
[2]: https://github.com/DataDog/integrations-extras/blob/master/stardog/metadata.csv
[3]: http://docs.datadoghq.com/help/
[4]: https://www.datadoghq.com/blog/
