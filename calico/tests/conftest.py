from os import path

import pytest

from datadog_checks.dev import kind, run_command

URL = "http://localhost:9091/metrics"
NAMESPACE = "calico"
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
]
INSTANCE = {"openmetrics_endpoint": URL, "namespace": NAMESPACE, "extra_metrics": EXTRA_METRICS}
HERE = path.dirname(path.abspath(__file__))


def setup_calico():
    # Deploy calico
    run_command(["kubectl", "apply", "-f", "https://docs.projectcalico.org/manifests/calico.yaml"])

    # Install calicoctl as a pod
    run_command(["kubectl", "apply", "-f", "https://docs.projectcalico.org/manifests/calicoctl.yaml"])

    # Create felix metrics service
    run_command(["kubectl", "apply", "-f", path.join(HERE, 'felix-service.yaml')])

    # Wait for pods
    run_command(["kubectl", "wait", "--for=condition=Ready", "pods", "--all", "--all-namespaces", "--timeout=300s"])


@pytest.fixture(scope='session')
def dd_environment():

    with kind.kind_run(conditions=[setup_calico], kind_config=path.join(HERE, 'kind-calico.yaml')):
        # Activate Felix
        run_command(
            """kubectl exec -i -n kube-system calicoctl -- /calicoctl patch felixConfiguration
            default --patch '{"spec":{"prometheusMetricsEnabled": true}}'"""
        )

        # Port forward felix service since Kind does not expose external IP for its service
        run_command("""kubectl port-forward service/felix-metrics-svc 9091:9091 -n kube-system &""")

        yield INSTANCE


@pytest.fixture
def instance():
    return INSTANCE.copy()
