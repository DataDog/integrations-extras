import os
from collections import namedtuple
from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev import get_here
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.exim import EximCheck


def exiqsumm_mock():
    filepath = os.path.join(get_here(), 'fixtures', 'exiqsumm.txt')
    with open(filepath, 'r') as f:
        return f.read()


def exiqsumm_empty_mock():
    filepath = os.path.join(get_here(), 'fixtures', 'exiqsumm-empty.txt')
    with open(filepath, 'r') as f:
        return f.read()


@pytest.mark.unit
def test_check(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    tags = []
    with mock.patch('datadog_checks.exim.check.get_subprocess_output', return_value=(exiqsumm_mock(), '', 0)):
        dd_run_check(check)

        aggregator.assert_metric('exim.queue.count', value=2, tags=tags + ['domain:gmail.com'])
        aggregator.assert_metric('exim.queue.count', value=1, tags=tags + ['domain:user@server2.in'])
        aggregator.assert_metric('exim.queue.count', value=3, tags=tags + ['domain:TOTAL'])

        aggregator.assert_metric('exim.queue.volume', value=1812.0, tags=tags + ['domain:gmail.com'])
        aggregator.assert_metric('exim.queue.volume', value=31000.0, tags=tags + ['domain:user@server2.in'])
        aggregator.assert_metric('exim.queue.volume', value=33000.0, tags=tags + ['domain:TOTAL'])

        aggregator.assert_all_metrics_covered()
        aggregator.assert_metrics_using_metadata(get_metadata_metrics())
        aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    dd_run_check(check)
    aggregator.assert_service_check('exim.returns.output', EximCheck.CRITICAL)


@pytest.mark.unit
def test_get_queue_stats(dd_run_check):

    check = EximCheck('exim', {}, [])
    with mock.patch('datadog_checks.exim.check.get_subprocess_output', return_value=(exiqsumm_mock(), '', 0)):
        result = check._get_queue_stats()
        queue = namedtuple('Queue', ["Count", "Volume", "Oldest", "Newest", "Domain"])
        expected = [
            queue(Count='2', Volume='1812', Oldest='14h', Newest='14h', Domain='gmail.com'),
            queue(Count='1', Volume='31KB', Oldest='11h', Newest='11h', Domain='user@server2.in'),
            queue(Count='3', Volume='33KB', Oldest='14h', Newest='11h', Domain='TOTAL'),
        ]
        assert result == expected


@pytest.mark.unit
def test_get_queue_stats_empty(dd_run_check):

    check = EximCheck('exim', {}, [])
    with mock.patch('datadog_checks.exim.check.get_subprocess_output', return_value=(exiqsumm_empty_mock(), '', 0)):
        result = check._get_queue_stats()
        queue = namedtuple('Queue', ["Count", "Volume", "Oldest", "Newest", "Domain"])
        expected = [queue(Count='0', Volume='0', Oldest='0m', Newest='0000d', Domain='TOTAL')]

        assert result == expected


def test_parse_size(dd_run_check):
    check = EximCheck('exim', {}, [])
    assert check.parse_size("31KB") == 31000
    assert check.parse_size("1812") == 1812
