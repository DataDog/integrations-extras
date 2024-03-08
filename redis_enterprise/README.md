# Agent Check: Redis Enterprise

## Overview

[Redis Enterprise][1] Software is a self-managed data platform that unlocks the full potential of Redis at enterprise scale. The speed you know and love, plus compliance, reliability, and unmatched resiliency for enterprise needs.

## Setup

### Installation

To install the Redis Enterprise check on your host:


1. Install the [developer toolkit]
(https://docs.datadoghq.com/developers/integrations/python/)
 on any machine.

2. Checkout the [repository][2] 

3. Run `ddev release build redis_enterprise` to build the package.

3. [Download the Datadog Agent][3].

4. Upload the build artifact to any host with an Agent and
 run `datadog-agent integration install -w
 path/to/redis_enterprise/dist/<ARTIFACT_NAME>.whl`. For information regarding starting and stopping the agent, see [start, stop, and restart the agent][5]. For other information about the agent, see [agent status and information][6].

### Configuration

5. Set the openmetrics_endpoint to point to your cluster. See the [example][4].

### Validation

6. Ensure you can ping the machine, particularly in a cloud environment. Run wget or curl to ensure that you can receive metrics.

## Data Collected

The current release gathers all metrics for databases, nodes, and shard.

### Metrics

See [metadata.csv][7] for a list of metrics provided by this integration.

### Service Checks

Redis Enterprise does not include any service checks.

### Events

Redis Enterprise does not include any events.

## Troubleshooting

Need help? Contact [Redis Field Engineering][9].

[1]: https://redis.com/redis-enterprise-software/overview/
[2]: https://github.com/redis-field-engineering/datadog-integrations-extras
[3]: https://app.datadoghq.com/account/settings/agent/latest
[4]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/datadog_checks/redis_enterprise/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/redis_enterprise/assets/service_checks.json
[9]: mailto:field.engineers@redis.com

