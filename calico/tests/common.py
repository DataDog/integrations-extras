EXTRA_METRICS = [
    "felix_active_local_endpoints",
    "felix_active_local_policies",
    "felix_active_local_selectors",
    "felix_active_local_tags",
    "felix_cluster_num_host_endpoints",
    "felix_cluster_num_hosts",
    "felix_cluster_num_workload_endpoints",
    "felix_ipset_calls",
    "felix_ipset_errors",
    "felix_ipsets_calico",
    "felix_ipsets_total",
    "felix_iptables_chains",
    "felix_iptables_rules",
    "felix_iptables_restore_calls",
    "felix_iptables_restore_errors",
    "felix_iptables_save_calls",
    "felix_iptables_save_errors",
    "felix_int_dataplane_failures.count"

]

FORMATTED_EXTRA_METRICS = [
    "calico.felix_active_local_endpoints",
    "calico.felix_active_local_policies",
    "calico.felix_active_local_selectors",
    "calico.felix_active_local_tags",
    "calico.felix_cluster_num_host_endpoints",
    "calico.felix_cluster_num_hosts",
    "calico.felix_cluster_num_workload_endpoints",
    "calico.felix_ipset_calls.count",
    "calico.felix_ipset_errors.count",
    "calico.felix_ipsets_calico",
    "calico.felix_ipsets_total",
    "calico.felix_iptables_chains",
    "calico.felix_iptables_rules",
    "calico.felix_iptables_restore_calls.count",
    "calico.felix_iptables_restore_errors.count",
    "calico.felix_iptables_save_calls.count",
    "calico.felix_iptables_save_errors.count",
    "calico.felix_int_dataplane_failures.count",
]

MOCK_CALICO_INSTANCE = {
    "openmetrics_endpoint": 'http://localhost:9091/metrics',
    "namespace": "calico",
    "extra_metrics": EXTRA_METRICS,
}
