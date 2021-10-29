from datadog_checks.base import ConfigurationError
from datadog_checks.base.checks.prometheus.prometheus_base import PrometheusCheck

GLOBAL_DB_NAME = 'global'
NAMESPACE = 'neo4j'


class Config:
    def __init__(self, host, port, neo4j_version, https, neo4j_dbs, exclude_labels, instance_tags):
        self.host = host
        self.port = port
        self.neo4j_version = neo4j_version
        self.https = https
        self.neo4j_dbs = neo4j_dbs
        self.exclude_labels = exclude_labels
        self.instance_tags = instance_tags

    def __eq__(self, other):
        return (
            self.host == other.host
            and self.port == other.port
            and self.neo4j_version == self.neo4j_version
            and self.https == self.https
            and self.neo4j_dbs == other.neo4j_dbs
            and self.exclude_labels == other.exclude_labels
            and self.instance_tags == other.instance_tags
        )


class Neo4jCheck(PrometheusCheck):
    def check(self, instance):
        self._set_whitelisted_metrics()
        config = self._get_config(instance=instance)
        self.exclude_labels = config.exclude_labels
        if config.https.lower() == 'false':
            endpoint = 'http://{}:{}/metrics'.format(config.host, config.port)
        else:
            endpoint = 'https://{}:{}/metrics'.format(config.host, config.port)
        self._check_metrics(self.scrape_metrics(endpoint=endpoint), config)

    def _check_metrics(self, metrics, config):
        # Determine if metrics.namespaces.enabled is set in the target Neo4j instance
        # Finding this dynamically lets users roll out this feature without interrupting their metrics,
        # as well as monitoring database fleets with mixed values for this setting.
        is_namespaced = True
        # convert the generator to a normal list
        new_metrics = list(metrics)

        for metric in new_metrics:
            if metric.name.startswith("neo4j_dbms_") or metric.name.startswith("neo4j_database_"):
                continue
            is_namespaced = False
            break

        if is_namespaced:
            self._check_namespaced_metrics(new_metrics, config)
        else:
            self._check_legacy_metrics(new_metrics, config)

    def _check_namespaced_metrics(self, metrics, config):
        for metric in metrics:
            if metric.name.startswith("neo4j_dbms_"):
                db_name = GLOBAL_DB_NAME
                metric.name = metric.name.replace("neo4j_dbms_", "", 1)
            else:
                db_name, metric_name = metric.name.replace("neo4j_database_", "", 1).split("_", 1)
                metric.name = metric_name
                # Exclude databases not in neo4j_dbs, if that config is set
                if config.neo4j_dbs and db_name not in config.neo4j_dbs:
                    continue

            tags = ['db_name:{}'.format(db_name)]
            if config.instance_tags:
                tags.extend(config.instance_tags.copy())
            self.process_metric(message=metric, custom_tags=tags)

    def _check_legacy_metrics(self, metrics, config):
        for metric in metrics:
            metric.name = metric.name.replace('neo4j_', '', 1)
            db_name = GLOBAL_DB_NAME
            if config.neo4j_version.startswith("4."):
                neo4j_db = self._get_db_for_metric(dbs=config.neo4j_dbs, metric_name=metric.name)
                if neo4j_db:
                    db_name = neo4j_db
                    metric.name = metric.name.replace('{}_'.format(db_name), '', 1)

            tags = ['db_name:{}'.format(db_name)]
            if config.instance_tags:
                tags.extend(config.instance_tags.copy())
            self.process_metric(message=metric, custom_tags=tags)

    def _get_db_for_metric(self, dbs, metric_name):
        for db in dbs:
            if metric_name.startswith('{}_'.format(db)):
                return db
        return None

    def _get_config(self, instance):
        host = self._get_value(instance=instance, key='host', required=True)
        port = self._get_value(instance=instance, key='port', required=False, default_value=2004)
        neo4j_version = self._get_value(instance=instance, key='neo4j_version', required=True)
        https = self._get_value(instance=instance, key='https', required=False, default_value='false')
        neo4j_dbs = self._get_value(instance=instance, key='neo4j_dbs', required=False, default_value=[])
        exclude_labels = self._get_value(instance=instance, key='exclude_labels', required=False, default_value=[])
        instance_tags = self._get_value(instance=instance, key='tags', required=False, default_value=[])

        if neo4j_version not in ["3.5", "4.0", "4.1", "4.2", "4.3", "4.4"]:
            raise ConfigurationError('neo4j_version "{}" is not a valid value'.format(neo4j_version))

        return Config(
            host=host,
            port=port,
            neo4j_version=neo4j_version,
            https=https,
            neo4j_dbs=neo4j_dbs,
            exclude_labels=exclude_labels,
            instance_tags=instance_tags,
        )

    def _get_value(self, instance, key, required, default_value=None):
        value = instance.get(key, default_value)
        if required and not value:
            raise ConfigurationError('"{}" is a required configuration'.format(key))
        return value

    def _set_whitelisted_metrics(self):
        self.NAMESPACE = NAMESPACE
        self.metrics_mapper = Neo4jCheck.get_whitelisted_metrics()

    @staticmethod
    def get_whitelisted_metrics():
        return {
            # bolt metrics
            'bolt_accumulated_processing_time_total': 'bolt.accumulated_processing_time',
            'bolt_accumulated_queue_time_total': 'bolt.accumulated_queue_time',
            'bolt_connections_closed_total': 'bolt.connections_closed',
            'bolt_connections_idle': 'bolt.connections_idle',
            'bolt_connections_opened_total': 'bolt.connections_opened',
            'bolt_connections_running': 'bolt.connections_running',
            'bolt_messages_done_total': 'bolt.messages_done',
            'bolt_messages_failed_total': 'bolt.messages_failed',
            'bolt_messages_received_total': 'bolt.messages_received',
            'bolt_messages_started_total': 'bolt.messages_started',
            #
            # causal clustering metrics
            'causal_clustering_catchup_tx_pull_requests_received_total': 'causal_clustering.catchup_tx_pull_requests_received',  # noqa: E501
            'causal_clustering_core_append_index': 'causal_clustering.core.append_index',
            'causal_clustering_core_commit_index': 'causal_clustering.core.commit_index',
            'causal_clustering_core_discovery_cluster_converged': 'causal_clustering.core.discovery.cluster.converged',  # noqa: E501
            'causal_clustering_core_discovery_cluster_members': 'causal_clustering.core.discovery.cluster.members',  # noqa: E501
            'causal_clustering_core_discovery_cluster_unreachable': 'causal_clustering.core.discovery.cluster.unreachable',  # noqa: E501
            # causal clustering replicated data metrics (4.3)
            'causal_clustering_core_discovery_replicated_data_member_data_invisible': 'causal_clustering.core.discovery.replicated_data.member_data.invisible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_member_data_visible': 'causal_clustering.core.discovery.replicated_data.member_data.visible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_raft_id_published_by_member_invisible': 'causal_clustering.core.discovery.replicated_data.raft_id_published_by_member.invisible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_raft_id_published_by_member_visible': 'causal_clustering.core.discovery.replicated_data.raft_id_published_by_member.visible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_per_db_leader_name_invisible': 'causal_clustering.core.discovery.replicated_data.per_db_leader_name.invisible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_per_db_leader_name_visible': 'causal_clustering.core.discovery.replicated_data.per_db_leader_name.visible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_member_db_state_invisible': 'causal_clustering.core.discovery.replicated_data.member_db_state.invisible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_member_db_state_visible': 'causal_clustering.core.discovery.replicated_data.member_db_state.visible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_raft_member_mapping_invisible': 'causal_clustering.core.discovery.replicated_data.raft_member_mapping.invisible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_raft_member_mapping_visible': 'causal_clustering.core.discovery.replicated_data.raft_member_mapping.visible',  # noqa: E501
            # causal clustering replicated data metrics (3.6)
            'causal_clustering_core_discovery_replicated_data_cluster_id_per_db_name_invisible': 'causal_clustering.core.discovery.replicated_data.cluster_id_per_db_name.invisible',  # noqa: E501
            'causal_clustering_core_discovery_replicated_data_cluster_id_per_db_name_visible': 'causal_clustering.core.discovery.replicated_data.cluster_id_per_db_name.visible',  # noqa: E501
            # end causal clustering replicated data metrics
            'causal_clustering_core_in_flight_cache_element_count': 'causal_clustering.core.in_flight_cache_element_count',  # noqa: E501
            'causal_clustering_core_in_flight_cache_hits_total': 'causal_clustering.core.in_flight_cache.hits',
            'causal_clustering_core_in_flight_cache_max_bytes': 'causal_clustering.core.in_flight_cache.max_bytes',
            'causal_clustering_core_in_flight_cache_max_elements': 'causal_clustering.core.in_flight_cache.max_elements',  # noqa: E501
            'causal_clustering_core_in_flight_cache_misses_total': 'causal_clustering.core.in_flight_cache.misses',
            'causal_clustering_core_in_flight_cache_total_bytes': 'causal_clustering.core.in_flight_cache.total_bytes',
            'causal_clustering_core_is_leader': 'causal_clustering.core.is_leader',
            'causal_clustering_core_message_processing_delay': 'causal_clustering.core.message_processing_delay',
            'causal_clustering_core_message_processing_timer': 'causal_clustering.core.message_processing_timer',
            'causal_clustering_core_message_processing_timer_append_entries_request': 'causal_clustering.core.message_processing_timer.append_entries_request',  # noqa: E501
            'causal_clustering_core_message_processing_timer_append_entries_response': 'causal_clustering.core.message_processing_timer.append_entries_response',  # noqa: E501
            'causal_clustering_core_message_processing_timer_election_timeout': 'causal_clustering.core.message_processing_timer.election_timeout',  # noqa: E501
            'causal_clustering_core_message_processing_timer_heartbeat': 'causal_clustering.core.message_processing_timer.heartbeat',  # noqa: E501
            'causal_clustering_core_message_processing_timer_heartbeat_response': 'causal_clustering.core.message_processing_timer.heartbeat_response',  # noqa: E501
            'causal_clustering_core_message_processing_timer_heartbeat_timeout': 'causal_clustering.core.message_processing_timer.heartbeat_timeout',  # noqa: E501
            'causal_clustering_core_message_processing_timer_log_compaction_info': 'causal_clustering.core.message_processing_timer.log_compaction_info',  # noqa: E501
            'causal_clustering_core_message_processing_timer_new_batch_request': 'causal_clustering.core.message_processing_timer.new_batch_request',  # noqa: E501
            'causal_clustering_core_message_processing_timer_new_entry_request': 'causal_clustering.core.message_processing_timer.new_entry_request',  # noqa: E501
            'causal_clustering_core_message_processing_timer_pre_vote_request': 'causal_clustering.core.message_processing_timer.pre_vote_request',  # noqa: E501
            'causal_clustering_core_message_processing_timer_pre_vote_response': 'causal_clustering.core.message_processing_timer.pre_vote_response',  # noqa: E501
            'causal_clustering_core_message_processing_timer_prune_request': 'causal_clustering.core.message_processing_timer.prune_request',  # noqa: E501
            'causal_clustering_core_message_processing_timer_vote_request': 'causal_clustering.core.message_processing_timer.vote_request',  # noqa: E501
            'causal_clustering_core_message_processing_timer_vote_response': 'causal_clustering.core.message_processing_timer.vote_response',  # noqa: E501
            'causal_clustering_core_replication_attempt_total': 'causal_clustering.core.replication_attempt',
            'causal_clustering_core_replication_fail_total': 'causal_clustering.core.replication_fail',
            'causal_clustering_core_replication_new_total': 'causal_clustering.core.replication_new',
            'causal_clustering_core_replication_success_total': 'causal_clustering.core.replication_success',
            'causal_clustering_core_term': 'causal_clustering.core.term',
            'causal_clustering_core_tx_retries_total': 'causal_clustering.core.tx_retries',
            #
            # database checkpointing metrics
            'check_point_events_total': 'check_point.events',
            'check_point_total_time_total': 'check_point.total_time',
            'check_point_duration': 'check_point.duration',
            #
            # cypher metrics
            'cypher_replan_events_total': 'cypher.replan_events',
            'cypher_replan_wait_time_total': 'cypher.replan_wait_time',
            #
            # database data metrics
            'neo4j_count_node': 'node_count',
            'neo4j_count_relationship': 'relationship_count',
            'ids_in_use_node': 'ids_in_use.node',
            'ids_in_use_property': 'ids_in_use.property',
            'ids_in_use_relationship': 'ids_in_use.relationship',
            'ids_in_use_relationship_type': 'ids_in_use.relationship_type',
            'store_size_total': 'store.size.total',
            'store_size_database': 'store.size.database',
            #
            # database transaction log metrics
            'log_appended_bytes_total': 'log.appended_bytes',
            'log_rotation_events_total': 'log.rotation_events',
            'log_rotation_total_time_total': 'log.rotation_total_time',
            'log_rotation_duration': 'log.rotation_duration',
            #
            # page cache metrics
            'page_cache_eviction_exceptions_total': 'page_cache.eviction_exceptions',
            'page_cache_evictions_total': 'page_cache.evictions',
            'page_cache_flushes_total': 'page_cache.flushes',
            'page_cache_hits_total': 'page_cache.hits',
            'page_cache_page_faults_total': 'page_cache.page_faults',
            'page_cache_pins_total': 'page_cache.pins',
            'page_cache_unpins_total': 'page_cache.unpins',
            #
            # server metrics
            'server_threads_jetty_all': 'server.threads.jetty.all',
            'server_threads_jetty_idle': 'server.threads.jetty.idle',
            #
            # transaction metrics
            'transaction_active': 'transaction.active',
            'transaction_active_read': 'transaction.active_read',
            'transaction_active_write': 'transaction.active_write',
            'transaction_committed_read_total': 'transaction.committed_read',
            'transaction_committed_total': 'transaction.committed',
            'transaction_committed_write_total': 'transaction.committed_write',
            'transaction_last_closed_tx_id_total': 'transaction.last_closed_tx_id',
            'transaction_last_committed_tx_id_total': 'transaction.last_committed_tx_id',
            'transaction_peak_concurrent_total': 'transaction.peak_concurrent',
            'transaction_rollbacks_read_total': 'transaction.rollbacks_read',
            'transaction_rollbacks_total': 'transaction.rollbacks',
            'transaction_rollbacks_write_total': 'transaction.rollbacks_write',
            'transaction_started_total': 'transaction.started',
            'transaction_terminated_read_total': 'transaction.terminated_read',
            'transaction_terminated_total': 'transaction.terminated',
            'transaction_terminated_write_total': 'transaction.terminated_write',
            'transaction_tx_size_heap': 'transaction.tx_size_heap',
            'transaction_tx_size_native': 'transaction.tx_size_native',
            #
            # JVM GC metrics
            'vm_gc_count_g1_old_generation_total': 'vm.gc.count.g1_old_generation',
            'vm_gc_count_g1_young_generation_total': 'vm.gc.count.g1_young_generation',
            'vm_gc_time_g1_old_generation_total': 'vm.gc.time.g1_old_generation',
            'vm_gc_time_g1_young_generation_total': 'vm.gc.time.g1_young_generation',
            #
            # JVM memory buffers metrics
            'vm_memory_buffer_direct_capacity': 'vm.memory.buffer.direct_capacity',
            'vm_memory_buffer_direct_count': 'vm.memory.buffer.direct_count',
            'vm_memory_buffer_direct_used': 'vm.memory.buffer.direct_used',
            'vm_memory_buffer_mapped_capacity': 'vm.memory.buffer.mapped_capacity',
            'vm_memory_buffer_mapped_count': 'vm.memory.buffer.mapped_count',
            'vm_memory_buffer_mapped_used': 'vm.memory.buffer.mapped_used',
            #
            # JVM memory pools metrics
            'vm_memory_pool_compressed_class_space': 'vm.memory.pool.compressed_class_space',
            'vm_memory_pool_g1_eden_space': 'vm.memory.pool.g1_eden_space',
            'vm_memory_pool_g1_old_gen': 'vm.memory.pool.g1_old_gen',
            'vm_memory_pool_g1_survivor_space': 'vm.memory.pool.g1_survivor_space',
            'vm_memory_pool_metaspace': 'vm.memory.pool.metaspace',
            #
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
            #
            # JVM threads metrics
            'vm_thread_count': 'vm.thread.count',
            'vm_thread_total': 'vm.thread.total',
        }
