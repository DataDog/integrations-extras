# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from datetime import datetime, timedelta
from os import remove, stat, utime
from os.path import isfile
from stat import ST_MTIME

from datadog_checks.base import AgentCheck


class RebootRequiredCheck(AgentCheck):
    REBOOT_SIGNAL_FILE = '/var/run/reboot-required'
    CREATED_AT_FILE = '/var/run/dd-agent/reboot-required.created_at'

    def check(self, instance):
        status, msg = self._check(instance)
        self.service_check('system.reboot_required', status, message=msg)

    def _check(self, instance):
        reboot_signal_file = instance.get('reboot_signal_file', self.REBOOT_SIGNAL_FILE)
        created_at_file = instance.get('created_at_file', self.CREATED_AT_FILE)
        warning_days = int(instance.get('days_warning', 7))
        critical_days = int(instance.get('days_critical', 14))

        return self._get_status(critical_days, warning_days, self._days_since(reboot_signal_file, created_at_file))

    def _days_since(self, reboot_signal_file, created_at_file):
        if isfile(reboot_signal_file):
            if isfile(created_at_file):
                created_at = self._get_created_at(created_at_file)
                return datetime.utcnow() - datetime.utcfromtimestamp(created_at)
            else:
                self._touch(created_at_file)
        elif isfile(created_at_file):
            remove(created_at_file)

        return timedelta()

    def _get_status(self, critical_days, warning_days, deltatime):
        if deltatime.days > critical_days:
            return (
                AgentCheck.CRITICAL,
                'Reboot is critical: security patches applied {} days ago'.format(deltatime.days),
            )
        elif deltatime.days > warning_days:
            return (
                AgentCheck.WARNING,
                'Reboot is necessary; security patches applied {} days ago'.format(deltatime.days),
            )
        else:
            return AgentCheck.OK, None

    def _get_created_at(self, fname):
        file_stat = stat(fname)
        created_at = file_stat[ST_MTIME]
        return created_at

    def _touch(self, fname, times=None):
        with open(fname, 'a'):
            utime(fname, times)
