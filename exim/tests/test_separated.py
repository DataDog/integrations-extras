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

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'
LONG_DOMAIN = 'a' * 70 + '.example'


def fixture(name):
    with open(os.path.join(get_here(), 'fixtures', name), 'r') as f:
        return f.read()


@pytest.mark.unit
def test_check_frozen_count(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    # exiqsumm-separated.txt is the real output of the check's shell script for the `exim -bp`
    # listing in exim-bp.txt, with exiqsumm from Exim 4.96: the plain, -f and -b summaries.
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-separated.txt'), '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.frozen.count', value=2, tags=['domain:example.org'])
    aggregator.assert_metric('exim.queue.frozen.count', value=1, tags=['domain:gmail.com'])
    aggregator.assert_metric('exim.queue.frozen.count', value=0, tags=['domain:yahoo.com'])
    # exiqsumm truncates `<78 chars> (f)` to `<78 chars> (`; the count is still derived correctly.
    aggregator.assert_metric('exim.queue.frozen.count', value=1, tags=[f'domain:{LONG_DOMAIN}'])
    aggregator.assert_metric('exim.queue.frozen.count', value=4, tags=['domain:TOTAL'])
    # The `exiqsumm -f` rows do not leak into the other metrics.
    aggregator.assert_metric('exim.queue.count', value=3, tags=['domain:example.org'])
    aggregator.assert_metric('exim.queue.count', value=7, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.count', count=5)
    aggregator.assert_metric('exim.queue.frozen.count', count=5)
    # The only bounce (empty sender) is the frozen message to dave@example.org.
    aggregator.assert_metric('exim.queue.bounce.count', value=1, tags=['domain:example.org'])
    aggregator.assert_metric('exim.queue.bounce.count', value=0, tags=['domain:gmail.com'])
    aggregator.assert_metric('exim.queue.bounce.count', value=0, tags=['domain:yahoo.com'])
    aggregator.assert_metric('exim.queue.bounce.count', value=0, tags=[f'domain:{LONG_DOMAIN}'])
    aggregator.assert_metric('exim.queue.bounce.count', value=1, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.bounce.count', count=5)
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_check_frozen_count_empty_queue(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    empty = fixture('exiqsumm-empty.txt')
    output = empty + '@@exiqsumm-f@@\n' + empty + '@@exiqsumm-b@@\n' + empty
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(output, '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.frozen.count', value=0, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.frozen.count', count=1)
    aggregator.assert_metric('exim.queue.bounce.count', value=0, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.bounce.count', count=1)


@pytest.mark.unit
def test_check_frozen_count_skipped_without_frozen_summary(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm.txt'), '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.frozen.count', count=0)
    aggregator.assert_metric('exim.queue.bounce.count', count=0)
    aggregator.assert_metric('exim.queue.count', value=3, tags=['domain:TOTAL'])
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_get_queue_summaries_parses_frozen_rows(dd_run_check):
    check = EximCheck('exim', {}, [{}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-separated.txt'), '', 0)):
        queues, separated = check._get_queue_summaries()

    assert [q.Domain for q in queues] == [LONG_DOMAIN, 'example.org', 'gmail.com', 'yahoo.com', 'TOTAL']
    assert sorted(separated) == ['bounce', 'frozen']
    assert [(q.Count, q.Domain) for q in separated['bounce']] == [
        ('1', LONG_DOMAIN),
        ('2', 'example.org'),
        ('1', 'example.org (b)'),
        ('2', 'gmail.com'),
        ('1', 'yahoo.com'),
        ('7', 'TOTAL'),
    ]
    assert [(q.Count, q.Domain) for q in separated['frozen']] == [
        ('1', LONG_DOMAIN + ' ('),
        ('1', 'example.org'),
        ('2', 'example.org (f)'),
        ('1', 'gmail.com'),
        ('1', 'gmail.com (f)'),
        ('1', 'yahoo.com'),
        ('7', 'TOTAL'),
    ]


@pytest.mark.unit
def test_frozen_count_for_domains_longer_than_78_characters(dd_run_check):
    # Beyond 78 characters exiqsumm truncates `<domain> (f)` to the same text as `<domain>`,
    # so both rows share a key: the frozen count is then too low, but never negative.
    check = EximCheck('exim', {}, [{}])
    queue = namedtuple('Queue', ["Count", "Volume", "Oldest", "Newest", "Domain"])
    domain = 'b' * 80
    queues = [queue('3', '0', '1m', '1m', domain), queue('3', '0', '1m', '1m', 'TOTAL')]
    frozen = [
        queue('1', '0', '1m', '1m', domain),
        queue('2', '0', '1m', '1m', domain),
        queue('3', '0', '1m', '1m', 'TOTAL'),
    ]
    assert check._get_separated_counts(queues, frozen, 'frozen') == {domain: 0, 'TOTAL': 0}
