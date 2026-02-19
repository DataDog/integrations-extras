# metrics.py

# Curated: UC essentials only
DEFAULT_METRICS = [
    {"uc_history_total": "uc_history.total"},
    {"uc_task_instance_active": "uc_task_instance.active"},
    {"uc_task_instance_launch_total": "uc_task_instance.launch.total"},
    {"uc_task_instance_late_start_total": "uc_task_instance.late_start.total"},
    {"uc_task_instance_late_finish_total": "uc_task_instance.late_finish.total"},
    {"uc_task_instance_early_finish_total": "uc_task_instance.early_finish.total"},
    {"uc_task_instance_duration_seconds": "uc_task_instance.duration.seconds"},
    {"uc_universal_event_total": "uc_universal_event.total"},
    {"uc_agent_status": "uc_agent.status"},
    {"uc_build_info": "uc_build.info"},
    {"uc_database_connection_pool_active": "uc_database_connection_pool.active"},
    {"uc_database_connection_pool_idle": "uc_database_connection_pool.idle"},
    {"uc_database_connection_pool_idle_min": "uc_database_connection_pool.idle_min"},
    {"uc_database_connection_pool_idle_max": "uc_database_connection_pool.idle_max"},
    {"uc_database_connection_pool_allocated": "uc_database_connection_pool.allocated"},
    {"uc_database_connection_pool_max": "uc_database_connection_pool.max"},
    {"uc_oms_server_last_connected_time_seconds": "uc_oms_server.last_connected_time.seconds"},
    {"uc_oms_server_status": "uc_oms_server.status"},
    {"uc_oms_server_session_status": "uc_oms_server.session.status"},
    {"uc_monthly_executions": "uc_monthly_executions"},
]

# Opt-in groups
ADDITIONAL_METRICS = {
    "jvm": [
        {"jvm_threads_current": "jvm_threads_current"},
        {"jvm_threads_peak": "jvm_threads_peak"},
        {"jvm_memory_used_bytes": "jvm_memory_used_bytes"},
        {"jvm_memory_committed_bytes": "jvm_memory_committed_bytes"},
    ],
    "process": [
        {"process_cpu_seconds_total": "process_cpu_seconds_total"},
        {"process_resident_memory_bytes": "process_resident_memory_bytes"},
        {"process_virtual_memory_bytes": "process_virtual_memory_bytes"},
        {"process_open_fds": "process_open_fds"},
    ],
    "license_details": [
        {"uc_license_agents_distributed_used": "uc_license.agents_distributed.used"},
        {"uc_license_agents_distributed_max": "uc_license.agents_distributed.max"},
        {"uc_license_agents_zos_used": "uc_license.agents_zos.used"},
        {"uc_license_agents_zos_max": "uc_license.agents_zos.max"},
        {"uc_license_cluster_nodes_used": "uc_license.cluster_nodes.used"},
        {"uc_license_cluster_nodes_max": "uc_license.cluster_nodes.max"},
        {"uc_license_monthly_executions_used": "uc_license.monthly_executions.used"},
        {"uc_license_monthly_executions_max": "uc_license.monthly_executions.max"},
        {"uc_license_task_definitions_used": "uc_license.task_definitions.used"},
        {"uc_license_task_definitions_max": "uc_license.task_definitions.max"},
    ],
}
