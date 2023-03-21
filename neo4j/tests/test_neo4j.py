import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.neo4j import Neo4jCheck

from .common import METRICS_URL, NEO4J_VERSION

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures('dd_environment')]


def test(aggregator, dd_run_check, instance):
    check = Neo4jCheck('neo4j', {}, [instance])
    dd_run_check(check)

    aggregator.assert_service_check('neo4j.openmetrics.health', ServiceCheck.OK)

    if NEO4J_VERSION.startswith('3.5'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
    elif NEO4J_VERSION.startswith('4.0'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:system', f'endpoint:{METRICS_URL}'])
    elif NEO4J_VERSION.startswith('4.1'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:system', f'endpoint:{METRICS_URL}'])
    elif NEO4J_VERSION.startswith('4.2'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:system', f'endpoint:{METRICS_URL}'])
    elif NEO4J_VERSION.startswith('4.3'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:system', f'endpoint:{METRICS_URL}'])
    elif NEO4J_VERSION.startswith('4.4'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:system', f'endpoint:{METRICS_URL}'])
    elif NEO4J_VERSION.startswith('5'):
        aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}'])
        aggregator.assert_metric('neo4j.check_point.duration', tags=['db_name:system', f'endpoint:{METRICS_URL}'])
    else:
        raise Exception(f'unknown neo4j_version: {NEO4J_VERSION}')
