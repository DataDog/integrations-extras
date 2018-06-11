from datadog_checks.reboot_required import RebootRequiredCheck
from os import utime, remove
from os.path import join, isfile
from tempfile import gettempdir
from datetime import datetime, timedelta
from time import mktime
# import pytest


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


reboot_required = RebootRequiredCheck('reboot_required',{},{})

@pytest.fixture(autouse=True)
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator


def setup_module():
    temp_dir = gettempdir()
    now = datetime.utcnow()

    eight_days_ago = mktime((now - timedelta(days=8)).timetuple())
    fifteen_days_ago = mktime((now - timedelta(days=15)).timetuple())

    open(join(temp_dir, 'reboot-required.freshly_minted'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.freshly_minted'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.should_not_be_present'), 'a').close()

    open(join(temp_dir, 'reboot-required.warning'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.warning'), 'a').close()

    utime(join(temp_dir, 'reboot-required.created_at.warning'), (eight_days_ago, eight_days_ago))

    open(join(temp_dir, 'reboot-required.critical'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.critical'), 'a').close()

    utime(join(temp_dir, 'reboot-required.created_at.critical'), (fifteen_days_ago, fifteen_days_ago))


def teardown_module():
    temp_dir = gettempdir()
    remove(join(temp_dir, 'reboot-required.freshly_minted'))
    remove(join(temp_dir, 'reboot-required.created_at.freshly_minted'))
    remove(join(temp_dir, 'reboot-required.created_at.should_not_be_present'))
    remove(join(temp_dir, 'reboot-required.warning'))
    remove(join(temp_dir, 'reboot-required.created_at.warning'))
    remove(join(temp_dir, 'reboot-required.critical'))
    remove(join(temp_dir, 'reboot-required.created_at.critical'))


def test_check_ok(self):
    reboot_required.check(CONFIG_STATUS_OK)
    aggregator.assert_service_check('system.reboot_required',status=reboot_required.OK)
    assert(isfile(join(gettempdir(), 'reboot-required.created_at.freshly_minted')))


def test_test():
    assert True is True
