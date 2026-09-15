import os

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_PROMETHEUS_METRICS = [
    'scaleops.health_check',
    'scaleops.events',
    'scaleops.alerts',
    'scaleops.multi_cluster_child_connection_status',
    'scaleops.recommendation_managed_workload_status',
    'scaleops.total_automated_workloads',
    'scaleops.cluster_automation_score',
    'scaleops.sum_workloads_oom',
    'scaleops.namespace_auto_state',
    'scaleops.estimated_monthly_costs',
    'scaleops.hpa_optimization_gap',
    'scaleops.underprovisioned_workloads',
    'scaleops.sum_automated_pods_count',
    'scaleops.recommendation_attached_policy',
    'scaleops.zdt_pod_force_delete',
    'scaleops.updater_failed_evictions',
    'scaleops.total_unautomated_workloads',
    'scaleops.argo_out_of_sync_object',
    'scaleops.health_check_admissions',
    'scaleops.dashboard_wasted_resources',
    'scaleops.nodes_total_hourly_cost',
    'scaleops.total_workloads_by_type',
    'scaleops.prometheus_tsdb_storage_usage_percentage',
    'scaleops.min_replicas_active_savings',
    'scaleops.evictions_by_types_count',
    'scaleops.consolidation_system_errors',
    'scaleops.min_replicas_available_savings',
    'scaleops.automated_not_optimized_workloads',
    'scaleops.kubelet_eviction_event_count',
    'scaleops.workload_recommendation_not_updated',
    'scaleops.pod_container_resource_recommendation_requests',
    'scaleops.hpa_threshold_optimization_gap',
    'scaleops.avg_active_node_monthly_cost',
    'scaleops.memory_underprovisioned_pods_on_stress_nodes',
    'scaleops.total_argo_out_of_sync_hpa_objects_count',
    'scaleops.workloads_with_cpu_throttle_percentage_higher_than_75_count',
]

MOCKED_INSTANCE = {'openmetrics_endpoint': 'http://localhost:9090/metrics'}

BAD_HOSTNAME_INSTANCE = {'openmetrics_endpoint': 'http://invalid-hostname:9090/metrics'}


def get_fixture_path(filename):
    return os.path.join(HERE, 'fixtures', filename)
