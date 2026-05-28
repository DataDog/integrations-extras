# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""
Unit tests for the linux_psi check.

These tests do not require Linux because each test points the check at a
test-controlled directory full of fixture files. The check reads them with
plain `open()` and behaves identically to reading /proc/pressure on a real host.
"""
import os
import shutil

import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.linux_psi import LinuxPSICheck

from .common import fixture_path


def make_check(instance, pressure_dir):
    """Build a check whose pressure_dir points at the given directory."""
    check = LinuxPSICheck('linux_psi', {}, [instance])
    check.pressure_dir = pressure_dir
    return check


@pytest.fixture
def proc_dir(tmp_path):
    """Create a fake /proc/pressure/ directory with the three resource files."""
    d = tmp_path / 'pressure'
    d.mkdir()
    return d


def _copy_fixture(src_name, dest_path):
    shutil.copy(fixture_path(src_name), dest_path)


def test_full_happy_path(aggregator, instance, proc_dir):
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    check = make_check(instance, str(proc_dir))
    check.check(None)

    expected_tags = ['integration:linux_psi_test']

    # CPU some
    aggregator.assert_metric('system.pressure.cpu.some.avg10', value=0.0, tags=expected_tags)
    aggregator.assert_metric('system.pressure.cpu.some.avg60', value=0.05, tags=expected_tags)
    aggregator.assert_metric('system.pressure.cpu.some.avg300', value=0.12, tags=expected_tags)
    aggregator.assert_metric('system.pressure.cpu.some.total', tags=expected_tags)

    # CPU full (present in this fixture, kernel 5.13+)
    aggregator.assert_metric('system.pressure.cpu.full.avg10', value=0.0, tags=expected_tags)
    aggregator.assert_metric('system.pressure.cpu.full.total', tags=expected_tags)

    # Memory and IO sanity
    aggregator.assert_metric('system.pressure.memory.some.avg300', value=0.0, tags=expected_tags)
    aggregator.assert_metric('system.pressure.io.some.avg10', value=0.18, tags=expected_tags)
    aggregator.assert_metric('system.pressure.io.full.avg60', value=0.09, tags=expected_tags)

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK, tags=expected_tags)


def test_cpu_without_full_line(aggregator, instance, proc_dir):
    """Pre-5.13 kernels: /proc/pressure/cpu has only the `some` line."""
    _copy_fixture('pressure_cpu_no_full', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    check = make_check(instance, str(proc_dir))
    check.check(None)

    # `some` for cpu should still appear
    aggregator.assert_metric('system.pressure.cpu.some.avg10')
    # but `full` should NOT have been emitted
    full_metrics = [m for m in aggregator.metric_names if m.startswith('system.pressure.cpu.full.')]
    assert full_metrics == [], f'cpu.full.* should not be emitted but got {full_metrics}'

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_pressure_dir_missing(aggregator, instance, tmp_path):
    """Kernel < 4.20 or psi=1 not set: /proc/pressure does not exist."""
    missing = tmp_path / 'definitely_does_not_exist' / 'pressure'
    check = make_check(instance, str(missing))
    check.check(None)

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.WARNING)
    metrics = [m for m in aggregator.metric_names if m.startswith('system.pressure.')]
    assert metrics == [], 'No pressure metrics should be emitted when PSI is unavailable'


def test_one_file_missing(aggregator, instance, proc_dir):
    """If io is restricted (some cgroups), the others should still emit."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    # No io file at all.

    check = make_check(instance, str(proc_dir))
    check.check(None)

    aggregator.assert_metric('system.pressure.cpu.some.avg10', value=0.0)
    aggregator.assert_metric('system.pressure.memory.some.avg10', value=0.0)
    io_metrics = [m for m in aggregator.metric_names if m.startswith('system.pressure.io.')]
    assert io_metrics == [], 'No io metrics expected when /proc/pressure/io is missing'
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_permission_denied(aggregator, instance, proc_dir, monkeypatch):
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    real_open = open

    def fake_open(path, *args, **kwargs):
        if str(path).endswith('/cpu'):
            raise PermissionError(13, 'Permission denied', path)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr('builtins.open', fake_open)

    check = make_check(instance, str(proc_dir))
    check.check(None)

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.CRITICAL)


def test_malformed_line_is_ignored(aggregator, instance, proc_dir):
    """Garbage values are skipped without raising. Other valid fields still emit."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_malformed', proc_dir / 'io')

    check = make_check(instance, str(proc_dir))
    check.check(None)

    # The malformed `some avg10=garbage` should NOT have emitted that metric.
    aggregator.assert_metric('system.pressure.io.some.avg60', value=0.09)
    aggregator.assert_metric('system.pressure.io.some.total')
    # The "unrecognized_kind" line should be skipped entirely.
    aggregator.assert_metric('system.pressure.io.full.avg10', value=0.18)
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_total_emits_as_monotonic_count(aggregator, instance, proc_dir):
    """The `total` field should be a count (rate-able), not a gauge."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    check = make_check(instance, str(proc_dir))
    check.check(None)

    # If a metric is asserted, the aggregator knows its type. The total metrics
    # must show up as MONOTONIC_COUNT, not GAUGE.
    aggregator.assert_metric(
        'system.pressure.cpu.some.total',
        metric_type=aggregator.MONOTONIC_COUNT,
    )
