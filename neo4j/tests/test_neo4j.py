import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.neo4j import GLOBAL_DB_NAME, NAMESPACE, Config, Neo4jCheck

from dataclasses import dataclass


@dataclass
class FakeMetric:
    name: str


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    check = Neo4jCheck('neo4j', {}, {})

    instance['neo4j_dbs'] = ['neo4j', 'system']

    check.check(instance)

    print(aggregator.metric_names)

    if instance.get('neo4j_version') == '3.5':
        aggregator.assert_metric(
            name='{}.page_cache.hits'.format(NAMESPACE), tags=['db_name:{}'.format(GLOBAL_DB_NAME)],
        )
        aggregator.assert_metric(
            name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:{}'.format(GLOBAL_DB_NAME)],
        )
    elif instance.get('neo4j_version') == '4.0':
        aggregator.assert_metric(
            name='{}.page_cache.hits'.format(NAMESPACE), tags=['db_name:{}'.format(GLOBAL_DB_NAME)],
        )
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:neo4j'])
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:system'])
    elif instance.get('neo4j_version') == '4.1':
        aggregator.assert_metric(
            name='{}.page_cache.hits'.format(NAMESPACE), tags=['db_name:{}'.format(GLOBAL_DB_NAME)],
        )
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:neo4j'])
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:system'])
    elif instance.get('neo4j_version') == '4.2':
        aggregator.assert_metric(
            name='{}.page_cache.hits'.format(NAMESPACE), tags=['db_name:{}'.format(GLOBAL_DB_NAME)],
        )
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:neo4j'])
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:system'])
    elif instance.get('neo4j_version') == '4.3':
        aggregator.assert_metric(
            name='{}.page_cache.hits'.format(NAMESPACE), tags=['db_name:{}'.format(GLOBAL_DB_NAME)],
        )
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:neo4j'])
        aggregator.assert_metric(name='{}.check_point.events'.format(NAMESPACE), tags=['db_name:system'])
    else:
        raise Exception('unknown neo4j_version: {}'.format(instance.get('neo4j_version')))


@pytest.mark.unit
def test_get_db_for_metric():
    check = Neo4jCheck('neo4j', {}, {})

    assert check._get_db_for_metric(dbs=['neo4j', 'system'], metric_name='neo4j_metric_1') == 'neo4j'
    assert check._get_db_for_metric(dbs=['neo4j', 'system'], metric_name='system_metric_1') == 'system'
    assert check._get_db_for_metric(dbs=['neo4j', 'system'], metric_name='metric_1') is None


@pytest.mark.unit
def test_check_namespaced_metrics():
    out = []

    def fake_process_metric(message, **kwargs):
        out.append((message, kwargs))

    check = Neo4jCheck('neo4j', {}, {})
    check.process_metric = fake_process_metric

    config = Config(host='localhost', port=9000, neo4j_version='4.0', https='false', neo4j_dbs=[],
                    exclude_labels=['kube_service'], instance_tags=['key:value'])

    check._check_metrics([
        FakeMetric("neo4j_dbms_some_global_metric"),
        FakeMetric("neo4j_database_mydb_some_local_metric"),
    ], config=config)

    assert out == [
        (FakeMetric("some_global_metric"), {'custom_tags': ['db_name:global', 'key:value']}),
        (FakeMetric("some_local_metric"), {'custom_tags': ['db_name:mydb', 'key:value']}),
    ]


@pytest.mark.unit
def test_get_config():
    check = Neo4jCheck('neo4j', {}, {})

    instance = {
        'host': 'localhost',
        'port': 9000,
        'neo4j_version': '4.0',
        'neo4j_dbs': ['neo4j', 'system'],
        'exclude_labels': ['kube_service'],
        'tags': ['key:value'],
    }
    assert check._get_config(instance) == Config(
        host='localhost',
        port=9000,
        neo4j_version='4.0',
        neo4j_dbs=['neo4j', 'system'],
        exclude_labels=['kube_service'],
        instance_tags=['key:value'],
    )

    instance = {
        'host': 'localhost',
        'neo4j_version': '3.5',
    }
    assert check._get_config(instance) == Config(
        host='localhost', port=2004, neo4j_version='3.5', https='false', neo4j_dbs=[],
        exclude_labels=[], instance_tags=[],
    )

    instance = {}
    with pytest.raises(ConfigurationError):
        check._get_config(instance)

    instance = {'host': 'localhost'}
    with pytest.raises(ConfigurationError):
        check._get_config(instance)


@pytest.mark.unit
def test_get_value():
    check = Neo4jCheck('neo4j', {}, {})

    with pytest.raises(ConfigurationError):
        check._get_value({}, 'neo4j_version', required=True)

    assert check._get_value({}, 'neo4j_dbs', False, ['neo4j']) == ['neo4j']
    assert check._get_value({'neo4j_version': '3.5'}, 'neo4j_version', True)
