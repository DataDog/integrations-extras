from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.exim import EximCheck

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'
HEADER = 'Count  Volume  Oldest  Newest  Domain\n-----  ------  ------  ------  ------\n\n'
RULE = '---------------------------------------------------------------\n'


def summary(rows):
    """Render exiqsumm-like output for (count, volume, oldest, newest, domain) rows plus a TOTAL row."""
    body = ''.join(f'{c:5d}  {v:>6}  {o:>6}  {n:>6}  {d}\n' for c, v, o, n, d in rows)
    total = sum(r[0] for r in rows)
    return HEADER + body + RULE + f'{total:5d}  {"0":>6}  {"0m":>6}  {"0m":>6}  TOTAL\n\n'


# Five domains; d1 and d2 are the busiest, the rest should fold into `other` with max_domains: 2.
PLAIN = [
    (10, '10KB', '3d', '1h', 'd1.example'),
    (7, '700', '14h', '5m', 'd2.example'),
    (3, '300', '2d', '2d', 'd3.example'),
    (2, '2KB', '5h', '5h', 'd4.example'),
    (1, '100', '9m', '9m', 'd5.example'),
]
# -f summary: d3 has 2 frozen recipients, d5 has 1; -b summary: d4 has 1 bounce.
FROZEN = [
    (10, '10KB', '3d', '1h', 'd1.example'),
    (7, '700', '14h', '5m', 'd2.example'),
    (1, '100', '2d', '2d', 'd3.example'),
    (2, '200', '2d', '2d', 'd3.example (f)'),
    (2, '2KB', '5h', '5h', 'd4.example'),
    (1, '100', '9m', '9m', 'd5.example (f)'),
]
BOUNCE = [
    (10, '10KB', '3d', '1h', 'd1.example'),
    (7, '700', '14h', '5m', 'd2.example'),
    (3, '300', '2d', '2d', 'd3.example'),
    (1, '1KB', '5h', '5h', 'd4.example'),
    (1, '1KB', '5h', '5h', 'd4.example (b)'),
    (1, '100', '9m', '9m', 'd5.example'),
]
OUTPUT = summary(PLAIN) + '@@exiqsumm-f@@\n' + summary(FROZEN) + '@@exiqsumm-b@@\n' + summary(BOUNCE)


def run(dd_run_check, instance):
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(OUTPUT, '', 0)):
        dd_run_check(check)
    return check


@pytest.mark.unit
def test_domains_beyond_the_limit_are_aggregated(dd_run_check, aggregator):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub) -> None
    run(dd_run_check, {'max_domains': 2})

    aggregator.assert_metric('exim.queue.count', value=10, tags=['domain:d1.example'])
    aggregator.assert_metric('exim.queue.count', value=7, tags=['domain:d2.example'])
    # d3 + d4 + d5
    aggregator.assert_metric('exim.queue.count', value=6, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.volume', value=300 + 2048 + 100, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.oldest_age', value=2 * 86400, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.frozen.count', value=3, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.bounce.count', value=1, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.count', value=23, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.domains', value=5, tags=[])
    # Exactly d1, d2, other and TOTAL are reported.
    aggregator.assert_metric('exim.queue.count', count=4)
    aggregator.assert_metric('exim.queue.count', count=0, tags=['domain:d3.example'])
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
@pytest.mark.parametrize(
    'instance', [pytest.param({'max_domains': 0}, id='zero'), pytest.param({'max_domains': 5}, id='exact')]
)
def test_no_aggregation_when_within_the_limit(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    run(dd_run_check, instance)

    aggregator.assert_metric('exim.queue.count', count=6)
    aggregator.assert_metric('exim.queue.count', count=0, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.count', value=1, tags=['domain:d5.example'])
    aggregator.assert_metric('exim.queue.frozen.count', value=2, tags=['domain:d3.example'])
    aggregator.assert_metric('exim.queue.bounce.count', value=1, tags=['domain:d4.example'])


@pytest.mark.unit
def test_default_limit_is_100(dd_run_check, aggregator):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub) -> None
    rows = [(i, '100', '1m', '1m', f'd{i:03d}.example') for i in range(150, 0, -1)]
    output = summary(rows) + '@@exiqsumm-f@@\n' + summary(rows) + '@@exiqsumm-b@@\n' + summary(rows)
    check = EximCheck('exim', {}, [{}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(output, '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.count', count=102)  # 100 domains + other + TOTAL
    aggregator.assert_metric('exim.queue.count', value=51, tags=['domain:d051.example'])
    aggregator.assert_metric('exim.queue.count', value=sum(range(1, 51)), tags=['domain:other'])
    aggregator.assert_metric('exim.queue.domains', value=150, tags=[])


@pytest.mark.unit
def test_other_without_parseable_age(dd_run_check, aggregator):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub) -> None
    rows = [(2, '100', '1m', '1m', 'a.example'), (1, '100', '??', '1m', 'b.example')]
    output = summary(rows) + '@@exiqsumm-f@@\n' + summary(rows) + '@@exiqsumm-b@@\n' + summary(rows)
    check = EximCheck('exim', {}, [{'max_domains': 1}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(output, '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.count', value=1, tags=['domain:other'])
    aggregator.assert_metric('exim.queue.oldest_age', count=0, tags=['domain:other'])


@pytest.mark.unit
def test_negative_limit_is_rejected(dd_run_check):
    # The generated config model (`minimum: 0` in spec.yaml) rejects it before the check runs.
    check = EximCheck('exim', {}, [{'max_domains': -1}])
    with pytest.raises(Exception, match='max_domains'):
        dd_run_check(check)
