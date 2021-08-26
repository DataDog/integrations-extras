from typing import Any, Dict

import pytest
from requests.exceptions import ConnectionError

from datadog_checks.base import ConfigurationError
from datadog_checks.base.errors import CheckException
from datadog_checks.base.stubs.aggregator import AggregatorStub
from datadog_checks.calico import CalicoCheck
from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.unit
def test_config():
    # instance vide
    with pytest.raises(CheckException):
        instance = {}
        CalicoCheck('calico', {}, [instance])

    instance = {'prometheus_url': "http://foo.bar"}
    c = CalicoCheck('calico', {}, instance)

    # instance vide
    with pytest.raises(ConfigurationError):
        c.check({})

    # url defined but not reachable
    with pytest.raises(ConnectionError):
        c.check({'prometheus_url': "http://foo.bar"})


@pytest.mark.integration
def test_check(aggregator, instance):
    # type: (AggregatorStub, Dict[str, Any]) -> None
    check = CalicoCheck('calico', {}, [instance])
    check.check(instance)

    aggregator.assert_metric("calico.felix_active_local_endpoints", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_active_local_policies", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_active_local_selectors", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_active_local_tags", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_cluster_num_host_endpoints", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_cluster_num_hosts", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_cluster_num_workload_endpoints", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_ipset_calls", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_ipset_errors", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_ipsets_calico", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_ipsets_total", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_iptables_chains", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_iptables_rules", metric_type=aggregator.GAUGE)
    aggregator.assert_metric("calico.felix_iptables_restore_calls", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_iptables_restore_errors", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_iptables_save_calls", metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_metric("calico.felix_iptables_save_errors", metric_type=aggregator.MONOTONIC_COUNT)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
