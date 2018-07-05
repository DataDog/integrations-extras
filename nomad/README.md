## Overview

Gather metrics from your Nomad clusters to:

* Visualize and monitor cluster performance
* Alert on cluster health and availability

## Setup

### Installation

Nomad emits metrics to Datadog via DogStatsD. To enable the Nomad integration, [install the Datadog Agent][1] on each client and server host.  

### Configuration

Once the Datadog Agent is installed, add a Telemetry stanza to the Nomad configuration for your clients and servers:

```
telemetry {
  publish_allocation_metrics = true
  publish_node_metrics       = true
  datadog_address = "localhost:8125"
  disable_hostname = true
}
```

Next, reload or restart the Nomad agent on each host. You should now begin to see Nomad metrics flowing to your Datadog account.  

## Data Collected
### Metrics
See [metadata.csv][2] for a list of metrics provided by this integration.

### Events
The Nomad check does not include any events at this time.

### Service Checks
The Nomad check does not include any service checks at this time.

## Troubleshooting
Need help? Contact [Datadog Support][3].

[1]: https://app.datadoghq.com/account/settings#agent
[2]: https://github.com/DataDog/integrations-extras/blob/master/nomad/metadata.csv
[3]: http://docs.datadoghq.com/help/
