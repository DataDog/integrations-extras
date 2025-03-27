
## Overview

WarpStream is an Apache Kafka® compatible data streaming platform built directly on top of object storage: no inter-AZ networking costs, no disks to manage, and infinitely scalable, all within your VPC.

The Datadog Agent collects many metrics from Warpstream, including those for:

- DAGs (Directed Acyclic Graphs): Number of DAG processes, DAG bag size, etc.
- Tasks: Task failures, successes, killed, etc.
- Pools: Open slots, used slots, etc.
- Executors: Open slots, queued tasks, running tasks, etc.

Metrics are sent directly from the [WarpStream Agent][2] to Datadog's [DogStatsD][3].

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://www.warpstream.com/
[2]: https://docs.warpstream.com/warpstream/byoc/deploy
[3]: https://docs.datadoghq.com/developers/dogstatsd/
[4]: https://docs.datadoghq.com/help/

