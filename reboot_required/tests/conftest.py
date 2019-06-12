# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from os.path import join

import pytest

from datadog_checks.dev import TempDir
from datadog_checks.reboot_required import RebootRequiredCheck

from .common import NINE_DAYS_AGO, SIXTEEN_DAYS_AGO
from .utils import touch


@pytest.fixture(scope='session')
def check():
    return RebootRequiredCheck('reboot_required', {}, {})


@pytest.fixture(scope='session')
def instance_not_present():
    return {
        'reboot_signal_file': 'reboot-required.should_not_be_present',
        'created_at_file': 'reboot-required.created_at.should_not_be_present',
        'days_warning': 7,
        'days_critical': 14,
    }


@pytest.fixture(scope='session')
def instance_ok():
    with TempDir() as d:
        yield {
            'reboot_signal_file': touch(join(d, 'reboot-required.freshly_minted')),
            'created_at_file': touch(join(d, 'reboot-required.created_at.freshly_minted')),
            'days_warning': 7,
            'days_critical': 14,
        }


@pytest.fixture(scope='session')
def instance_warning():
    with TempDir() as d:
        yield {
            'reboot_signal_file': touch(join(d, 'reboot-required.warning')),
            'created_at_file': touch(
                join(d, 'reboot-required.created_at.warning'), times=(NINE_DAYS_AGO, NINE_DAYS_AGO)
            ),
            'days_warning': 7,
            'days_critical': 14,
        }


@pytest.fixture(scope='session')
def instance_critical():
    with TempDir() as d:
        yield {
            'reboot_signal_file': touch(join(d, 'reboot-required.critical')),
            'created_at_file': touch(
                join(d, 'reboot-required.created_at.critical'), times=(SIXTEEN_DAYS_AGO, SIXTEEN_DAYS_AGO)
            ),
            'days_warning': 7,
            'days_critical': 14,
        }
