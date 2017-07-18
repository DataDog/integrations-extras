# stdlib
from nose.plugins.attrib import attr

# 3p

# project
from tests.checks.common import AgentCheckTest


instance = {
    'sentinel_host': 'localhost',
    'sentinel_port': 26379,
    'masters': ['mymaster']
}

METRICS = [
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

@attr(requires='redis_sentinel', mock=False)  # set mock to True if appropriate
class TestRedis_sentinel(AgentCheckTest):
    """Basic Test for redis_sentinel integration."""
    CHECK_NAME = 'redis_sentinel'

    def test_check(self):
        """
        Testing Redis_sentinel check.
        """
        self.run_check({'instances': [instance]})

        for mname in METRICS:
            self.assertMetric(mname, at_least=1)

        for svc_chk in SERVICE_CHECKS:
            self.assertServiceCheckOK(svc_chk)

        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
