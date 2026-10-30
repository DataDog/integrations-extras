import mock
import pytest

from datadog_checks.exim import EximCheck

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'
EXIM_BV = """Exim version 4.97 #2 built 22-Sep-2026 18:24:17
Copyright (c) University of Cambridge, 1995 - 2018
(c) The Exim Maintainers and contributors in ACKNOWLEDGMENTS file, 2007 - 2022
Berkeley DB: Berkeley DB 5.3.28: (September  9, 2013)
"""


@pytest.fixture
def no_version():
    # Override the autouse fixture from conftest.py: these tests exercise _collect_version itself.
    yield


def fake_subprocess(bv_result):
    def run(command, log, raise_on_empty_output=True):
        if command[-1] == '-bV':
            return bv_result
        return (
            'Count  Volume  Oldest  Newest  Domain\n-----  ------  ------  ------  ------\n\n'
            '    0       0      0m   0000d  TOTAL\n',
            '',
            0,
        )

    return run


@pytest.mark.unit
@pytest.mark.parametrize(
    'bv_result, expected',
    [
        pytest.param(
            (EXIM_BV, '', 0), {'version.major': '4', 'version.minor': '97', 'version.raw': '4.97'}, id='two_parts'
        ),
        pytest.param(
            ('Exim version 4.94.2 #2 built 01-Jan-2021\n', '', 0),
            {'version.major': '4', 'version.minor': '94', 'version.patch': '2', 'version.raw': '4.94.2'},
            id='three_parts',
        ),
    ],
)
def test_version_metadata(dd_run_check, datadog_agent, bv_result, expected):
    check = EximCheck('exim', {}, [{'exim_path': '/opt/exim/bin/exim'}])
    check.check_id = 'test:123'
    with (
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess(bv_result)) as subprocess_output,
    ):
        dd_run_check(check)

    expected = dict(expected, **{'version.scheme': 'exim'})
    datadog_agent.assert_metadata('test:123', expected)
    assert [c.args[0] for c in subprocess_output.call_args_list if c.args[0][-1] == '-bV'] == [
        ['/opt/exim/bin/exim', '-bV']
    ]


@pytest.mark.unit
@pytest.mark.parametrize(
    'bv_result',
    [
        pytest.param(('', '/bin/sh: /usr/sbin/exim: not found\n', 127), id='exim_missing'),
        pytest.param(('garbage\n', '', 0), id='unexpected_output'),
        pytest.param(('', '', 0), id='empty_output'),
    ],
)
def test_version_metadata_skipped_on_failure(dd_run_check, datadog_agent, aggregator, bv_result):
    check = EximCheck('exim', {}, [{}])
    check.check_id = 'test:123'
    with (
        mock.patch(SUBPROCESS_OUTPUT, side_effect=fake_subprocess(bv_result)),
    ):
        dd_run_check(check)

    datadog_agent.assert_metadata_count(0)
    # The version lookup never affects the queue collection.
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)
