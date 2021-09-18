import pytest

from datadog_checks.calico import CalicoCheck
from datadog_checks.dev.utils import get_metadata_metrics

from . import common
from .utils import get_fixture_path


@pytest.mark.unit
def test_check(aggregator, dd_run_check, mock_http_response):

    mock_http_response(file_path=get_fixture_path('calico.txt'))
    check = CalicoCheck('calico', {}, [common.MOCK_CALICO_INSTANCE])
    dd_run_check(check)

    aggregator.assert_metric("calico.felix_active_local_endpoints", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_active_local_policies", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_active_local_selectors", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_active_local_tags", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_cluster_num_host_endpoints", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_cluster_num_hosts", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_cluster_num_workload_endpoints", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_ipset_calls.count", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_ipset_errors.count", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_ipsets_calico", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_ipsets_total", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_iptables_chains", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_iptables_rules", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_iptables_restore_calls.count", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_iptables_restore_errors.count", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_iptables_save_calls.count", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_iptables_save_errors.count", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_int_dataplane_failures.count", metric_type=aggregator.MONOTONIC_COUNT)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
