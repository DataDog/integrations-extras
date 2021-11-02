import os

import mock
import pytest

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.unbound import UnboundCheck


def test_nonexistent_unbound_control():
    check = UnboundCheck('unbound', {}, {})
    with mock.patch('datadog_checks.unbound.unbound.which', return_value=None):
        with pytest.raises(ConfigurationError, match='executable not found: .*'):
            check.check({})


def test_no_sudo(mock_which):
    check = UnboundCheck('unbound', {}, {})
    with mock.patch('datadog_checks.unbound.unbound.os.system', return_value=1):
        with pytest.raises(Exception, match='.* does not have sudo access'):
            check.check({'use_sudo': True})


def test_unbound_on_root_path_but_not_current_users_path(aggregator, env_setup):
    check = UnboundCheck('unbound', {}, {})

    # Simulate success with the setsid sudo check, and output from unbound-control.  This
    # test focuses on sudo which can work even when setsid sudo doesn't.
    #
    # Unfortunately on some systems sudo may require entering a password...
    with mock.patch('datadog_checks.unbound.unbound.os.system', return_value=0):
        with mock.patch('datadog_checks.unbound.UnboundCheck.call_unbound_control', return_value='foo=0'):
            # env_setup removes paths with sbin from the PATH for the current user, so use
            # a program in e.g. /sbin for sudo.  Note that unbound-control is not
            # necessarily (and probably not) installed in the test environment, so use
            # something that is.
            sudo_only_executable = '/sbin/ifconfig'
            assert os.path.isfile(sudo_only_executable)

            check.check({'use_sudo': True, 'unbound_control': sudo_only_executable})

    # Ignore the actual metrics...Consider the test successful if we see an ok service
    # check
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)


def test_nonexistent_unbound_control_with_sudo(aggregator):
    check = UnboundCheck('unbound', {}, {})

    # Choose an unbound_control executable that doesn't exist under sudo.
    non_existent_executable = '/this/does/not/exist'
    # This makes sure it doesn't exist at all, which is stronger, but helps home in on
    # errors in the test vs. errors in the code.
    assert not os.path.isfile(non_existent_executable)

    # Simulate success with the setsid sudo check.  This test focuses on sudo which can
    # work even when setsid sudo doesn't.
    #
    # Unfortunately on some systems sudo may require entering a password...
    with mock.patch('datadog_checks.unbound.unbound.os.system', return_value=0):
        with pytest.raises(ConfigurationError, match='executable not found: .*'):
            check.check({'use_sudo': True, 'unbound_control': non_existent_executable})


def test_unbound_control_exception(aggregator, mock_which):
    check = UnboundCheck('unbound', {}, {})
    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output') as mock_unbound:
        message = 'arbitrary exception'
        mock_unbound.side_effect = Exception(message)
        with pytest.raises(Exception, match='Unable to get unbound stats: {}'.format(message)):
            check.check({})
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.CRITICAL)


def test_unbound_control_non_zero_return_code(aggregator, mock_which):
    check = UnboundCheck('unbound', {}, {})
    return_code = 1
    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=('', '', return_code)):
        with pytest.raises(Exception, match='failed, return code: {}'.format(return_code)):
            check.check({})
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.CRITICAL)


def test_unbound_control_empty_output(aggregator, mock_which):
    check = UnboundCheck('unbound', {}, {})
    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=('', '', 0)):
        with pytest.raises(Exception, match='no output from .*'):
            check.check({})
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.CRITICAL)


def test_wacky_output(aggregator, mock_which):
    check = UnboundCheck('unbound', {}, {})
    output = 'foo'
    with mock.patch('datadog_checks.unbound.unbound.get_subprocess_output', return_value=(output, '', 0)):
        with pytest.raises(Exception, match="unable to parse output '{}'".format(output)):
            check.check({})
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.CRITICAL)


def test_basic_stats_1_4_22(aggregator, mock_which, mock_basic_stats_1_4_22):
    check = UnboundCheck('unbound', {}, {})
    tags = ['foo:bar']
    check.check({'tags': tags})

    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)
    assert_basic_stats_1_4_22(aggregator, tags)
    aggregator.assert_all_metrics_covered()


def test_basic_stats_1_9_2(aggregator, mock_which, mock_basic_stats_1_9_2):
    check = UnboundCheck('unbound', {}, {})
    tags = ['foo:bar']
    check.check({'tags': tags})

    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)
    assert_basic_stats_1_9_2(aggregator, tags)
    aggregator.assert_all_metrics_covered()


def test_multithread_stats(aggregator, mock_which, mock_multithread_stats):
    check = UnboundCheck('unbound', {}, {})
    tags = ['foo:bar']
    check.check({'tags': tags})

    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)
    assert_multithread_stats(aggregator, tags)
    aggregator.assert_all_metrics_covered()


def test_extended_stats_1_4_22(aggregator, mock_which, mock_extended_stats_1_4_22):
    check = UnboundCheck('unbound', {}, {})
    tags = ['foo:bar']
    check.check({'tags': tags})

    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)
    assert_extended_stats_1_4_22(aggregator, tags)
    aggregator.assert_all_metrics_covered()


def test_extended_stats_1_9_2(aggregator, mock_which, mock_extended_stats_1_9_2):
    check = UnboundCheck('unbound', {}, {})
    tags = ['foo:bar']
    check.check({'tags': tags})

    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)
    assert_extended_stats_1_9_2(aggregator, tags)
    aggregator.assert_all_metrics_covered()


def test_hostname_with_port(aggregator, mock_which, mock_basic_stats_1_4_22):
    instance = {"host": "localhost@53"}
    check = UnboundCheck('unbound', {}, [instance])
    check.check(instance)
    # Ignore the actual metrics...Consider the test successful if we see an ok service
    # check
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)


def test_hostname_without_port(aggregator, mock_which, mock_basic_stats_1_4_22):
    instance = {"host": "localhost"}
    check = UnboundCheck('unbound', {}, [instance])
    check.check(instance)
    # Ignore the actual metrics...Consider the test successful if we see an ok service
    # check
    aggregator.assert_service_check(UnboundCheck.SERVICE_CHECK_NAME, status=AgentCheck.OK)


def assert_basic_stats_1_9_2(aggregator, tags):
    thread0_tags = tags + ['thread:0']
    aggregator.assert_metric(
        'unbound.thread.num.queries', value=1, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.queries_ip_ratelimited',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss', value=1, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.zero_ttl', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=1,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0.275972,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.tcpusage', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )

    thread1_tags = tags + ['thread:1']
    aggregator.assert_metric(
        'unbound.thread.num.queries', value=1, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.queries_ip_ratelimited',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits', value=1, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.zero_ttl', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.tcpusage', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )

    thread2_tags = tags + ['thread:2']
    aggregator.assert_metric(
        'unbound.thread.num.queries', value=1, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.queries_ip_ratelimited',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits', value=1, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.zero_ttl', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.tcpusage', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )

    aggregator.assert_metric(
        'unbound.total.num.queries', value=3, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.queries_ip_ratelimited',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.total.num.cachehits', value=2, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.cachemiss', value=1, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.prefetch', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.zero_ttl', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.recursivereplies', value=1, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.avg', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.max', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.overwritten',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.exceeded', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.all',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.user',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.avg',
        value=0.275972,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.median', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.tcpusage', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.now', value=1561493959.739239, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.up', value=18.262188, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.elapsed', value=18.262188, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )


def assert_basic_stats_1_4_22(aggregator, tags):
    # Rather than write code to parse stats.basic and wrestle with potential
    # bugs there, let's manually craft the assertions.  I don't expect
    # stats.basic to change very often.
    thread_tags = tags + ['thread:0']
    aggregator.assert_metric(
        'unbound.thread.num.queries',
        value=178275254,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits',
        value=166270813,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss',
        value=12004441,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=12004441,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0.395844,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=9,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0.010833,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0.00169968,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.num.queries', value=178275254, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.cachehits', value=166270813, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.cachemiss', value=12004441, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.prefetch', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.recursivereplies',
        value=12004441,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.avg', value=0.395844, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.max', value=9, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.overwritten',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.exceeded', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.all',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.user',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.avg',
        value=0.010833,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.median',
        value=0.00169968,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.time.now', value=1558048773.969199, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.up', value=49144398.166967, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.elapsed', value=2082502.474876, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )


def assert_multithread_stats(aggregator, tags):
    thread_tags = tags + ['thread:11']
    aggregator.assert_metric(
        'unbound.thread.num.queries',
        value=178275254,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits',
        value=166270813,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss',
        value=12004441,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=12004441,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0.395844,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=9,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0.010833,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0.00169968,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )


def assert_extended_stats_1_4_22(aggregator, tags):
    thread_tags = tags + ['thread:0']
    aggregator.assert_metric(
        'unbound.thread.num.queries',
        value=204240518,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits',
        value=190406406,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss',
        value=13834112,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=13834112,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0.272588,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=14,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0.005766,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0.00165754,
        tags=thread_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.num.queries', value=204240518, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.cachehits', value=190406406, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.cachemiss', value=13834112, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.prefetch', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.recursivereplies',
        value=13834112,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.avg', value=0.272588, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.max', value=14, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.overwritten',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.exceeded', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.all',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.user',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.avg',
        value=0.005766,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.median',
        value=0.00165754,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.time.now', value=1558634276.538588, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.up', value=56320542.076365, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.elapsed', value=56320542.076365, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    # extended stats start here
    aggregator.assert_metric(
        'unbound.mem.total.sbrk', value=10919936, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.cache.rrset', value=249585, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.cache.message', value=618825, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.mod.iterator', value=16532, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.mod.validator', value=66344, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.num.query.type',
        value=63589866,
        tags=tags + ['query_type:A'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.type',
        value=30,
        tags=tags + ['query_type:CNAME'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.type',
        value=2436,
        tags=tags + ['query_type:PTR'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.type',
        value=133376595,
        tags=tags + ['query_type:AAAA'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.type',
        value=7271591,
        tags=tags + ['query_type:SRV'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.class',
        value=204240518,
        tags=tags + ['query_class:IN'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.opcode',
        value=204240518,
        tags=tags + ['opcode:QUERY'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.tcp', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.ipv6', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:QR'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:AA'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:TC'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=204240518,
        tags=tags + ['flag:RD'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:RA'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags', value=0, tags=tags + ['flag:Z'], count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:AD'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:CD'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.edns.present', value=187, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.edns.DO', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=112675648,
        tags=tags + ['rcode:NOERROR'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=18863,
        tags=tags + ['rcode:SERVFAIL'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=91546007,
        tags=tags + ['rcode:NXDOMAIN'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode.nodata',
        value=48630830,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.secure', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.answer.bogus', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.rrset.bogus', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.unwanted.queries', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.unwanted.replies', value=5, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )


def assert_extended_stats_1_9_2(aggregator, tags):
    thread0_tags = tags + ['thread:0']
    aggregator.assert_metric(
        'unbound.thread.num.queries', value=3, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.queries_ip_ratelimited',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits', value=3, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.zero_ttl', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0,
        tags=thread0_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.tcpusage', value=0, tags=thread0_tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )

    thread1_tags = tags + ['thread:1']
    aggregator.assert_metric(
        'unbound.thread.num.queries', value=1, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss', value=1, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.zero_ttl', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=1,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0.416939,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0,
        tags=thread1_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.tcpusage', value=0, tags=thread1_tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )

    thread2_tags = tags + ['thread:2']
    aggregator.assert_metric(
        'unbound.thread.num.queries', value=1, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachehits', value=1, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.cachemiss', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.prefetch', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.zero_ttl', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.thread.num.recursivereplies',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.avg',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.max',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.overwritten',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.exceeded',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.all',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.requestlist.current.user',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.avg',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.recursion.time.median',
        value=0,
        tags=thread2_tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.thread.tcpusage', value=0, tags=thread2_tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )

    aggregator.assert_metric(
        'unbound.total.num.queries', value=5, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.queries_ip_ratelimited',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.total.num.cachehits', value=4, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.cachemiss', value=1, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.prefetch', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.zero_ttl', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.num.recursivereplies', value=1, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.avg', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.max', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.overwritten',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.exceeded', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.all',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.requestlist.current.user',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.avg',
        value=0.416939,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.GAUGE,
    )
    aggregator.assert_metric(
        'unbound.total.recursion.time.median', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.total.tcpusage', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.now', value=1561494094.953120, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.up', value=26.067263, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.time.elapsed', value=26.067263, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    # extended stats start here
    aggregator.assert_metric(
        'unbound.mem.cache.rrset', value=71423, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.cache.message', value=67845, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.mod.iterator', value=16588, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.mod.validator', value=69288, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.mod.respip', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.mem.streamwait', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.GAUGE
    )
    aggregator.assert_metric(
        'unbound.num.query.type',
        value=5,
        tags=tags + ['query_type:A'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.class',
        value=5,
        tags=tags + ['query_class:IN'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.opcode',
        value=5,
        tags=tags + ['opcode:QUERY'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.tcp', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.tcpout', value=7, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.tls', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.tls.resume', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.ipv6', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:QR'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:AA'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:TC'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=5,
        tags=tags + ['flag:RD'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:RA'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags', value=0, tags=tags + ['flag:Z'], count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:AD'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.flags',
        value=0,
        tags=tags + ['flag:CD'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.edns.present', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.edns.DO', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=5,
        tags=tags + ['rcode:NOERROR'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=0,
        tags=tags + ['rcode:FORMERR'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=0,
        tags=tags + ['rcode:SERVFAIL'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=0,
        tags=tags + ['rcode:NXDOMAIN'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=0,
        tags=tags + ['rcode:NOTIMPL'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.answer.rcode',
        value=0,
        tags=tags + ['rcode:REFUSED'],
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.num.query.ratelimited', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.answer.secure', value=5, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.answer.bogus', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.rrset.bogus', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.aggressive.NOERROR', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.aggressive.NXDOMAIN',
        value=0,
        tags=tags,
        count=1,
        hostname=None,
        metric_type=aggregator.COUNT,
    )
    aggregator.assert_metric(
        'unbound.unwanted.queries', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.unwanted.replies', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.msg.cache.count', value=7, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.rrset.cache.count', value=8, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.infra.cache.count', value=3, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.key.cache.count', value=3, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.authzone.up', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
    aggregator.assert_metric(
        'unbound.num.query.authzone.down', value=0, tags=tags, count=1, hostname=None, metric_type=aggregator.COUNT
    )
