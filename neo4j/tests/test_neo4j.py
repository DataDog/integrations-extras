# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import pytest

from datadog_checks.base.errors import CheckException
from datadog_checks.neo4j import Neo4jCheck

from .common import CHECK_NAME, CONNECTION_FAILURE, NEO4J_MINIMAL_CONFIG, NEO4J_VARS


@pytest.mark.usefixtures('dd_environment')
def test_minimal_config(aggregator):
    c = Neo4jCheck(CHECK_NAME, {}, [NEO4J_MINIMAL_CONFIG])
    c.check(NEO4J_MINIMAL_CONFIG)

    # Test service check
    aggregator.assert_service_check('neo4j.can_connect', status=Neo4jCheck.OK)

    # Test metrics
    testable_metrics = NEO4J_VARS

    for mname in testable_metrics:
        aggregator.assert_metric('neo4j.{}'.format(mname), tags=[])

    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures('dd_environment')
def test_connection_failure(aggregator):
    """
    Service check reports connection failure
    """
    c = Neo4jCheck(CHECK_NAME, {}, [CONNECTION_FAILURE])

    with pytest.raises(CheckException):
        c.check(CONNECTION_FAILURE)

    aggregator.assert_service_check('neo4j.can_connect', status=Neo4jCheck.CRITICAL)
