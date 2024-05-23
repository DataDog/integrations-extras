# Zfs Integration

## Overview

Get metrics and service status in real time from your zfs pools.

## Setup

The Zfs check is not included in the [Datadog Agent][1] package, so you need to install it.

### Installation

For Agent v7.21+ / v6.21+, follow the instructions below to install the Zfs check on your host. See [Use Community Integrations][3] to install with the Docker Agent or earlier versions of the Agent.

1. Run the following command to install the Agent integration:

   ```shell
   datadog-agent integration install -t datadog-zfs==<INTEGRATION_VERSION>
   ```

2. Configure your integration similar to core [integrations][4].

## Data Collected

### Metrics

See [metadata.csv][10] for a list of metrics provided by this check.

### Events

### Service Checks

[1]: https://app.datadoghq.com/account/settings/agent/latest
[2]: https://github.com/DataDog/integrations-extras/blob/master/zfs/metadata.csv
[3]: https://docs.datadoghq.com/agent/guide/use-community-integrations/
