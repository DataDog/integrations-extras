import pytest

from datadog_checks.kurrentdb import KurrentdbCheck


@pytest.mark.e2e
def test_e2e(dd_agent_check, instance):
    aggregator = dd_agent_check(instance, rate=True)

    aggregator.assert_service_check('kurrentdb.openmetrics.health', KurrentdbCheck.OK)
    aggregator.assert_service_check('kurrentdb.api.can_connect', KurrentdbCheck.OK, at_least=1)

    for metric in (
        'kurrentdb.proc_thread_count',
        'kurrentdb.is_leader',
        'kurrentdb.cluster.member_alive',
        'kurrentdb.cluster.last_commit_position',
        'kurrentdb.subscription.live',
        'kurrentdb.projection.running',
        'kurrentdb.es.queue.length',
    ):
        aggregator.assert_metric(metric, at_least=1)
