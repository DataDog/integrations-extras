# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import re

import mock

from datadog_checks.upsc import UpscCheck

from .common import INSTANCES


def test_load_from_config(aggregator):
    check = UpscCheck('upsc ', {}, {}, INSTANCES)
    check.update_from_config(INSTANCES[0])

    assert sorted(['ups.testStringTag'] + check.DEFAULT_STRING_TAGS) == sorted(check.string_tags)
    assert ['foo:bar'] == check.additional_tags
    assert sorted(['ups.testStringTag'] + check.DEFAULT_STRING_TAGS) == sorted(check.string_tags)
    assert sorted(['ups.ignoreme'] + check.DEFAULT_EXCLUDED_TAGS) == sorted(check.excluded)
    assert [re.compile(r'ups\.ignore\..*')] == check.excluded_re
    assert ['ignoreme'] == check.excluded_devices
    assert [re.compile(r'ignore\..*')] == check.excluded_devices_re


@mock.patch('subprocess.check_output')
def test_list_ups_devices(mock_iocall):
    check = UpscCheck('upsc ', {}, {}, INSTANCES)
    check.update_from_config(INSTANCES[0])

    mock_iocall.return_value = '\n'.join(['ignoreme', 'ignore.me.too', 'testUps'])
    assert sorted(['ignoreme', 'ignore.me.too', 'testUps']) == sorted(check.list_ups_devices())


@mock.patch('subprocess.check_output')
def test_query_ups_device(mock_iocall):
    check = UpscCheck('upsc ', {}, {}, INSTANCES)
    check.update_from_config(INSTANCES[0])
    mock_iocall.return_value = '\n'.join(['ups.status: OL', 'battery.charge: 100'])
    assert {'ups.status': 'OL', 'battery.charge': '100'} == check.query_ups_device('testUps')


def test_convert_and_filter_stats():
    check = UpscCheck('upsc ', {}, {}, INSTANCES)
    check.update_from_config(INSTANCES[0])

    test_stats = {
        'ups.status': 'OL',
        'battery.charge': '100',
        'ups.testStringTag': 'foo Bar-*/baz',
        'device.mfr': 'CPS',
        'device.model': 'OR700VAU1',
    }
    result_stats, tags = check.convert_and_filter_stats(test_stats)
    assert {'ups.status': 1.0, 'battery.charge': 100.0} == result_stats
    assert sorted(['ups.testStringTag:foo__bar_baz', 'foo:bar', 'device.mfr:cps', 'device.model:or700_vau1']) == sorted(
        tags
    )


@mock.patch('subprocess.check_output')
def test_check(mock_iocall, aggregator):
    """
    Testing Upsc check.
    """
    check = UpscCheck('upsc ', {}, {}, INSTANCES)

    # run your actual tests...
    mock_list_results = '\n'.join(['ignoreme', 'ignore.me.too', 'testUps'])
    mock_query_results = '\n'.join(
        [
            'ups.status: OL',
            'battery.charge: 100',
            'ups.testStringTag: foo Bar-*/baz',
            'ups.ignoreme: 1',
            'ups.ignore.me.too: 3',
            'device.mfr: CPS',
            'device.model: OR700VAU1',
        ]
    )

    results = [mock_list_results, mock_query_results, mock_query_results, mock_query_results, mock_query_results]

    def sequence_calls(*args, **kwargs):
        return results.pop(0)

    mock_iocall.side_effect = sequence_calls

    check.check(INSTANCES[0])

    test_tags = ['foo:bar', 'ups.testStringTag:foo__bar_baz', 'device.mfr:cps', 'device.model:or700_vau1']

    test_cases = (('battery.charge', 1, 100.0), ('ups.status', 1, 1.0))

    for name, count, value in test_cases:
        aggregator.assert_metric('upsc.{}'.format(name), count=count, value=value, tags=test_tags)

    aggregator.assert_all_metrics_covered()
