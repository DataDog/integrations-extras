# CHANGELOG - Riak_Repl

## 1.0.0

 * [FEATURE] adds realtime_queue_stats metrics for consumers
 * [FEATURE] adds realtime source/sink connection stats
 * [UPDATE] fullsync_coordinator metrics changed from `riak_repl.fullsync_coordinator.<cluster>.<key>` to `riak_repl.fullsync_coordinator.<key>` with a cluster tag
 * [FIX] implement tests to ensure replication is enabled before expecting stats

## 0.0.2

 * [FEATURE] adds basic fullsync_coordinator metrics

## 0.0.1

* [FEATURE] adds riak-repl integration
