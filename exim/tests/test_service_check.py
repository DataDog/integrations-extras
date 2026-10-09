from typing import Any, Callable, Dict  # noqa: F401

import mock
import pytest

from datadog_checks.base import AgentCheck  # noqa: F401
from datadog_checks.base.stubs.aggregator import AggregatorStub  # noqa: F401
from datadog_checks.dev.utils import get_service_checks
from datadog_checks.exim import EximCheck

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'
WHICH = 'datadog_checks.exim.check.shutil.which'
SYSTEMCTL = '/usr/bin/systemctl'
SERVICE_CHECK = 'exim.service.running'

EXIQSUMM_EMPTY = """
Count  Volume  Oldest  Newest  Domain
-----  ------  ------  ------  ------

---------------------------------------------------------------
    0       0      0m   0000d  TOTAL
"""


def systemctl_show(load_state, active_state):
    return 'LoadState={}\nActiveState={}\n'.format(load_state, active_state), '', 0


def fake_subprocess(units):
    """
    Return a get_subprocess_output replacement: `units` maps a unit name to the
    (stdout, stderr, returncode) of `systemctl show`; unknown units are not-found.
    """

    def run(command, log, raise_on_empty_output=True):
        if command[0] == '/bin/sh':
            return EXIQSUMM_EMPTY, '', 0
        assert command[:4] == [SYSTEMCTL, 'show', '-p', 'LoadState,ActiveState']
        return units.get(command[4], systemctl_show('not-found', 'inactive'))

    return run


def systemctl_calls(subprocess_output):
    return [c.args[0][4] for c in subprocess_output.call_args_list if c.args[0][0] == SYSTEMCTL]


@pytest.mark.unit
@pytest.mark.parametrize(
    'units, expected_status, expected_message, expected_calls',
    [
        pytest.param({'exim4': systemctl_show('loaded', 'active')}, EximCheck.OK, None, ['exim4'], id='exim4_active'),
        pytest.param(
            {'exim': systemctl_show('loaded', 'active')}, EximCheck.OK, None, ['exim4', 'exim'], id='exim_active'
        ),
        pytest.param(
            {'exim4': systemctl_show('loaded', 'inactive')},
            EximCheck.CRITICAL,
            'Exim unit `exim4` is inactive \\(LoadState=loaded\\)',
            ['exim4'],
            id='exim4_inactive',
        ),
        pytest.param(
            {'exim': systemctl_show('loaded', 'failed')},
            EximCheck.CRITICAL,
            'Exim unit `exim` is failed',
            ['exim4', 'exim'],
            id='exim_failed',
        ),
        pytest.param(
            {'exim4': systemctl_show('masked', 'inactive')},
            EximCheck.CRITICAL,
            'is inactive \\(LoadState=masked\\)',
            ['exim4'],
            id='exim4_masked',
        ),
        pytest.param(
            {},
            EximCheck.UNKNOWN,
            'No Exim systemd unit found \\(tried: exim4, exim\\)',
            ['exim4', 'exim'],
            id='no_unit_found',
        ),
    ],
)
def test_service_running_probes_default_units(
    dd_run_check, aggregator, instance, units, expected_status, expected_message, expected_calls
):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any], Any, int, Any, Any) -> None
    check = EximCheck('exim', {}, [instance])
    with (
        mock.patch(WHICH, return_value=SYSTEMCTL),
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess(units)) as subprocess_output,
    ):
        dd_run_check(check)

    aggregator.assert_service_check(SERVICE_CHECK, expected_status, count=1, message=expected_message)
    assert systemctl_calls(subprocess_output) == expected_calls


@pytest.mark.unit
@pytest.mark.parametrize(
    'state, expected_status',
    [
        pytest.param(systemctl_show('loaded', 'active'), EximCheck.OK, id='active'),
        pytest.param(systemctl_show('loaded', 'activating'), EximCheck.CRITICAL, id='activating'),
        pytest.param(systemctl_show('not-found', 'inactive'), EximCheck.UNKNOWN, id='not_found'),
    ],
)
def test_service_running_uses_configured_service_name(dd_run_check, aggregator, state, expected_status):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Any, int) -> None
    check = EximCheck('exim', {}, [{'service_name': 'exim-custom'}])
    with (
        mock.patch(WHICH, return_value=SYSTEMCTL),
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess({'exim-custom': state})) as subprocess_output,
    ):
        dd_run_check(check)

    aggregator.assert_service_check(SERVICE_CHECK, expected_status, count=1)
    assert systemctl_calls(subprocess_output) == ['exim-custom']


@pytest.mark.unit
def test_service_running_unknown_without_systemctl(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with (
        mock.patch(WHICH, return_value=None),
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess({})) as subprocess_output,
    ):
        dd_run_check(check)

    aggregator.assert_service_check(SERVICE_CHECK, EximCheck.UNKNOWN, count=1, message='systemctl` was not found')
    assert systemctl_calls(subprocess_output) == []
    # Queue collection is unaffected.
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)
    aggregator.assert_metric('exim.queue.count', value=0, tags=['domain:TOTAL'])


@pytest.mark.unit
def test_service_running_unknown_when_systemctl_fails(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    error = ('', 'System has not been booted with systemd as init system (PID 1). Can\'t operate.\n', 1)
    with (
        mock.patch(WHICH, return_value=SYSTEMCTL),
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess({'exim4': error})),
    ):
        dd_run_check(check)

    aggregator.assert_service_check(
        SERVICE_CHECK, EximCheck.UNKNOWN, count=1, message='exited with status 1: System has not been booted'
    )
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_service_running_unknown_on_unexpected_output(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with (
        mock.patch(WHICH, return_value=SYSTEMCTL),
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess({'exim4': ('', '', 0)})),
    ):
        dd_run_check(check)

    aggregator.assert_service_check(SERVICE_CHECK, EximCheck.UNKNOWN, count=1, message='Unexpected output')


@pytest.mark.unit
def test_service_running_unknown_on_exception(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])

    def run(command, log, raise_on_empty_output=True):
        if command[0] == '/bin/sh':
            return EXIQSUMM_EMPTY, '', 0
        raise OSError('boom')

    with mock.patch(WHICH, return_value=SYSTEMCTL), mock.patch(SUBPROCESS_OUTPUT, side_effect=run):
        dd_run_check(check)

    aggregator.assert_service_check(
        SERVICE_CHECK, EximCheck.UNKNOWN, count=1, message='Cannot determine the state of the Exim service: boom'
    )
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)
    aggregator.assert_metric('exim.queue.count', value=0, tags=['domain:TOTAL'])


@pytest.mark.unit
def test_service_checks_metadata(dd_run_check, aggregator, instance):
    # type: (Callable[[AgentCheck, bool], None], AggregatorStub, Dict[str, Any]) -> None
    check = EximCheck('exim', {}, [instance])
    with (
        mock.patch(WHICH, return_value=SYSTEMCTL),
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess({'exim4': systemctl_show('loaded', 'active')})),
    ):
        dd_run_check(check)

    aggregator.assert_service_checks(get_service_checks())
