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
    # causal clustering metrics (5.x)
    'cluster_catchup_tx_pull_requests_received': 'cluster.catchup_tx_pull_requests_received',
    # cluster core
    'cluster_core_append_index': 'cluster.core.append_index',
    'cluster_core_applied_index': 'cluster.core.applied_index',
    'cluster_core_commit_index': 'cluster.core.commit_index',
    'cluster_core_in_flight_cache_element_count': 'cluster.core_in_flight_cache_element_count',
    'cluster_core_in_flight_cache_hits': 'cluster.core_in_flight_cache_hits',
    'cluster_core_in_flight_cache_max_bytes': 'cluster.core_in_flight_cache_max_bytes',
    'cluster_core_in_flight_cache_max_elements': 'cluster.core_in_flight_cache_max_elements',
    'cluster_core_in_flight_cache_misses': 'cluster_core_in_flight_cache_misses',
    'cluster_core_in_flight_cache_total_bytes': 'cluster.core_in_flight_cache_total_bytes',
    'cluster_core_is_leader': 'cluster.core_is_leader',
    'cluster_core_last_leader_message': 'cluster.core_last_leader_message',
    'cluster_core_message_processing_delay': ('cluster.core_message_processing_delay'),
    'cluster_core_message_processing_timer_append_entries_request': (
        'cluster.core.message_processing_timer.append_entries_request'
    ),
    'cluster_core_message_processing_timer_append_entries_response': (
        'cluster.core_message_processing_timer_append_entries_response'
    ),
    'cluster_core_message_processing_timer': ('cluster.core_message_processing_timer'),
    'cluster_core_message_processing_timer_election_timeout': (
        'cluster.core_message_processing_timer_election_timeout'
    ),
    'cluster_core_message_processing_timer_heartbeat_response': (
        'cluster.core_message_processing_timer_heartbeat_response'
    ),
    'cluster_core_message_processing_timer_heartbeat_timeout': (
        'cluster.core_message_processing_timer_heartbeat_timeout'
    ),
    'cluster_core_message_processing_timer_heartbeat': ('cluster.core_message_processing_timer_heartbeat'),
    'cluster_core_message_processing_timer_leadership_transfer_proposal': (
        'cluster.core_message_processing_timer_leadership_transfer_proposal'
    ),
    'cluster_core_message_processing_timer_leadership_transfer_rejection': (
        'cluster.core_message_processing_timer_leadership_transfer_rejection'
    ),
    'cluster_core_message_processing_timer_leadership_transfer_request': (
        'cluster.core_message_processing_timer_leadership_transfer_request'
    ),
    'cluster_core_message_processing_timer_log_compaction_info': (
        'cluster.core_message_processing_timer_log_compaction_info'
    ),
    'cluster_core_message_processing_timer_new_batch_request': (
        'cluster.core_message_processing_timer_new_batch_request'
    ),
    'cluster_core_message_processing_timer_new_entry_request': (
        'cluster.core_message_processing_timer_new_entry_request'
    ),
    'cluster_core_message_processing_timer_pre_vote_request': (
        'cluster.core_message_processing_timer_pre_vote_request'
    ),
    'cluster_core_message_processing_timer_pre_vote_response': (
        'cluster.core_message_processing_timer_pre_vote_response'
    ),
    'cluster_core_message_processing_timer_prune_request': ('cluster.core_message_processing_timer_prune_request'),
    'cluster_core_message_processing_timer_status_response': ('cluster.core_message_processing_timer_status_response'),
    'cluster_core_message_processing_timer_vote_request': ('cluster.core_message_processing_timer_vote_request'),
    'cluster_core_message_processing_timer_vote_response': ('cluster.core_message_processing_timer_vote_response'),
    # raft
    'cluster_raft_append_index': 'cluster.raft_append_index',
    'cluster_raft_applied_index': 'cluster.raft_applied_index',
    'cluster_raft_commit_index': 'cluster.raft_commit_index',
    'cluster_raft_in_flight_cache_element_count': 'cluster.raft_in_flight_cache_element_count',
    'cluster_raft_in_flight_cache_hits': 'cluster.raft_in_flight_cache_hits',
    'cluster_raft_in_flight_cache_max_bytes': 'cluster.raft_in_flight_cache_max_bytes',
    'cluster_raft_in_flight_cache_max_elements': 'cluster.raft_in_flight_cache_max_elements',
    'cluster_raft_in_flight_cache_misses': 'cluster.raft_in_flight_cache_misses',
    'cluster_raft_in_flight_cache_total_bytes': 'cluster.raft_in_flight_cache_total_bytes',
    'cluster_raft_is_leader': 'cluster.raft_is_leader',
    'cluster_raft_last_leader_message': 'cluster.raft_last_leader_message',
    'cluster_raft_message_processing_delay': ('cluster.raft_message_processing_delay'),
    'cluster_raft_message_processing_timer_append_entries_request': (
        'cluster.raft_message_processing_timer_append_entries_request'
    ),
    'cluster_raft_message_processing_timer_append_entries_response': (
        'cluster.raft_message_processing_timer_append_entries_response'
    ),
    'cluster_raft_message_processing_timer': ('cluster.raft_message_processing_timer'),
    'cluster_raft_message_processing_timer_election_timeout': (
        'cluster.raft_message_processing_timer_election_timeout'
    ),
    'cluster_raft_message_processing_timer_heartbeat_response': (
        'cluster.raft_message_processing_timer_heartbeat_response'
    ),
    'cluster_raft_message_processing_timer_heartbeat_timeout': (
        'cluster.raft_message_processing_timer_heartbeat_timeout'
    ),
    'cluster_raft_message_processing_timer_heartbeat': ('cluster.raft_message_processing_timer_heartbeat'),
    'cluster_raft_message_processing_timer_leadership_transfer_proposal': (
        'cluster.raft_message_processing_timer_leadership_transfer_proposal'
    ),
    'cluster_raft_message_processing_timer_leadership_transfer_rejection': (
        'cluster.raft_message_processing_timer_leadership_transfer_rejection'
    ),
    'cluster_raft_message_processing_timer_leadership_transfer_request': (
        'cluster.raft_message_processing_timer_leadership_transfer_request'
    ),
    'cluster_raft_message_processing_timer_log_compaction_info': (
        'cluster.raft_message_processing_timer_log_compaction_info'
    ),
    'cluster_raft_message_processing_timer_new_batch_request': (
        'cluster.raft_message_processing_timer_new_batch_request'
    ),
    'cluster_raft_message_processing_timer_new_entry_request': (
        'cluster.raft_message_processing_timer_new_entry_request'
    ),
    'cluster_raft_message_processing_timer_pre_vote_request': (
        'cluster.raft_message_processing_timer_pre_vote_request'
    ),
    'cluster_raft_message_processing_timer_pre_vote_response': (
        'cluster.raft_message_processing_timer_pre_vote_response'
    ),
    'cluster_raft_message_processing_timer_prune_request': ('cluster.raft_message_processing_timer_prune_request'),
    'cluster_raft_message_processing_timer_status_response': ('cluster.raft_message_processing_timer_status_response'),
    'cluster_raft_message_processing_timer_vote_request': ('cluster.raft_message_processing_timer_vote_request'),
    'cluster_raft_message_processing_timer_vote_response': ('cluster.raft_message_processing_timer_vote_response'),
    'cluster_raft_raft_log_entry_prefetch_buffer_async_put': ('cluster.raft_raft_log_entry_prefetch_buffer_async_put'),
    'cluster_raft_raft_log_entry_prefetch_buffer_bytes': ('cluster.raft_raft_log_entry_prefetch_buffer_bytes'),
    'cluster_raft_raft_log_entry_prefetch_buffer_lag': ('cluster.raft_raft_log_entry_prefetch_buffer_lag'),
    'cluster_raft_raft_log_entry_prefetch_buffer_size': ('cluster.raft_raft_log_entry_prefetch_buffer_size'),
    'cluster_raft_raft_log_entry_prefetch_buffer_sync_put': ('cluster.raft_raft_log_entry_prefetch_buffer_sync_put'),
    'cluster_raft_replication_attempt': 'cluster.raft_replication_attempt',
    'cluster_raft_replication_fail': 'cluster.raft_replication_fail',
    'cluster_raft_replication_maybe': 'cluster.raft_replication_maybe',
    'cluster_raft_replication_new': 'cluster.raft_replication_new',
    'cluster_raft_replication_success': 'cluster.raft_replication_success',
    'cluster_raft_term': 'cluster.raft_term',
    'cluster_raft_tx_retries': 'cluster.raft_tx_retries',
    # replication
    'cluster_core_replication_attempt': 'cluster.core_replication_attempt',
    'cluster_core_replication_fail': 'cluster.core_replication_fail',
    'cluster_core_replication_maybe': 'cluster.core_replication_maybe',
    'cluster_core_replication_new': 'cluster.core_replication_new',
    'cluster_core_replication_success': 'cluster.core_replication_success',
    'cluster_core_term': 'cluster.core_term',
    'cluster_core_tx_retries': 'cluster.core_tx_retries',
    # cluster discovery
    'cluster_discovery_cluster_converged': 'cluster.discovery_cluster_converged',
    'cluster_discovery_cluster_members': 'cluster.discovery_cluster_members',
    'cluster_discovery_cluster_unreachable': 'cluster.discovery_cluster_unreachable',
    'cluster_discovery_restart_failed__count': 'cluster.discovery.restart.failed_count',
    'cluster_discovery_restart_success__count': 'cluster.discovery.restart.success_count',
    'cluster_discovery_replicated_data_server_data_invisible': (
        'cluster.discovery_replicated_data_server_data_invisible'
    ),
    'cluster_discovery_replicated_data_server_data_visible': ('cluster.discovery_replicated_data_server_data_visible'),
    'cluster_discovery_replicated_data_leader_data_invisible': (
        'cluster.discovery_replicated_data_leader_data_invisible'
    ),
    'cluster_discovery_replicated_data_leader_data_visible': ('cluster.discovery_replicated_data_leader_data_visible'),
    'cluster_discovery_replicated_data_bootstrap_data_invisible': (
        'cluster.discovery_replicated_data_bootstrap_data_invisible'
    ),
    'cluster_discovery_replicated_data_bootstrap_data_visible': (
        'cluster.discovery_replicated_data_bootstrap_data_visible'
    ),
    'cluster_discovery_replicated_data_component_versions_invisible': (
        'cluster.discovery_replicated_data_component_versions_invisible'
    ),
    'cluster_discovery_replicated_data_component_versions_visible': (
        'cluster.discovery_replicated_data_component_versions)visible'
    ),
    'cluster_discovery_replicated_data_database_data_invisible': (
        'cluster.discovery_replicated_data_database_data_invisible'
    ),
    'cluster_discovery_replicated_data_database_data_visible': (
        'cluster.discovery_replicated_data_database_data_visible'
    ),
    # Store Copy
    'cluster_store_copy_pull_updates': ('cluster.store_copy.pull_updates'),
    'cluster_store_copy_pull_update_highest_tx_id_requested': (
        'cluster.store_copy.pull_update_highest_tx_id_requested'
    ),
    'cluster_store_copy_pull_update_highest_tx_id_received': ('cluster.store_copy.pull_update_highest_tx_id_received'),
    # end causal clustering replicated data metrics
    'cluster.read_replica.pull_updates': 'cluster.read_replica.pull_updates',
    'cluster.read_replica.pull_update_highest_tx_id_requested': (
        'cluster.read_replica.pull_update_highest_tx_id_requested'
    ),
    'cluster.read_replica.pull_update_highest_tx_id_received': (
        'cluster.read_replica.pull_update_highest_tx_id_received'
    ),
    # causal clustering metrics (4.x)
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
    'causal_clustering.read_replica.pull_updates': 'causal_clustering.read_replica.pull_updates',
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
    'check_point_pages_flushed': 'check_point.pages_flushed',
    'check_point_io_performed': 'check_point.io_performed',
    'check_point_io_limit': 'check_point.io_limit',
    # cypher metrics
    'cypher_replan_events': 'cypher.replan_events',
    'cypher_replan_wait_time': 'cypher.replan_wait_time',
    'cypher_cache_ast_entries': 'cypher.cache.ast.entries',
    'cypher_cache_executable_query_cache_flushes': 'cypher.cache.executable_query.cache_flushes',
    'cypher_cache_executable_query_compiled': 'cypher.cache.executable_query.compiled',
    'cypher_cache_executable_query_discards': 'cypher.cache.executable_query.discards',
    'cypher_cache_executable_query_entries': 'cypher.cache.executable_query.entries',
    'cypher_cache_executable_query_hits': 'cypher.cache.executable_query.hits',
    'cypher_cache_executable_query_misses': 'cypher.cache.executable_query.misses',
    'cypher_cache_executable_query_stale_entries': 'cypher.cache.executable_query.stale_entries',
    'cypher_cache_execution_plan_cache_flushes': 'cypher.cache.execution_plan.cache_flushes',
    'cypher_cache_execution_plan_compiled': 'cypher.cache.execution_plan.compiled',
    'cypher_cache_execution_plan_discards': 'cypher.cache.execution_plan.discards',
    'cypher_cache_execution_plan_entries': 'cypher.cache.execution_plan.entries',
    'cypher_cache_execution_plan_hits': 'cypher.cache.execution_plan.hits',
    'cypher_cache_execution_plan_misses': 'cypher.cache.execution_plan.misses',
    'cypher_cache_execution_plan_stale_entries': 'cypher.cache.execution_plan.stale_entries',
    'cypher_cache_logical_plan_cache_flushes': 'cypher.cache.logical_plan.cache_flushes',
    'cypher_cache_logical_plan_compiled': 'cypher.cache.logical_plan.compiled',
    'cypher_cache_logical_plan_discards': 'cypher.cache.logical_plan.discards',
    'cypher_cache_logical_plan_entries': 'cypher.cache.logical_plan.entries',
    'cypher_cache_logical_plan_hits': 'cypher.cache.logical_plan.hits',
    'cypher_cache_logical_plan_misses': 'cypher.cache.logical_plan.misses',
    'cypher_cache_logical_plan_stale_entries': 'cypher.cache.logical_plan.stale_entries',
    'cypher_cache_pre_parser_entries': 'cypher.cache.pre_parser.entries',
    # database data count metrics
    'neo4j_count_node': 'node_count',
    'neo4j_count_relationship': 'relationship_count',
    # database data metrics
    'ids_in_use_node': 'ids_in_use.node',
    'ids_in_use_property': 'ids_in_use.property',
    'ids_in_use_relationship': 'ids_in_use.relationship',
    'ids_in_use_relationship_type': 'ids_in_use.relationship_type',
    # database operation count metrics
    'db_operation_count_create': 'db.operation.count.create',
    'db_operation_count_start': 'db.operation.count.start',
    'db_operation_count_stop': 'db.operation.count.stop',
    'db_operation_count_drop': 'db.operation.count.drop',
    'db_operation_count_failed': 'db.operation.count.failed',
    'db_operation_count_recovered': 'db.operation.count.recovered',
    # database store size metrics
    'neo4j_store_size_total': 'neo4j.store.size_total',
    'neo4j_store_size_database': 'neo4j.store.size_database',
    # database store size metrics (4.x)
    'store_size_total': 'store.size.total',
    'store_size_database': 'store.size.database',
    # database transaction log metrics
    'log_appended_bytes': 'log.appended_bytes',
    'log_append_batch_size': 'log.append_batch_size',
    'log_flushes': 'log.flushes',
    'log_rotation_events': 'log.rotation_events',
    'log_rotation_total_time': 'log.rotation_total_time',
    'log_rotation_duration': 'log.rotation_duration',
    # database transaction metrics
    'transaction_active': 'transaction.active',
    'transaction_active_read': 'transaction.active_read',
    'transaction_active_write': 'transaction.active_write',
    'transaction_committed': 'transaction.committed',
    'transaction_committed_read': 'transaction.committed_read',
    'transaction_committed_write': 'transaction.committed_write',
    'transaction_last_closed_tx_id': 'transaction.last_closed_tx_id',
    'transaction_last_committed_tx_id': 'transaction.last_committed_tx_id',
    'transaction_peak_concurrent': 'transaction.peak_concurrent',
    'transaction_rollbacks': 'transaction.rollbacks',
    'transaction_rollbacks_read': 'transaction.rollbacks_read',
    'transaction_rollbacks_write': 'transaction.rollbacks_write',
    'transaction_started': 'transaction.started',
    'transaction_terminated': 'transaction.terminated',
    'transaction_terminated_read': 'transaction.terminated_read',
    'transaction_terminated_write': 'transaction.terminated_write',
    'transaction_tx_size_heap': 'transaction.tx_size_heap',
    'transaction_tx_size_native': 'transaction.tx_size_native',
    # page cache metrics
    'page_cache_bytes_written': 'page_cache.bytes_written',
    'page_cache_bytes_read': 'page_cache.bytes_read',
    'page_cache_cancelled_faults': 'page_cache.cancelled_faults',
    'page_cache_eviction_exceptions': 'page_cache.eviction_exceptions',
    'page_cache_evictions': 'page_cache.evictions',
    'page_cache_evictions_cooperative': 'page_cache.evictions_cooperative',
    'page_cache_flushes': 'page_cache.flushes',
    'page_cache_hits': 'page_cache.hits',
    'page_cache_hit_ratio': 'page_cache.hit_ratio',
    'page_cache_merges': 'page_cache.merges',
    'page_cache_page_faults': 'page_cache.page_faults',
    'page_cache_page_fault_failures': 'page_cache.page_fault_failures',
    'page_cache_pages_copied': 'page_cache.pages_copied',
    'page_cache_pins': 'page_cache.pins',
    'page_cache_throttled_times': 'page_cache.throttled_times',
    'page_cache_throttled_millis': 'page_cache.throttled_millis',
    'page_cache_unpins': 'page_cache.unpins',
    'page_cache_usage_ratio': 'page_cache.usage_ratio',
    # query metrics
    'db_query_execution_success': 'db_query.execution_success',
    'db_query_execution_failure': 'db_query.execution_failure',
    'db_query_execution_latency_millis': 'db_query.execution_latency_millis',
    # server metrics
    'server_threads_jetty_all': 'server.threads.jetty.all',
    'server_threads_jetty_idle': 'server.threads.jetty.idle',
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
    # JVM Other Metrics
    'vm_pause_time': 'vm.pause_time',
    'vm_heap_used': 'vm.heap.used',
    'vm_heap_max': 'vm.heap.max',
    'vm_heap_committed': 'vm.heap.committed',
    'vm_file_descriptors_count': 'vm.file.descriptors.count',
    'vm_file_descriptors_maximum': 'vm.file.descriptors.maximum',
    # dbms memory pools metrics
    'pool_cluster_free': 'pool.cluster_free',
    'pool_cluster_total_size': 'pool.cluster.total_size',
    'pool_cluster_total_used': 'pool.cluster.total_used',
    'pool_cluster_used_heap': 'pool.cluster.used_heap',
    'pool_cluster_used_native': 'pool.cluster.used_native',
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
    # pool http
    'pool_http_free': 'pool.http.free',
    'pool_http_total_size': 'pool.http.total_size',
    'pool_http_total_used': 'pool.http.total_used',
    'pool_http_used_heap': 'pool.http.used_heap',
    'pool_http_used_native': 'pool.http.used_native',
    'pool_http_transaction_total_size': 'pool.http_transaction.total_size',
    'pool_http_transaction_free': 'pool.http_transaction.free',
    'pool_http_transaction_total_used': 'pool.http_transaction.total_used',
    'pool_http_transaction_used_native': 'pool.http_transaction.used_native',
    'pool_http_transaction_used_heap': 'pool.http_transaction.used_heap',
    # JVM threads metrics
    'vm_thread_count': 'vm.thread.count',
    'vm_thread_total': 'vm.thread.total',
    'vm_threads': 'vm.threads',
    # Routed queries metrics
    'routing_query_count_local': 'routing.query.count.local',
    'routing_query_count_remote_internal': 'routing.query.count.remote_internal',
    'routing_query_count_remote_external': 'routing.query.count.remote_external',
}
