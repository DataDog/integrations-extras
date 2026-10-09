import os
from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev import get_here
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.exim import EximCheck

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'


def fixture(name):
    with open(os.path.join(get_here(), 'fixtures', name), 'r') as f:
        return f.read()


@pytest.mark.unit
def test_check_oldest_age(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    # exiqsumm-ages.txt is the output of exiqsumm (Exim 4.96) for exim-bp.txt.
    check = EximCheck('exim', {}, [instance])
    long_domain = 'a' * 70 + '.example'
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-ages.txt'), '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.oldest_age', value=2 * 3600, tags=[f'domain:{long_domain}'])
    aggregator.assert_metric('exim.queue.oldest_age', value=4 * 86400, tags=['domain:example.org'])
    aggregator.assert_metric('exim.queue.oldest_age', value=4 * 86400, tags=['domain:gmail.com'])
    aggregator.assert_metric('exim.queue.oldest_age', value=100 * 86400, tags=['domain:yahoo.com'])
    aggregator.assert_metric('exim.queue.oldest_age', value=100 * 86400, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.count', value=7, tags=['domain:TOTAL'])
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


@pytest.mark.unit
def test_check_skips_unparseable_oldest_age(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    output = fixture('exiqsumm-empty.txt').replace('0m   0000d', '??   0000d')
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(output, '', 0)):
        dd_run_check(check)

    aggregator.assert_metric('exim.queue.count', value=0, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.oldest_age', count=0)
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
@pytest.mark.parametrize(
    'age_string, expected',
    [
        ('0m', 0),
        ('0000d', 0),
        ('5m', 300),
        ('90m', 5400),
        ('14h', 50400),
        ('4d', 345600),
        ('100d', 8640000),
        ('30s', 30),
        ('2w', 1209600),
        (' 5m', 300),
        ('', None),
        ('5', None),
        ('5y', None),
        ('abc', None),
    ],
)
def test_parse_age(age_string, expected):
    assert EximCheck.parse_age(age_string) == expected
