# Nomad

## Overview

Gather health metrics from your Nomad clusters.

## Setup

### Configuration

Nomad emits metrics to Datadog via DogStatsD. To enable the Nomad integration, you will need 
to install the Datadog Agent on each client and server host.  Once installed, add a Telemetry 
stanza to the Nomad configuration for your clients and servers:

```
telemetry {
  publish_allocation_metrics = true
  publish_node_metrics       = true
  datadog_address = "localhost:8125"
  disable_hostname = true
```

Next, reload or restart the Nomad agent on each host. You should now begin to see Nomad metrics flowing to
your Datadog account.  
