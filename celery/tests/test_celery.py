# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest
from datadog_checks.base import AgentCheck, ConfigurationError  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401

# from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.celery import CeleryCheck


# def test_check(dd_run_check, aggregator, instance):
#     # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#     check = CeleryCheck('celery', {}, [instance])
#     dd_run_check(check)
#
#     aggregator.assert_all_metrics_covered()
#     aggregator.assert_metrics_using_metadata(get_metadata_metrics())
#
#
# def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
#     # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
#     check = CeleryCheck('celery', {}, [instance])
#     dd_run_check(check)
#     aggregator.assert_service_check('celery.can_connect', CeleryCheck.CRITICAL)


@pytest.mark.unit
def test_config():
    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{}])

    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{"app": "test"}])

    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{"broker": "redis://redis:6379"}])

    CeleryCheck('celery', {}, [{"app": "test", "broker": "redis://redis:6379"}])

    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{"app": "test", "broker": "redis://redis:6379", "remember_workers": 42}])

    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{"app": "test", "broker": "redis://redis:6379", "report_task_count": 42}])

    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{"app": "test", "broker": "redis://redis:6379", "report_rusage": 42}])

    with pytest.raises(ConfigurationError):
        CeleryCheck('celery', {}, [{"app": "test", "broker": "redis://redis:6379", "workers_crit_max": "fail"}])


def test__check_worker_ping(check, aggregator, worker_instance):
    check = check(worker_instance)
    app = mock.MagicMock()
    app.control.ping.return_value = [{'celery@4f8ff30e0459': {'ok': 'pong'}}]
    check._check_worker_ping(app)

    expected_tags = ["worker:celery@4f8ff30e0459", "app:tasks"]
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.OK, tags=expected_tags)


def test__check_task_metrics(check, aggregator, worker_instance):
    check = check(worker_instance)
    inspect = mock.MagicMock()
    inspect.active.return_value = {'celery@173b8997ac64': [
        {'id': '6c4dd7eb-c18c-41dd-a1d0-e77e4458f602', 'name': 'tasks.add', 'args': [1, 2], 'kwargs': {},
         'type': 'tasks.add', 'hostname': 'celery@173b8997ac64', 'time_start': 1682450302.0659862, 'acknowledged': True,
         'delivery_info': {'exchange': '', 'routing_key': 'celery', 'priority': 0, 'redelivered': None},
         'worker_pid': 14}]}
    inspect.scheduled.return_value = {'celery@173b8997ac64': []}
    inspect.reserved.return_value = {'celery@173b8997ac64': []}
    inspect.revoked.return_value = {'celery@173b8997ac64': []}

    check._check_task_metrics(inspect)

    expected_tags = ["worker:celery@173b8997ac64", "app:tasks"]
    aggregator.assert_metric('celery.worker.tasks.active', value=1, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.tasks.scheduled', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.tasks.reserved', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.tasks.revoked', value=0, count=1, tags=expected_tags)


def test__check_worker_metrics(check, aggregator, worker_instance):
    check = check(worker_instance)
    inspect = mock.MagicMock()
    inspect.stats.return_value = {
        'celery@173b8997ac64': {'total': {'tasks.add': 1}, 'pid': 1, 'clock': '770', 'uptime': 769,
                                'pool': {'max-concurrency': 8, 'processes': [7, 8, 9, 10, 11, 12, 13, 14],
                                         'max-tasks-per-child': 'N/A', 'put-guarded-by-semaphore': False,
                                         'timeouts': [0, 0],
                                         'writes': {'total': 1, 'avg': '1.00', 'all': '1.00', 'raw': '1',
                                                    'strategy': 'fair', 'inqueues': {'total': 8, 'active': 0}}},
                                'broker': {'hostname': 'redis', 'userid': None, 'virtual_host': '0', 'port': 6379,
                                           'insist': False, 'ssl': False, 'transport': 'redis', 'connect_timeout': 4,
                                           'transport_options': {}, 'login_method': None, 'uri_prefix': None,
                                           'heartbeat': 120.0, 'failover_strategy': 'round-robin', 'alternates': []},
                                'prefetch_count': 32,
                                'rusage': {'utime': 1.865402, 'stime': 0.340309, 'maxrss': 40644, 'ixrss': 0,
                                           'idrss': 0, 'isrss': 0, 'minflt': 40085, 'majflt': 0, 'nswap': 0,
                                           'inblock': 904, 'oublock': 776, 'msgsnd': 0, 'msgrcv': 0, 'nsignals': 0,
                                           'nvcsw': 2287, 'nivcsw': 57}}}

    check._check_worker_metrics(inspect)

    expected_tags = ["worker:celery@173b8997ac64", "app:tasks"]
    aggregator.assert_metric('celery.worker.uptime', value=769, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.prefetch_count', value=32, count=1, tags=expected_tags)

    aggregator.assert_metric('celery.worker.task_count', value=1, count=1, tags=expected_tags + ["task:tasks.add"])

    aggregator.assert_metric('celery.worker.rusage.utime', value=1.865402, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.stime', value=0.340309, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.maxrss', value=40644, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.ixrss', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.idrss', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.isrss', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.minflt', value=40085, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.majflt', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.nswap', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.inblock', value=904, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.oublock', value=776, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.msgsnd', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.msgrcv', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.nsignals', value=0, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.nvcsw', value=2287, count=1, tags=expected_tags)
    aggregator.assert_metric('celery.worker.rusage.nivcsw', value=57, count=1, tags=expected_tags)


def test__remembered_workers(check, aggregator, worker_instance):
    check = check(worker_instance)
    app = mock.MagicMock()
    app.control.ping.return_value = [{'celery@4f8ff30e0459': {'ok': 'pong'}}, {'celery@173b8997ac64': {'ok': 'pong'}}]
    check._check_worker_ping(app)
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.OK, count=2)

    aggregator.reset()
    app.control.ping.return_value = [{'celery@4f8ff30e0459': {'ok': 'pong'}}]
    check._check_worker_ping(app)
    ok_tags = ["worker:celery@4f8ff30e0459", "app:tasks"]
    critical_tags = ["worker:celery@173b8997ac64", "app:tasks"]
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.OK, count=1, tags=ok_tags)
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.CRITICAL, count=1, tags=critical_tags)


def test__no_remembered_workers(check, aggregator, worker_instance):
    worker_instance['remember_workers'] = False
    check = check(worker_instance)
    app = mock.MagicMock()
    app.control.ping.return_value = [{'celery@4f8ff30e0459': {'ok': 'pong'}}, {'celery@173b8997ac64': {'ok': 'pong'}}]
    check._check_worker_ping(app)
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.OK, count=2)

    aggregator.reset()
    app.control.ping.return_value = [{'celery@4f8ff30e0459': {'ok': 'pong'}}]
    check._check_worker_ping(app)
    ok_tags = ["worker:celery@4f8ff30e0459", "app:tasks"]
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.OK, count=1, tags=ok_tags)
    aggregator.assert_service_check('celery.worker.ping', CeleryCheck.CRITICAL, count=0)
