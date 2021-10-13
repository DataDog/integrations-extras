import pytest

from datadog_checks.tidb import TiDBCheck

from .expected import EXPECTED_PD_METRICS, EXPECTED_TIDB_METRICS, EXPECTED_TIKV_METRICS

# test transforming tidb check config to openmetrics check config


@pytest.mark.unit
def test_create_check_instance_transform(required_instances):
    check = TiDBCheck("test_config_transform", {}, [required_instances])
    ensure_tidb = False
    ensure_tikv = False
    ensure_pd = False
    for i in check.instances:
        if i.get("prometheus_url") == "http://localhost:10080/metrics":
            ensure_tidb = True
        if i.get("prometheus_url") == "http://localhost:20180/metrics":
            ensure_tikv = True
        if i.get("prometheus_url") == "http://localhost:2379/metrics":
            ensure_pd = True
    assert ensure_tidb and ensure_tikv and ensure_pd, "transforming config failed."


@pytest.mark.unit
def test_tidb_mock_metrics(aggregator, mock_tidb_metrics, required_instances):
    check = TiDBCheck("test_tidb_mock_metrics", {}, [required_instances])
    ins = {}
    for instance in check.instances:
        if instance.get("prometheus_url") == "http://localhost:10080/metrics":
            ins = instance
    _check_and_assert(aggregator, ins, EXPECTED_TIDB_METRICS, check)


@pytest.mark.unit
def test_pd_mock_metrics(aggregator, mock_pd_metrics, required_instances):
    check = TiDBCheck("test_pd_mock_metrics", {}, [required_instances])
    ins = {}
    for instance in check.instances:
        if instance.get("prometheus_url") == "http://localhost:2379/metrics":
            ins = instance
    _check_and_assert(aggregator, ins, EXPECTED_PD_METRICS, check)


@pytest.mark.unit
def test_tikv_mock_metrics(aggregator, mock_tikv_metrics, required_instances):
    check = TiDBCheck("test_tidb_mock_metrics", {}, [required_instances])
    ins = {}
    for instance in check.instances:
        if instance.get("prometheus_url") == "http://localhost:20180/metrics":
            ins = instance
    _check_and_assert(aggregator, ins, EXPECTED_TIKV_METRICS, check)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_cluster_metrics(aggregator, required_instances):
    check = TiDBCheck("test_cluster_metrics", {}, [required_instances])
    ensure_tidb = False
    ensure_tikv = False
    ensure_pd = False
    for instance in check.instances:
        # ensure correctness for 3 components (tidb, pd, tikv)
        if instance.get("prometheus_url") == "http://localhost:10080/metrics":
            _check_and_assert(aggregator, instance, EXPECTED_TIDB_METRICS, check)
            ensure_tidb = True
        elif instance.get("prometheus_url") == "http://localhost:2379/metrics":
            _check_and_assert(aggregator, instance, EXPECTED_PD_METRICS, check)
            ensure_tikv = True
        elif instance.get("prometheus_url") == "http://localhost:20180/metrics":
            _check_and_assert(aggregator, instance, EXPECTED_TIKV_METRICS, check)
            ensure_pd = True
        else:
            pass
    assert ensure_tidb and ensure_tikv and ensure_pd, "each 3 components must be covered!"


def _check_and_assert(agg, ins, expected, c):
    c.check(ins)
    for metric in expected:
        agg.assert_metric(metric)

    agg.assert_service_check(ins['namespace'] + '.prometheus.health')

    # since tidb cluster metrics cannot be listed thoroughly, we disable all completeness assertions here
    # agg.assert_all_metrics_covered()
    # agg.assert_metrics_using_metadata(get_metadata_metrics(), check_metric_type=False)
