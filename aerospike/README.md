## Overview

Get metrics from [Aerospike](https://aerospike.com) in real time to:

* Visualize your database's performance.

* Obtain usage statistics


## Setup

*To capture Aerospike metrics, you need to install the Datadog Agent*

**Note:** This plugin does not support access control. As such, it is only compatible with Community Edition and Enterprise Edition that does not have TLS or Access Control enabled.

1. Configure the Agent to connect to Aerospike  
edit conf.d/aerospike.yaml

  ```
  init_config:
    mappings:
      ...
  instances:
    - host: localhost
  ```

2. Restart the Agent

## Data Collected
### Metrics
See [metadata.csv](https://github.com/DataDog/integrations-extras/blob/master/aerospike/metadata.csv) for a list of metrics provided by this integration.

### Events

The Aerospike integration does not include any events at this time.

### Service Checks

There is one service check: `aerospike.cluster_up`

## Troubleshooting
Need help? Contact [Datadog Support](http://docs.datadoghq.com/help/).

## Further Reading

Learn more about infrastructure monitoring and all our integrations on [our blog](https://www.datadoghq.com/blog/).
