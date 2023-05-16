import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.neo4j import Neo4jCheck

from .common import METRICS_URL

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures('dd_environment')]


def test_v4(aggregator, dd_run_check, instance):
    check = Neo4jCheck('neo4j', {}, [instance])
    dd_run_check(check)

    aggregator.assert_service_check('neo4j.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_metric('neo4j.page_cache.hits.count', tags=['db_name:global', f'endpoint:{METRICS_URL}'])
