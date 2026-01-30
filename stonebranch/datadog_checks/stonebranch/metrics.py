# metrics.py

# Curated: UC essentials only
DEFAULT_METRICS = [
    {"uc_history_total": "uc_history_total"},
    {"uc_task_instance_active": "uc_task_instance_active"},
    {"uc_task_instance_launch_total": "uc_task_instance_launch_total"},
    {"uc_task_instance_late_start_total": "uc_task_instance_late_start_total"},
    {"uc_task_instance_late_finish_total": "uc_task_instance_late_finish_total"},
    {"uc_task_instance_early_finish_total": "uc_task_instance_early_finish_total"},
    {"uc_universal_event_total": "uc_universal_event_total"},
    {"uc_agent_status": "uc_agent_status"},
    {"uc_build_info": "uc_build_info"},
    {"uc_database_connection_pool_active": "uc_database_connection_pool_active"},
    {"uc_database_connection_pool_idle": "uc_database_connection_pool_idle"},
    {"uc_database_connection_pool_idle_min": "uc_database_connection_pool_idle_min"},
    {"uc_database_connection_pool_idle_max": "uc_database_connection_pool_idle_max"},
    {"uc_database_connection_pool_allocated": "uc_database_connection_pool_allocated"},
    {"uc_database_connection_pool_max": "uc_database_connection_pool_max"},
    {"uc_oms_server_last_connected_time_seconds": "uc_oms_server_last_connected_time_seconds"},
    {"uc_oms_server_status": "uc_oms_server_status"},
    {"uc_oms_server_session_status": "uc_oms_server_session_status"},
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
        {"uc_license_agents_distributed_used": "uc_license_agents_distributed_used"},
        {"uc_license_agents_distributed_max": "uc_license_agents_distributed_max"},
        {"uc_license_agents_zos_used": "uc_license_agents_zos_used"},
        {"uc_license_agents_zos_max": "uc_license_agents_zos_max"},
        {"uc_license_cluster_nodes_used": "uc_license_cluster_nodes_used"},
        {"uc_license_cluster_nodes_max": "uc_license_cluster_nodes_max"},
        {"uc_license_monthly_executions_used": "uc_license_monthly_executions_used"},
        {"uc_license_monthly_executions_max": "uc_license_monthly_executions_max"},
        {"uc_license_task_definitions_used": "uc_license_task_definitions_used"},
        {"uc_license_task_definitions_max": "uc_license_task_definitions_max"},
    ],
}
