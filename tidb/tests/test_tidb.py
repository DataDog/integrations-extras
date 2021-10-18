import pytest

# test transforming tidb check config to openmetrics check config
from datadog_checks.base.utils.tagging import GENERIC_TAGS
from datadog_checks.tidb import TiDBCheck

from .conftest import EXPECTED_PD, EXPECTED_TIDB, EXPECTED_TIKV


@pytest.mark.unit
def test_create_check_instance_transform(tidb_instance):
    check = TiDBCheck("test_config_transform", {}, [tidb_instance])
    assert check.instance.get('prometheus_url') == 'http://localhost:10080/metrics'
    assert check.instance.get('namespace') == 'tidb_cluster'
    assert check.instance.get('tags') == ['tidb_cluster_name:test', 'tidb_cluster_component:tidb']
    mapper = check.instance.get('labels_mapper')
    for label in GENERIC_TAGS:
        assert mapper.get(label) == label + "_in_app"


@pytest.mark.unit
def test_tidb_mock_metrics(aggregator, mock_tidb_metrics, tidb_instance):
    check = TiDBCheck("test_tidb_mock_metrics", {}, [tidb_instance])
    _check_and_assert(aggregator, EXPECTED_TIDB, check)


@pytest.mark.unit
def test_pd_mock_metrics(aggregator, mock_pd_metrics, pd_instance):
    check = TiDBCheck("test_pd_mock_metrics", {}, [pd_instance])
    _check_and_assert(aggregator, EXPECTED_PD, check)


@pytest.mark.unit
def test_tikv_mock_metrics(aggregator, mock_tikv_metrics, tikv_instance):
    check = TiDBCheck("test_tidb_mock_metrics", {}, [tikv_instance])
    _check_and_assert(aggregator, EXPECTED_TIKV, check)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_cluster_metrics(aggregator, pd_instance, tikv_instance, tidb_instance):
    check = TiDBCheck("test_cluster_metrics", {}, [tidb_instance])
    _check_and_assert(aggregator, EXPECTED_TIDB, check)
    check = TiDBCheck("test_cluster_metrics", {}, [pd_instance])
    _check_and_assert(aggregator, EXPECTED_PD, check)
    check = TiDBCheck("test_cluster_metrics", {}, [tikv_instance])
    _check_and_assert(aggregator, EXPECTED_TIKV, check)


def _check_and_assert(agg, expected, c):
    c.check(c.instance)
    for name, tags in expected['metrics'].items():
        agg.assert_metric(name, tags=tags)
    for name, tags in expected['service_check'].items():
        agg.assert_service_check(name, status=TiDBCheck.OK, tags=tags)

    # since tidb cluster metrics cannot be listed thoroughly, we disable all completeness assertions here
    # agg.assert_all_metrics_covered()
    # agg.assert_metrics_using_metadata(get_metadata_metrics(), check_metric_type=False)
