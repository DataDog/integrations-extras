import mock
import pytest

from datadog_checks.redis_sentinel import RedisSentinelCheck

METRICS = [
    'redis.sentinel.odown_slaves',
    'redis.sentinel.sdown_slaves',
    'redis.sentinel.ok_slaves',
    'redis.sentinel.ok_sentinels',
    'redis.sentinel.known_sentinels',
    'redis.sentinel.known_slaves',
    'redis.sentinel.link_pending_commands',
]

SERVICE_CHECKS = [
    'redis.sentinel.master_is_disconnected',
    'redis.sentinel.master_is_down',
    'redis.sentinel.slave_is_disconnected',
    'redis.sentinel.slave_master_link_down',
]

CHECK_NAME = 'redis_sentinel'


@pytest.mark.usefixtures('dd_environment')
def test_check(aggregator, instance):
    """
    Testing Redis_sentinel check.
    """
    check = RedisSentinelCheck(CHECK_NAME, {}, {})
    check.check(instance)

    for mname in METRICS:
        aggregator.assert_metric(mname, at_least=1)

    for svc_chk in SERVICE_CHECKS:
        aggregator.assert_service_check(svc_chk, status=RedisSentinelCheck.OK, count=1)

    aggregator.assert_all_metrics_covered()


@pytest.mark.usefixtures('dd_environment')
def test_down_slaves(aggregator, instance):
    """
    Testing Redis_sentinel check.
    """
    check = RedisSentinelCheck(CHECK_NAME, {}, {})

    sentinel_slaves = []
    for _ in range(5):
        sentinel_slaves.append({'is_odown': True, 'is_sdown': False})
    for _ in range(7):
        sentinel_slaves.append({'is_odown': False, 'is_sdown': True})

    with mock.patch('redis.StrictRedis.sentinel_slaves', return_value=sentinel_slaves):
        check.check(instance)

        aggregator.assert_metric('redis.sentinel.odown_slaves', 5)
        aggregator.assert_metric('redis.sentinel.sdown_slaves', 7)
