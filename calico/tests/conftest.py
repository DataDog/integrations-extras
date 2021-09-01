import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture
def instance():
    return {
        "openmetrics_endpoint": "http://localhost:9091/metrics",
        "namespace": "calico",
        "extra_metrics": [
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
        ],
    }
