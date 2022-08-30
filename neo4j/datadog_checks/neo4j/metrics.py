METRIC_MAP = {
    # bolt metrics
    'bolt_accumulated_processing_time': 'bolt.accumulated_processing_time',
    'bolt_accumulated_queue_time': 'bolt.accumulated_queue_time',
    'bolt_connections_closed': 'bolt.connections_closed',
    'bolt_connections_idle': 'bolt.connections_idle',
    'bolt_connections_opened': 'bolt.connections_opened',
    'bolt_connections_running': 'bolt.connections_running',
    'bolt_messages_done': 'bolt.messages_done',
    'bolt_messages_failed': 'bolt.messages_failed',
    'bolt_messages_received': 'bolt.messages_received',
    'bolt_messages_started': 'bolt.messages_started',
    # causal clustering metrics
    'causal_clustering_catchup_tx_pull_requests_received': 'causal_clustering.catchup_tx_pull_requests_received',
    'causal_clustering_core_append_index': 'causal_clustering.core.append_index',
    'causal_clustering_core_commit_index': 'causal_clustering.core.commit_index',
    'causal_clustering_core_discovery_cluster_converged': 'causal_clustering.core.discovery.cluster.converged',
    'causal_clustering_core_discovery_cluster_members': 'causal_clustering.core.discovery.cluster.members',
    'causal_clustering_core_discovery_cluster_unreachable': 'causal_clustering.core.discovery.cluster.unreachable',
    # causal clustering replicated data metrics (4.3)
    'causal_clustering_core_discovery_replicated_data_member_data_invisible': (
        'causal_clustering.core.discovery.replicated_data.member_data.invisible'
    ),
    'causal_clustering_core_discovery_replicated_data_member_data_visible': (
        'causal_clustering.core.discovery.replicated_data.member_data.visible'
    ),
    'causal_clustering_core_discovery_replicated_data_raft_id_published_by_member_invisible': (
        'causal_clustering.core.discovery.replicated_data.raft_id_published_by_member.invisible'
    ),
    'causal_clustering_core_discovery_replicated_data_raft_id_published_by_member_visible': (
        'causal_clustering.core.discovery.replicated_data.raft_id_published_by_member.visible'
    ),
    'causal_clustering_core_discovery_replicated_data_per_db_leader_name_invisible': (
        'causal_clustering.core.discovery.replicated_data.per_db_leader_name.invisible'
    ),
    'causal_clustering_core_discovery_replicated_data_per_db_leader_name_visible': (
        'causal_clustering.core.discovery.replicated_data.per_db_leader_name.visible'
    ),
    'causal_clustering_core_discovery_replicated_data_member_db_state_invisible': (
        'causal_clustering.core.discovery.replicated_data.member_db_state.invisible'
    ),
    'causal_clustering_core_discovery_replicated_data_member_db_state_visible': (
        'causal_clustering.core.discovery.replicated_data.member_db_state.visible'
    ),
    'causal_clustering_core_discovery_replicated_data_raft_member_mapping_invisible': (
        'causal_clustering.core.discovery.replicated_data.raft_member_mapping.invisible'
    ),
    'causal_clustering_core_discovery_replicated_data_raft_member_mapping_visible': (
        'causal_clustering.core.discovery.replicated_data.raft_member_mapping.visible'
    ),
    # causal clustering replicated data metrics (3.6)
    'causal_clustering_core_discovery_replicated_data_cluster_id_per_db_name_invisible': (
        'causal_clustering.core.discovery.replicated_data.cluster_id_per_db_name.invisible'
    ),
    'causal_clustering_core_discovery_replicated_data_cluster_id_per_db_name_visible': (
        'causal_clustering.core.discovery.replicated_data.cluster_id_per_db_name.visible'
    ),
    # end causal clustering replicated data metrics
    'causal_clustering_core_in_flight_cache_element_count': 'causal_clustering.core.in_flight_cache_element_count',
    'causal_clustering_core_in_flight_cache_hits': 'causal_clustering.core.in_flight_cache.hits',
    'causal_clustering_core_in_flight_cache_max_bytes': 'causal_clustering.core.in_flight_cache.max_bytes',
    'causal_clustering_core_in_flight_cache_max_elements': 'causal_clustering.core.in_flight_cache.max_elements',
    'causal_clustering_core_in_flight_cache_misses': 'causal_clustering.core.in_flight_cache.misses',
    'causal_clustering_core_in_flight_cache_total_bytes': 'causal_clustering.core.in_flight_cache.total_bytes',
    'causal_clustering_core_is_leader': 'causal_clustering.core.is_leader',
    'causal_clustering_core_message_processing_delay': 'causal_clustering.core.message_processing_delay',
    'causal_clustering_core_message_processing_timer': 'causal_clustering.core.message_processing_timer',
    'causal_clustering_core_message_processing_timer_append_entries_request': (
        'causal_clustering.core.message_processing_timer.append_entries_request'
    ),
    'causal_clustering_core_message_processing_timer_append_entries_response': (
        'causal_clustering.core.message_processing_timer.append_entries_response'
    ),
    'causal_clustering_core_message_processing_timer_election_timeout': (
        'causal_clustering.core.message_processing_timer.election_timeout'
    ),
    'causal_clustering_core_message_processing_timer_heartbeat': (
        'causal_clustering.core.message_processing_timer.heartbeat'
    ),
    'causal_clustering_core_message_processing_timer_heartbeat_response': (
        'causal_clustering.core.message_processing_timer.heartbeat_response'
    ),
    'causal_clustering_core_message_processing_timer_heartbeat_timeout': (
        'causal_clustering.core.message_processing_timer.heartbeat_timeout'
    ),
    'causal_clustering_core_message_processing_timer_log_compaction_info': (
        'causal_clustering.core.message_processing_timer.log_compaction_info'
    ),
    'causal_clustering_core_message_processing_timer_new_batch_request': (
        'causal_clustering.core.message_processing_timer.new_batch_request'
    ),
    'causal_clustering_core_message_processing_timer_new_entry_request': (
        'causal_clustering.core.message_processing_timer.new_entry_request'
    ),
    'causal_clustering_core_message_processing_timer_pre_vote_request': (
        'causal_clustering.core.message_processing_timer.pre_vote_request'
    ),
    'causal_clustering_core_message_processing_timer_pre_vote_response': (
        'causal_clustering.core.message_processing_timer.pre_vote_response'
    ),
    'causal_clustering_core_message_processing_timer_prune_request': (
        'causal_clustering.core.message_processing_timer.prune_request'
    ),
    'causal_clustering_core_message_processing_timer_vote_request': (
        'causal_clustering.core.message_processing_timer.vote_request'
    ),
    'causal_clustering_core_message_processing_timer_vote_response': (
        'causal_clustering.core.message_processing_timer.vote_response'
    ),
    'causal_clustering.read_replica.pull_updates': (
        'causal_clustering.read_replica.pull_updates'
    ),
    'causal_clustering.read_replica.pull_update_highest_tx_id_requested': (
        'causal_clustering.read_replica.pull_update_highest_tx_id_requested'
    ),
    'causal_clustering.read_replica.pull_update_highest_tx_id_received': (
        'causal_clustering.read_replica.pull_update_highest_tx_id_received'
    ),
    'causal_clustering_core_replication_attempt': 'causal_clustering.core.replication_attempt',
    'causal_clustering_core_replication_fail': 'causal_clustering.core.replication_fail',
    'causal_clustering_core_replication_new': 'causal_clustering.core.replication_new',
    'causal_clustering_core_replication_success': 'causal_clustering.core.replication_success',
    'causal_clustering_core_term': 'causal_clustering.core.term',
    'causal_clustering_core_tx_retries': 'causal_clustering.core.tx_retries',
    # database checkpointing metrics
    'check_point_events': 'check_point.events',
    'check_point_total_time': 'check_point.total_time',
    'check_point_duration': 'check_point.duration',
    # cypher metrics
    'cypher_replan_events': 'cypher.replan_events',
    'cypher_replan_wait_time': 'cypher.replan_wait_time',
    # database data metrics
    'neo4j_count_node': 'node_count',
    'neo4j_count_relationship': 'relationship_count',
    'ids_in_use_node': 'ids_in_use.node',
    'ids_in_use_property': 'ids_in_use.property',
    'ids_in_use_relationship': 'ids_in_use.relationship',
    'ids_in_use_relationship_type': 'ids_in_use.relationship_type',
    'store_size_total': 'store.size.total',
    'store_size_database': 'store.size.database',
    # database transaction log metrics
    'log_appended_bytes': 'log.appended_bytes',
    'log_rotation_events': 'log.rotation_events',
    'log_rotation_total_time': 'log.rotation_total_time',
    'log_rotation_duration': 'log.rotation_duration',
    # page cache metrics
    'page_cache_eviction_exceptions': 'page_cache.eviction_exceptions',
    'page_cache_evictions': 'page_cache.evictions',
    'page_cache_flushes': 'page_cache.flushes',
    'page_cache_hits': 'page_cache.hits',
    'page_cache_page_faults': 'page_cache.page_faults',
    'page_cache_pins': 'page_cache.pins',
    'page_cache_unpins': 'page_cache.unpins',
    # server metrics
    'server_threads_jetty_all': 'server.threads.jetty.all',
    'server_threads_jetty_idle': 'server.threads.jetty.idle',
    # transaction metrics
    'transaction_active': 'transaction.active',
    'transaction_active_read': 'transaction.active_read',
    'transaction_active_write': 'transaction.active_write',
    'transaction_committed_read': 'transaction.committed_read',
    'transaction_committed': 'transaction.committed',
    'transaction_committed_write': 'transaction.committed_write',
    'transaction_last_closed_tx_id': 'transaction.last_closed_tx_id',
    'transaction_last_committed_tx_id': 'transaction.last_committed_tx_id',
    'transaction_peak_concurrent': 'transaction.peak_concurrent',
    'transaction_rollbacks_read': 'transaction.rollbacks_read',
    'transaction_rollbacks': 'transaction.rollbacks',
    'transaction_rollbacks_write': 'transaction.rollbacks_write',
    'transaction_started': 'transaction.started',
    'transaction_terminated_read': 'transaction.terminated_read',
    'transaction_terminated': 'transaction.terminated',
    'transaction_terminated_write': 'transaction.terminated_write',
    'transaction_tx_size_heap': 'transaction.tx_size_heap',
    'transaction_tx_size_native': 'transaction.tx_size_native',
    # JVM GC metrics
    'vm_gc_count_g1_old_generation': 'vm.gc.count.g1_old_generation',
    'vm_gc_count_g1_young_generation': 'vm.gc.count.g1_young_generation',
    'vm_gc_time_g1_old_generation': 'vm.gc.time.g1_old_generation',
    'vm_gc_time_g1_young_generation': 'vm.gc.time.g1_young_generation',
    # JVM memory buffers metrics
    'vm_memory_buffer_direct_capacity': 'vm.memory.buffer.direct_capacity',
    'vm_memory_buffer_direct_count': 'vm.memory.buffer.direct_count',
    'vm_memory_buffer_direct_used': 'vm.memory.buffer.direct_used',
    'vm_memory_buffer_mapped_capacity': 'vm.memory.buffer.mapped_capacity',
    'vm_memory_buffer_mapped_count': 'vm.memory.buffer.mapped_count',
    'vm_memory_buffer_mapped_used': 'vm.memory.buffer.mapped_used',
    # JVM memory pools metrics
    'vm_memory_pool_compressed_class_space': 'vm.memory.pool.compressed_class_space',
    'vm_memory_pool_g1_eden_space': 'vm.memory.pool.g1_eden_space',
    'vm_memory_pool_g1_old_gen': 'vm.memory.pool.g1_old_gen',
    'vm_memory_pool_g1_survivor_space': 'vm.memory.pool.g1_survivor_space',
    'vm_memory_pool_metaspace': 'vm.memory.pool.metaspace',
    # dbms memory pools metrics
    'pool_page_cache_total_size': 'pool.page_cache.total_size',
    'pool_page_cache_free': 'pool.page_cache.free',
    'pool_page_cache_total_used': 'pool.page_cache.total_used',
    'pool_page_cache_used_native': 'pool.page_cache.used_native',
    'pool_page_cache_used_heap': 'pool.page_cache.used_heap',
    #
    'pool_other_total_size': 'pool.other.total_size',
    'pool_other_free': 'pool.other.free',
    'pool_other_total_used': 'pool.other.total_used',
    'pool_other_used_native': 'pool.other.used_native',
    'pool_other_used_heap': 'pool.other.used_heap',
    #
    'pool_recent_query_buffer_total_size': 'pool.recent_query_buffer.total_size',
    'pool_recent_query_buffer_free': 'pool.recent_query_buffer.free',
    'pool_recent_query_buffer_total_used': 'pool.recent_query_buffer.total_used',
    'pool_recent_query_buffer_used_native': 'pool.recent_query_buffer.used_native',
    'pool_recent_query_buffer_used_heap': 'pool.recent_query_buffer.used_heap',
    #
    'pool_transaction_total_size': 'pool.transaction.total_size',
    'pool_transaction_free': 'pool.transaction.free',
    'pool_transaction_total_used': 'pool.transaction.total_used',
    'pool_transaction_used_native': 'pool.transaction.used_native',
    'pool_transaction_used_heap': 'pool.transaction.used_heap',
    #
    'pool_bolt_total_size': 'pool.bolt.total_size',
    'pool_bolt_free': 'pool.bolt.free',
    'pool_bolt_total_used': 'pool.bolt.total_used',
    'pool_bolt_used_native': 'pool.bolt.used_native',
    'pool_bolt_used_heap': 'pool.bolt.used_heap',
    # JVM threads metrics
    'vm_thread_count': 'vm.thread.count',
    'vm_thread_total': 'vm.thread.total',
}
