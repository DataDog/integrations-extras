from time import sleep

import pytest

from datadog_checks.redisenterprise import RedisenterpriseCheck

# from datadog_checks.dev.utils import get_metadata_metrics


@pytest.mark.unit
def test_check(aggregator, instance):
    instance['is_mock'] = True
    check = RedisenterpriseCheck('redisenterprise', {}, [instance])
    check.check({'host': 'localhost', 'username': 'chris@example.com', 'password': 'thePasswerd', 'is_mock': True})


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_version(aggregator, instance):
    # We need to wait for the server to completely run
    sleep(60)
    check = RedisenterpriseCheck('redisenterprise', {}, [instance])
    check.check(instance)
    aggregator.assert_service_check('redisenterprise.running', RedisenterpriseCheck.OK)
    aggregator.assert_service_check('redisenterprise.license_status', RedisenterpriseCheck.OK)
    aggregator.assert_metric('redisenterprise.conns', 0.0)
    aggregator.assert_metric('redisenterprise.database_count', 1.0)
    aggregator.assert_metric('redisenterprise.endpoints', 1.0)
    aggregator.assert_metric('redisenterprise.cache_hit_rate', 0.0)
    aggregator.assert_metric('redisenterprise.license_shards', 4.0)
    aggregator.assert_metric('redisenterprise.total_shards_used', 1.0)
    aggregator.assert_metric('redisenterprise.total_node_count', 1.0)
    aggregator.assert_metric('redisenterprise.total_active_nodes', 1.0)
    assert len(aggregator._events) > 3
