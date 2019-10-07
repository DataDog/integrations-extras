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
