import pytest

# test transforming tidb check config to openmetrics check config
from datadog_checks.base.utils.tagging import GENERIC_TAGS
from datadog_checks.tidb import TiDBCheck

from .expected import EXPECTED_TIDB, EXPECTED_TIFLASH, EXPECTED_TIFLASH_PROXY, EXPECTED_TIKV


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
def test_tiflash_mock_metrics(aggregator, mock_tiflash_metrics, tiflash_instance):
    check = TiDBCheck("test_tiflash_mock_metrics", {}, [tiflash_instance])
    _check_and_assert(aggregator, EXPECTED_TIFLASH, check)


@pytest.mark.unit
def test_tiflash_proxy_mock_metrics(aggregator, mock_tiflash_proxy_metrics, tiflash_proxy_instance):
    check = TiDBCheck("test_tiflash_proxy_mock_metrics", {}, [tiflash_proxy_instance])
    _check_and_assert(aggregator, EXPECTED_TIFLASH_PROXY, check)


@pytest.mark.unit
def test_tikv_mock_metrics(aggregator, mock_tikv_metrics, tikv_instance):
    check = TiDBCheck("test_tidb_mock_metrics", {}, [tikv_instance])
    _check_and_assert(aggregator, EXPECTED_TIKV, check)


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_cluster_metrics(aggregator, tikv_instance, tidb_instance, tiflash_instance, tiflash_proxy_instance):
    check = TiDBCheck("test_cluster_metrics", {}, [tidb_instance])
    _check_and_assert(aggregator, EXPECTED_TIDB, check)
    check = TiDBCheck("test_cluster_metrics", {}, [tiflash_instance])
    _check_and_assert(aggregator, EXPECTED_TIFLASH, check)
    check = TiDBCheck("test_cluster_metrics", {}, [tiflash_proxy_instance])
    _check_and_assert(aggregator, EXPECTED_TIFLASH_PROXY, check)
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
