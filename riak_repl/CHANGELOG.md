# CHANGELOG - Riak_Repl

## 1.0.1

***Fixed***: 

* Add a condition to check that `rt_sink_connected_to` is a dict before collecting `sink_stats`

## 1.0.0

***Added***: 

* Adds realtime_queue_stats metrics for consumers
* Adds realtime source/sink connection stats
* `fullsync_coordinator` metrics changed from `riak_repl.fullsync_coordinator.<cluster>.<key>` to `riak_repl.fullsync_coordinator.<key>` with a cluster tag

***Fixed***: 

* Implement tests to ensure replication is enabled before expecting stats

## 0.0.2

***Added***: 

* Adds basic fullsync_coordinator metrics

## 0.0.1

***Added***: 

* Adds riak-repl integration
