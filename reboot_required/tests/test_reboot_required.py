from datadog_checks.checks import AgentCheck

from os import utime, remove
from os.path import join, isfile
from tempfile import gettempdir
from datetime import datetime, timedelta
from time import mktime
import pytest


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

def test_test():
    assert True is True
