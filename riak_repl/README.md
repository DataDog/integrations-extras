# Agent Check: Riak-Repl

## Overview

This check monitors Riak replication [riak-repl][1].

## Setup

### Installation

The riak-repl check is not included in the [Datadog Agent][2] package, so you will need to install it yourself.

### Configuration

1. Edit the `riak_repl.d/conf.yaml` file, in the `conf.d/` folder at the root of your Agent's configuration directory to start collecting your riak_repl performance data. See the [sample riak_repl.d/conf.yaml][3] for all available configuration options.

2. [Restart the Agent][4]

### Validation

[Run the Agent's `status` subcommand][5] and look for `riak_repl` under the Checks section.

## Data Collected

### Metrics

- riak_repl.server_bytes_sent: Total number of bytes the primary has sent
- riak_repl.server_bytes_recv: Total number of bytes the primary has received
- riak_repl.server_connects: Number of times the primary connects to the client sink
- riak_repl.server_fullsyncs: Number of fullsync operations since the server was started
- riak_repl.client_bytes_sent: Total number of bytes sent to all connected secondaries
- riak_repl.client_bytes_recv: Total number of bytes the client has received since the server has been started
- riak_repl.client_connects: Count of the number of sink connections made to this node
- riak_repl.client_redirect: Count of client connects to a non-leader node that are redirected to a leader node
- riak_repl.objects_dropped_no_clients: Total number of objects dropped from a full realtime queue
- riak_repl.objects_dropped_no_leader: Total number of objects dropped by a sink with no leader
- riak_repl.objects_sent: Total number of objects sent via realtime replication
- riak_repl.objects_forwarded: Total number of objects forwarded to the leader
- riak_repl.elections_elected: Total number of times a new leader has been elected
- riak_repl.elections_leader_changed: Total number of times a Riak node has surrendered leadership
- riak_repl.rt_source_errors: Total number of source errors detected on the source node
- riak_repl.rt_sink_errors: Total number of sink errors detected on the source node
- riak_repl.rt_dirty: Number of errors detected that can prevent objects from being replicated via realtime
- riak_repl.realtime_send_kbps: Total number of bytes realtime has sent
- riak_repl.realtime_recv_kbps: Total number of bytes realtime has received
- riak_repl.fullsync_send_kbps: Total number of bytes fullsync has sent
- riak_repl.fullsync_recv_kbps: Total number of bytes fullsync has received
- riak_repl.realtime_queue_stats.percent_bytes_used: Percentage of realtime queue used (max_bytes/bytes)
- riak_repl.realtime_queue_stats.bytes: Size in bytes of all objects currently in the realtime queue
- riak_repl.realtime_queue_stats.max_bytes: Size in bytes of the realtime queue
- riak_repl.realtime_queue_stats.overload_drops: Number of put transfers dropped due to an overload of the message queue of the Erlang process responsible for processing outgoing transfers
- riak_repl.fullsync_coordinator.<foo>.queued: Total number of partitions that are waiting for an available process
- riak_repl.fullsync_coordinator.<foo>.in_progress: Total number of partitions that are being synced
- riak_repl.fullsync_coordinator.<foo>.waiting_for_retry: Total number of partitions that are waiting for a retry
- riak_repl.fullsync_coordinator.<foo>.starting: Total number of partitions connecting to remote cluster
- riak_repl.fullsync_coordinator.<foo>.successful_exits: Total number of partitions successfully synced. When completed, this will be the same number as total number of partitions in the ring.
- riak_repl.fullsync_coordinator.<foo>.error_exits: Total number of partitions for which sync failed or was aborted
- riak_repl.fullsync_coordinator.<foo>.retry_exits: Total number of partitions successfully synced via retry
- riak_repl.fullsync_coordinator.<foo>.soft_retry_exits: 42
- riak_repl.fullsync_coordinator.<foo>.busy_nodes: 42
- riak_repl.fullsync_coordinator.<foo>.fullsyncs_completed: Total number of fullsyncs that have been completed to the specified sink cluster.
- riak_repl.fullsync_coordinator.<foo>.last_fullsync_duration: The duration (in seconds) of the last completed fullsync.

### Service Checks

riak_repl does not currently include any service checks.

### Events

riak_repl does not currently include any events.

## Troubleshooting

Need help? Contact [Datadog Support][6].

[1]: **LINK_TO_INTEGERATION_SITE**
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://github.com/DataDog/integrations-extras/blob/master/riak_repl/datadog_checks/riak_repl/data/conf.yaml.example
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[5]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[6]: https://docs.datadoghq.com/help/
