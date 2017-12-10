# vim: ts=4:sw=4:et
# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

from nose.plugins.attrib import attr
from tests.checks.common import AgentCheckTest
from os import utime, remove
from os.path import join, isfile
from tempfile import gettempdir
from datetime import datetime, timedelta
from time import mktime

CONFIG_STATUS_OK = {
    'instances': [{
        'reboot_signal_file': join(gettempdir(), 'reboot-required.freshly_minted'),
        'created_at_file': join(gettempdir(), 'reboot-required.created_at.freshly_minted'),
        'days_warning': 7,
        'days_critical': 14
    }]
}

CONFIG_STATUS_NP_OK = {
    'instances': [{
        'reboot_signal_file': join(gettempdir(), 'reboot-required.should_not_be_present'),
        'created_at_file': join(gettempdir(), 'reboot-required.created_at.should_not_be_present'),
        'days_warning': 7,
        'days_critical': 14
    }]
}

CONFIG_STATUS_WARNING = {
    'instances': [{
        'reboot_signal_file': join(gettempdir(), 'reboot-required.warning'),
        'created_at_file': join(gettempdir(), 'reboot-required.created_at.warning'),
        'days_warning': 7,
        'days_critical': 14
    }]
}

CONFIG_STATUS_CRITICAL = {
    'instances': [{
        'reboot_signal_file': join(gettempdir(), 'reboot-required.critical'),
        'created_at_file': join(gettempdir(), 'reboot-required.created_at.critical'),
        'days_warning': 7,
        'days_critical': 14
    }]
}

@attr(requires="reboot_required")
class RebootRequiredTestCase(AgentCheckTest):

    CHECK_NAME = 'reboot_required'

    @classmethod
    def setUpClass(cls):

        temp_dir = gettempdir()
        now = datetime.utcnow()

        eight_days_ago = mktime((now - timedelta(days=8)).timetuple())
        fifteen_days_ago = mktime((now - timedelta(days=15)).timetuple())

        open(join(temp_dir, 'reboot-required.freshly_minted'), 'a').close()
        open(join(temp_dir, 'reboot-required.created_at.should_not_be_present'), 'a').close()

        open(join(temp_dir, 'reboot-required.warning'), 'a').close()
        open(join(temp_dir, 'reboot-required.created_at.warning'), 'a').close()

        utime(join(temp_dir, 'reboot-required.created_at.warning'), (eight_days_ago, eight_days_ago))

        open(join(temp_dir, 'reboot-required.critical'), 'a').close()
        open(join(temp_dir, 'reboot-required.created_at.critical'), 'a').close()

        utime(join(temp_dir, 'reboot-required.created_at.critical'), (fifteen_days_ago, fifteen_days_ago))

    @classmethod
    def tearDownCls(cls):
        temp_dir = gettempdir()
        remove(join(temp_dir, 'reboot-required.freshly_minted'))
        remove(join(temp_dir, 'reboot-required.created_at.freshly_minted'))
        remove(join(temp_dir, 'reboot-required.warning'))
        remove(join(temp_dir, 'reboot-required.created_at.warning'))
        remove(join(temp_dir, 'reboot-required.critical'))
        remove(join(temp_dir, 'reboot-required.created_at.critical'))

    def test_check_ok(self):
        self.run_check(CONFIG_STATUS_OK)
        self.assertServiceCheckOK('system.reboot_required')
        self.assertTrue(isfile(join(gettempdir(), 'reboot-required.created_at.freshly_minted')))
        self.coverage_report()

    def test_check_np_ok(self):
        self.run_check(CONFIG_STATUS_NP_OK)
        self.assertServiceCheckOK('system.reboot_required')
        self.assertFalse(isfile(join(gettempdir(), 'reboot-required.created_at.should_not_be_present')))
        self.coverage_report()

    def test_check_warning(self):
        self.run_check(CONFIG_STATUS_WARNING)
        self.assertServiceCheckWarning('system.reboot_required')
        self.coverage_report()

    def test_check_critical(self):
        self.run_check(CONFIG_STATUS_CRITICAL)
        self.assertServiceCheckCritical('system.reboot_required')
        self.coverage_report()
