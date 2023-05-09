import pytest

from datadog_checks.base.constants import ServiceCheck
from datadog_checks.neo4j import Neo4jCheck

from .common import METRICS_URL

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures('dd_environment_v5')]


def test_v5(aggregator, dd_run_check, instance):
    check = Neo4jCheck('neo4j', {}, [instance])
    dd_run_check(check)

    aggregator.assert_service_check('neo4j.openmetrics.health', ServiceCheck.OK)
    aggregator.assert_metric(
        'neo4j.transaction_committed_read.count', tags=['db_name:neo4j', f'endpoint:{METRICS_URL}']
    )
    aggregator.assert_metric(
        'neo4j.transaction_committed_read.count', tags=['db_name:system', f'endpoint:{METRICS_URL}']
    )
