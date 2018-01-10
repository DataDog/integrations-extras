# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import mock
from nose.plugins.attrib import attr
import re

# 3p

# project
from tests.checks.common import AgentCheckTest
import check

instance = {
    'host': 'localhost',
    'port': 26379,
    'password': 'datadog-is-devops-best-friend'
}


@attr(requires='upsc')
class TestUpsc(AgentCheckTest):
    """Test for UPSC integration."""
    CHECK_NAME = 'upsc'
    TEST_CHECK_CONFIG = {'instances': [
        {
            'tags': ['foo:bar'],
            'string_tags': ['ups.testStringTag'],
            'excluded': ['ups.ignoreme'],
            'excluded_re': ['ups\.ignore\..*'],
            'excluded_devices': ['ignoreme'],
            'excluded_devices_re': ['ignore\..*']
        }
    ]}

    class MockUpscCheck(check.UpscCheck):
        """ Some overrides to work in CI"""

        def list_ups_devices(self):
            return ['ignoreme', 'ignore.me.too', 'testUps']

        @mock.patch('subprocess.check_output')
        def query_ups_device(self, name):
            return {
                'ups.status': 'OL',

            }


    @attr('config')
    def test_load_from_config(self):
        self.load_check(self.TEST_CHECK_CONFIG, {})
        self.check.update_from_config(self.TEST_CHECK_CONFIG['instances'][0])

        self.assertListEqual(['foo:bar'], self.check.additional_tags)
        self.assertListEqual(sorted(['ups.testStringTag'] + self.check.DEFAULT_STRING_TAGS),
                             sorted(self.check.string_tags))
        self.assertListEqual(sorted(['ups.ignoreme'] + self.check.DEFAULT_EXCLUDED_TAGS),
                             sorted(self.check.excluded))
        self.assertListEqual([re.compile('ups\.ignore\..*')], self.check.excluded_re)
        self.assertListEqual(['ignoreme'], self.check.excluded_devices)
        self.assertListEqual([re.compile('ignore\..*')], self.check.excluded_devices_re)

    @mock.patch('subprocess.check_output')
    def test_list_ups_devices(self, mock_iocall):
        self.load_check(self.TEST_CHECK_CONFIG, {})
        self.check.update_from_config(self.TEST_CHECK_CONFIG['instances'][0])

        mock_iocall.return_value = '\n'.join(['ignoreme', 'ignore.me.too', 'testUps'])
        self.assertListEqual(sorted(['ignoreme', 'ignore.me.too', 'testUps']),
                             sorted(self.check.list_ups_devices()))

    @mock.patch('subprocess.check_output')
    def test_query_ups_device(self, mock_iocall):
        self.load_check(self.TEST_CHECK_CONFIG, {})
        self.check.update_from_config(self.TEST_CHECK_CONFIG['instances'][0])

        mock_iocall.return_value = '\n'.join(['ups.status: OL', 'battery.charge: 100'])
        self.assertDictEqual({'ups.status': 'OL', 'battery.charge': '100'}, self.check.query_ups_device('testUps'))

    def test_convert_and_filter_stats(self):
        self.load_check(self.TEST_CHECK_CONFIG, {})
        self.check.update_from_config(self.TEST_CHECK_CONFIG['instances'][0])

        test_stats = {'ups.status': 'OL', 'battery.charge': '100', 'ups.testStringTag': 'foo Bar-*/baz',
                      'device.mfr': 'CPS', 'device.model': 'OR700VAU1'}
        result_stats, tags = self.check.convert_and_filter_stats(test_stats)
        self.assertDictEqual({'ups.status': 1.0, 'battery.charge': 100.0}, result_stats)
        self.assertListEqual(
            sorted(['ups.testStringTag:foo__bar_baz', 'foo:bar', 'device.mfr:cps', 'device.model:or700_vau1']),
            sorted(tags)
        )

    @mock.patch('subprocess.check_output')
    def test_check(self, mock_iocall):
        """
        Testing Upsc check.
        """
        self.load_check(self.TEST_CHECK_CONFIG, {})

        # run your actual tests...
        mock_list_results = '\n'.join(['ignoreme', 'ignore.me.too', 'testUps'])
        mock_query_results = '\n'.join(['ups.status: OL', 'battery.charge: 100', 'ups.testStringTag: foo Bar-*/baz',
                                        'ups.ignoreme: 1', 'ups.ignore.me.too: 3', 'device.mfr: CPS',
                                        'device.model: OR700VAU1'])

        results = [
            mock_list_results, mock_query_results, mock_query_results, mock_query_results, mock_query_results
        ]

        def sequence_calls(*args, **kwargs):
            return results.pop(0)

        mock_iocall.side_effect = sequence_calls

        self.run_check(self.TEST_CHECK_CONFIG['instances'][0])

        test_tags = ['foo:bar', 'ups.testStringTag:foo__bar_baz', 'device.mfr:cps', 'device.model:or700_vau1']

        test_cases = (
            ('battery.charge', 1, 100.0),
            ('ups.status', 1, 1.0),
        )

        for name, count, value in test_cases:
            self.assertMetric(
                'upsc.{}'.format(name),
                count=count,
                value=value,
                tags=test_tags
            )

        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
