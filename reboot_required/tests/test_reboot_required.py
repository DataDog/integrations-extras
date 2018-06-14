from datadog_checks.reboot_required import RebootRequiredCheck
from os import utime, remove
from os.path import join, isfile
from tempfile import gettempdir
from datetime import datetime, timedelta
from time import mktime
import pytest

from .common import (
    CONFIG_STATUS_OK,
    CONFIG_STATUS_NP_OK,
    CONFIG_STATUS_WARNING,
    CONFIG_STATUS_CRITICAL
)

reboot_required = RebootRequiredCheck('reboot_required', {}, {})


@pytest.fixture()
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator


def setup_module():
    temp_dir = gettempdir()
    now = datetime.utcnow()

    nine_days_ago = mktime((now - timedelta(days=9)).timetuple())
    sixteen_days_ago = mktime((now - timedelta(days=16)).timetuple())

    open(join(temp_dir, 'reboot-required.freshly_minted'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.freshly_minted'), 'a').close()

    open(join(temp_dir, 'reboot-required.warning'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.warning'), 'a').close()

    utime(join(temp_dir, 'reboot-required.created_at.warning'), (nine_days_ago, nine_days_ago))

    open(join(temp_dir, 'reboot-required.critical'), 'a').close()
    open(join(temp_dir, 'reboot-required.created_at.critical'), 'a').close()

    utime(join(temp_dir, 'reboot-required.created_at.critical'), (sixteen_days_ago, sixteen_days_ago))


def teardown_module():
    temp_dir = gettempdir()
    remove(join(temp_dir, 'reboot-required.freshly_minted'))
    remove(join(temp_dir, 'reboot-required.created_at.freshly_minted'))
    remove(join(temp_dir, 'reboot-required.warning'))
    remove(join(temp_dir, 'reboot-required.created_at.warning'))
    remove(join(temp_dir, 'reboot-required.critical'))
    remove(join(temp_dir, 'reboot-required.created_at.critical'))


def test_check_ok(aggregator):
    reboot_required.check(CONFIG_STATUS_OK)
    aggregator.assert_service_check('system.reboot_required', status=reboot_required.OK)
    assert(isfile(join(gettempdir(), 'reboot-required.created_at.freshly_minted')))


def test_check_np_ok(aggregator):
    reboot_required.check(CONFIG_STATUS_NP_OK)
    aggregator.assert_service_check('system.reboot_required', status=reboot_required.OK)
    assert(not isfile(join(gettempdir(), 'reboot-required.created_at.should_not_be_present')))


def test_check_warning(aggregator):
    reboot_required.check(CONFIG_STATUS_WARNING)
    aggregator.assert_service_check('system.reboot_required', status=reboot_required.WARNING)


def test_check_critical(aggregator):
    reboot_required.check(CONFIG_STATUS_CRITICAL)
    aggregator.assert_service_check('system.reboot_required', status=reboot_required.CRITICAL)
