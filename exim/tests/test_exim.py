import os
from collections import namedtuple
from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.base.utils.subprocess_output import SubprocessOutputEmptyError
from datadog_checks.dev import get_here
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.exim import EximCheck

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'
DEFAULT_SCRIPT = 'out=$(/usr/sbin/exim -bp) || exit $?; printf \'%s\\n\' "$out" | /usr/sbin/exiqsumm'


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
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(exiqsumm_mock(), '', 0)):
        dd_run_check(check)

        aggregator.assert_metric('exim.queue.count', value=2, tags=tags + ['domain:gmail.com'])
        aggregator.assert_metric('exim.queue.count', value=1, tags=tags + ['domain:user@server2.in'])
        aggregator.assert_metric('exim.queue.count', value=3, tags=tags + ['domain:TOTAL'])

        aggregator.assert_metric('exim.queue.volume', value=1812.0, tags=tags + ['domain:gmail.com'])
        aggregator.assert_metric('exim.queue.volume', value=31744.0, tags=tags + ['domain:user@server2.in'])
        aggregator.assert_metric('exim.queue.volume', value=33792.0, tags=tags + ['domain:TOTAL'])

        aggregator.assert_metric('exim.queue.oldest_age', value=14 * 3600, tags=tags + ['domain:gmail.com'])
        aggregator.assert_metric('exim.queue.oldest_age', value=11 * 3600, tags=tags + ['domain:user@server2.in'])
        aggregator.assert_metric('exim.queue.oldest_age', value=14 * 3600, tags=tags + ['domain:TOTAL'])

        aggregator.assert_all_metrics_covered()
        aggregator.assert_metrics_using_metadata(get_metadata_metrics())
        aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_check_empty_queue(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(exiqsumm_empty_mock(), '', 0)):
        dd_run_check(check)

        aggregator.assert_metric('exim.queue.count', value=0, tags=['domain:TOTAL'])
        aggregator.assert_metric('exim.queue.volume', value=0, tags=['domain:TOTAL'])
        aggregator.assert_metric('exim.queue.oldest_age', value=0, tags=['domain:TOTAL'])
        aggregator.assert_all_metrics_covered()
        aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_check_runs_pipeline_through_shell(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(exiqsumm_mock(), '', 0)) as subprocess_output:
        dd_run_check(check)

    subprocess_output.assert_called_once_with(['/bin/sh', '-c', DEFAULT_SCRIPT], check.log, raise_on_empty_output=True)


@pytest.mark.unit
def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=('', '/bin/sh: 1: /usr/sbin/exim: not found', 127)):
        dd_run_check(check)
    aggregator.assert_service_check('exim.returns.output', EximCheck.CRITICAL, message='status 127: .*not found')
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
def test_emits_critical_service_check_on_nonzero_exit(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=('', 'exim: permission denied\n', 1)):
        dd_run_check(check)
    aggregator.assert_service_check(
        'exim.returns.output', EximCheck.CRITICAL, message='exited with status 1: exim: permission denied$'
    )
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
def test_emits_critical_service_check_on_empty_output(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    error = SubprocessOutputEmptyError('expected subprocess output but had none.')
    with mock.patch(SUBPROCESS_OUTPUT, side_effect=error):
        dd_run_check(check)
    aggregator.assert_service_check('exim.returns.output', EximCheck.CRITICAL, message='expected subprocess output')
    aggregator.assert_all_metrics_covered()


@pytest.mark.unit
@pytest.mark.parametrize(
    'instance, expected_script',
    [
        pytest.param({}, DEFAULT_SCRIPT, id='defaults'),
        pytest.param(
            {'exim_path': '/opt/exim/bin/exim', 'exiqsumm_path': '/opt/exim/bin/exiqsumm'},
            'out=$(/opt/exim/bin/exim -bp) || exit $?; printf \'%s\\n\' "$out" | /opt/exim/bin/exiqsumm',
            id='custom_paths',
        ),
        pytest.param(
            {'exim_path': '/opt/exim 4/exim', 'exiqsumm_path': '/opt/exim 4/exiqsumm'},
            'out=$(\'/opt/exim 4/exim\' -bp) || exit $?; printf \'%s\\n\' "$out" | \'/opt/exim 4/exiqsumm\'',
            id='paths_are_shell_quoted',
        ),
        pytest.param(
            {'use_sudo': True},
            'out=$(sudo -n /usr/sbin/exim -bp) || exit $?; printf \'%s\\n\' "$out" | /usr/sbin/exiqsumm',
            id='use_sudo',
        ),
        pytest.param({'use_sudo': False}, DEFAULT_SCRIPT, id='use_sudo_disabled'),
        pytest.param(
            {'use_sudo': True, 'exim_path': '/usr/local/sbin/exim'},
            'out=$(sudo -n /usr/local/sbin/exim -bp) || exit $?; printf \'%s\\n\' "$out" | /usr/sbin/exiqsumm',
            id='use_sudo_custom_exim_path',
        ),
    ],
)
def test_build_command(instance, expected_script):
    check = EximCheck('exim', {}, [instance])
    assert check._build_command() == ['/bin/sh', '-c', expected_script]


@pytest.mark.unit
def test_get_queue_stats(dd_run_check):
    check = EximCheck('exim', {}, [{}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(exiqsumm_mock(), '', 0)):
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
    check = EximCheck('exim', {}, [{}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(exiqsumm_empty_mock(), '', 0)):
        result = check._get_queue_stats()
        queue = namedtuple('Queue', ["Count", "Volume", "Oldest", "Newest", "Domain"])
        expected = [queue(Count='0', Volume='0', Oldest='0m', Newest='0000d', Domain='TOTAL')]

        assert result == expected


@pytest.mark.unit
def test_get_queue_stats_raises_on_nonzero_exit(dd_run_check):
    check = EximCheck('exim', {}, [{}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(exiqsumm_empty_mock(), 'sudo: a password is required\n', 1)):
        with pytest.raises(Exception, match='exited with status 1: sudo: a password is required'):
            check._get_queue_stats()


@pytest.mark.unit
@pytest.mark.parametrize(
    'size_string, expected',
    [
        ('1812', 1812),
        ('31KB', 31744),
        ('1312KB', 1343488),
        ('12MB', 12582912),
    ],
)
def test_parse_size(size_string, expected):
    assert EximCheck.parse_size(size_string) == expected
