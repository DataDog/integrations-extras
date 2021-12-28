# CHANGELOG - Riak_Repl

## 1.0.1

 * [FIX] Add a condition to check that `rt_sink_connected_to` is a dict before collecting `sink_stats`

## 1.0.0

 * [FEATURE] Adds realtime_queue_stats metrics for consumers
 * [FEATURE] Adds realtime source/sink connection stats
 * [UPDATE] `fullsync_coordinator` metrics changed from `riak_repl.fullsync_coordinator.<cluster>.<key>` to `riak_repl.fullsync_coordinator.<key>` with a cluster tag
 * [FIX] Implement tests to ensure replication is enabled before expecting stats

## 0.0.2

 * [FEATURE] Adds basic fullsync_coordinator metrics

## 0.0.1

* [FEATURE] Adds riak-repl integration
