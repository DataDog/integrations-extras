import os

import mock
import pytest

from datadog_checks.dev import get_here
from datadog_checks.exim import EximCheck

SUBPROCESS_OUTPUT = 'datadog_checks.exim.check.get_subprocess_output'


def fixture(name):
    with open(os.path.join(get_here(), 'fixtures', name), 'r') as f:
        return f.read()


def script_of(instance):
    return EximCheck('exim', {}, [instance])._build_command()[2]


@pytest.mark.unit
def test_all_features_enabled_by_default():
    script = script_of({})
    assert '/usr/sbin/exiqsumm -f' in script
    assert '/usr/sbin/exiqsumm -b' in script
    assert script.count('/usr/sbin/exiqsumm') == 3


@pytest.mark.unit
def test_disabling_frozen_count_drops_the_f_pass(dd_run_check, aggregator):
    script = script_of({'collect_frozen_count': False})
    assert 'exiqsumm -f' not in script and '/usr/sbin/exiqsumm -b' in script

    check = EximCheck('exim', {}, [{'collect_frozen_count': False}])
    # Output as the shortened script would produce it: plain and -b summaries only.
    output = fixture('exiqsumm-separated.txt').split('@@exiqsumm-f@@\n')[0]
    output += '@@exiqsumm-b@@\n' + fixture('exiqsumm-separated.txt').split('@@exiqsumm-b@@\n')[1]
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(output, '', 0)):
        dd_run_check(check)
    aggregator.assert_metric('exim.queue.frozen.count', count=0)
    aggregator.assert_metric('exim.queue.bounce.count', value=1, tags=['domain:TOTAL'])
    aggregator.assert_metric('exim.queue.count', value=7, tags=['domain:TOTAL'])


@pytest.mark.unit
def test_disabling_bounce_count_drops_the_b_pass(dd_run_check, aggregator):
    script = script_of({'collect_bounce_count': False})
    assert 'exiqsumm -b' not in script and '/usr/sbin/exiqsumm -f' in script

    check = EximCheck('exim', {}, [{'collect_bounce_count': False}])
    output = fixture('exiqsumm-separated.txt').split('@@exiqsumm-b@@\n')[0]
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(output, '', 0)):
        dd_run_check(check)
    aggregator.assert_metric('exim.queue.bounce.count', count=0)
    aggregator.assert_metric('exim.queue.frozen.count', value=4, tags=['domain:TOTAL'])


@pytest.mark.unit
def test_disabling_both_separated_counts_runs_exiqsumm_once(dd_run_check, aggregator):
    instance = {'collect_frozen_count': False, 'collect_bounce_count': False}
    assert script_of(instance).count('/usr/sbin/exiqsumm') == 1

    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm.txt'), '', 0)):
        dd_run_check(check)
    aggregator.assert_metric('exim.queue.frozen.count', count=0)
    aggregator.assert_metric('exim.queue.bounce.count', count=0)
    aggregator.assert_metric('exim.queue.count', value=3, tags=['domain:TOTAL'])
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
@pytest.mark.parametrize(
    'instance', [{'collect_domain_metrics': False}, {'collect_domain_metrics': False, 'max_domains': 1}]
)
def test_disabling_domain_metrics_keeps_only_total(dd_run_check, aggregator, instance):
    check = EximCheck('exim', {}, [instance])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-separated.txt'), '', 0)):
        dd_run_check(check)
    for name, value in (
        ('exim.queue.count', 7),
        ('exim.queue.volume', 2511 * 1024),
        ('exim.queue.oldest_age', 100 * 86400),
        ('exim.queue.frozen.count', 4),
        ('exim.queue.bounce.count', 1),
    ):
        aggregator.assert_metric(name, value=value, tags=['domain:TOTAL'])
        aggregator.assert_metric(name, count=1)
    aggregator.assert_metric('exim.queue.domains', value=4, tags=[])
    aggregator.assert_all_metrics_covered()
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)


@pytest.mark.unit
def test_disabling_oldest_age(dd_run_check, aggregator):
    check = EximCheck('exim', {}, [{'collect_oldest_age': False}])
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-separated.txt'), '', 0)):
        dd_run_check(check)
    aggregator.assert_metric('exim.queue.oldest_age', count=0)
    aggregator.assert_metric('exim.queue.count', value=7, tags=['domain:TOTAL'])


@pytest.mark.unit
def test_disabling_service_running_submits_no_service_check(dd_run_check, aggregator):
    check = EximCheck('exim', {}, [{'collect_service_running': False}])
    with (
        mock.patch('datadog_checks.exim.check.shutil.which', return_value='/usr/bin/systemctl'),
        mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-separated.txt'), '', 0)) as subprocess_output,
    ):
        dd_run_check(check)
    aggregator.assert_service_check('exim.service.running', count=0)
    aggregator.assert_service_check('exim.returns.output', EximCheck.OK)
    assert all('systemctl' not in c.args[0][0] for c in subprocess_output.call_args_list)


@pytest.mark.unit
def test_disabling_version_metadata_skips_exim_bv(dd_run_check, datadog_agent, no_version):
    check = EximCheck('exim', {}, [{'collect_version_metadata': False}])
    check.check_id = 'test:123'
    with mock.patch(SUBPROCESS_OUTPUT, return_value=(fixture('exiqsumm-separated.txt'), '', 0)) as subprocess_output:
        dd_run_check(check)
    datadog_agent.assert_metadata_count(0)
    assert all(c.args[0][-1] != '-bV' for c in subprocess_output.call_args_list)


@pytest.fixture
def no_version():
    # Override the autouse fixture from conftest.py so the real _collect_version would run if called.
    yield
