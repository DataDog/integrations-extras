# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""
Integration tests for linux_psi. These read the real /proc/pressure/* on the
host running the tests and are skipped on non-Linux platforms or when PSI is
not enabled on the kernel.
"""
import os
import sys

import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.linux_psi import LinuxPSICheck


PSI_PATH = '/proc/pressure'

pytestmark = [
    pytest.mark.skipif(sys.platform != 'linux', reason='PSI is Linux-only'),
    pytest.mark.skipif(not os.path.isdir(PSI_PATH),
                       reason='PSI not enabled on this kernel (psi=1 boot param missing?)'),
    pytest.mark.integration,
]


def test_real_psi(aggregator, instance):
    check = LinuxPSICheck('linux_psi', {}, [instance])
    check.check(None)

    # On any PSI-enabled system, cpu.some.avg10 will be emitted, even if 0.
    aggregator.assert_metric('system.pressure.cpu.some.avg10')
    aggregator.assert_metric('system.pressure.cpu.some.total',
                             metric_type=aggregator.MONOTONIC_COUNT)
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)
