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


def test_procfs_path_override(instance, monkeypatch):
    """Containerized agents pass procfs_path: /host/proc; the check should
    resolve its pressure_dir to /host/proc/pressure."""
    from datadog_checks.linux_psi import check as check_mod

    fake_agent = type('FakeAgent', (), {
        'get_config': staticmethod(lambda key: '/host/proc' if key == 'procfs_path' else None),
    })()
    monkeypatch.setattr(check_mod, 'datadog_agent', fake_agent)

    c = LinuxPSICheck('linux_psi', {}, [instance])
    assert c.pressure_dir == '/host/proc/pressure'


def test_os_error_is_soft_failed(aggregator, instance, proc_dir, monkeypatch):
    """A generic OSError (e.g. EIO mid-read) on one file is logged but does
    not crash the check; other resources keep emitting and the service check
    stays OK if at least one file succeeded."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    real_open = open

    def fake_open(path, *args, **kwargs):
        if str(path).endswith('/memory'):
            raise OSError(5, 'I/O error', path)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr('builtins.open', fake_open)

    check = make_check(instance, str(proc_dir))
    check.check(None)

    # cpu and io should still have emitted; memory should have nothing.
    aggregator.assert_metric('system.pressure.cpu.some.avg10', value=0.0)
    aggregator.assert_metric('system.pressure.io.some.avg10', value=0.18)
    memory_metrics = [m for m in aggregator.metric_names if m.startswith('system.pressure.memory.')]
    assert memory_metrics == [], f'memory should not have emitted, got {memory_metrics}'
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_all_files_missing_yields_warning(aggregator, instance, tmp_path):
    """Directory exists but no resource files in it. Should fire WARNING,
    not OK, since nothing useful was collected."""
    pressure = tmp_path / 'empty_pressure'
    pressure.mkdir()

    check = make_check(instance, str(pressure))
    check.check(None)

    psi_metrics = [m for m in aggregator.metric_names if m.startswith('system.pressure.')]
    assert psi_metrics == [], 'No metrics expected when all resource files are missing'
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.WARNING)


@pytest.mark.parametrize('osrelease,expected', [
    ('5.15.0-91-generic\n', ('5.15.0', '5', '15', '0')),
    ('6.5.0\n',             ('6.5.0', '6', '5', '0')),
    ('4.4.302+\n',          ('4.4.302', '4', '4', '302')),
    ('4.19.0-amd64\n',      ('4.19.0', '4', '19', '0')),
])
def test_kernel_version_metadata_parses(instance, tmp_path, monkeypatch,
                                          osrelease, expected):
    """The kernel version metadata should extract major.minor.patch from a
    variety of distro-specific osrelease strings."""
    osrel_dir = tmp_path / 'sys' / 'kernel'
    osrel_dir.mkdir(parents=True)
    (osrel_dir / 'osrelease').write_text(osrelease)

    check = LinuxPSICheck('linux_psi', {}, [instance])
    check._proc_root = str(tmp_path)

    captured = {}
    monkeypatch.setattr(check, 'set_metadata',
                        lambda name, value, **kw: captured.setdefault(name, (value, kw)))

    check._submit_kernel_version()

    version, major, minor, patch = expected
    assert captured['version'][0] == version
    assert captured['version'][1]['scheme'] == 'semver'
    assert captured['version'][1]['part_map'] == {
        'major': major, 'minor': minor, 'patch': patch,
    }


def test_kernel_version_metadata_missing_file_is_silent(instance, tmp_path, monkeypatch):
    """If /proc/sys/kernel/osrelease is missing or unreadable, the metadata
    submission should silently no-op (not raise) and not call set_metadata."""
    check = LinuxPSICheck('linux_psi', {}, [instance])
    check._proc_root = str(tmp_path / 'nonexistent')

    called = []
    monkeypatch.setattr(check, 'set_metadata',
                        lambda *a, **kw: called.append((a, kw)))

    check._submit_kernel_version()
    assert called == []


def test_kernel_version_metadata_garbled_is_silent(instance, tmp_path, monkeypatch):
    """A malformed osrelease (no major.minor.patch prefix) should be skipped."""
    osrel_dir = tmp_path / 'sys' / 'kernel'
    osrel_dir.mkdir(parents=True)
    (osrel_dir / 'osrelease').write_text('totally not a version\n')

    check = LinuxPSICheck('linux_psi', {}, [instance])
    check._proc_root = str(tmp_path)

    called = []
    monkeypatch.setattr(check, 'set_metadata',
                        lambda *a, **kw: called.append((a, kw)))

    check._submit_kernel_version()
    assert called == []


def test_resources_config_filters_collection(aggregator, proc_dir):
    """When the user sets `resources: [cpu]`, only cpu metrics emit and the
    other resource files are not even opened."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    instance = {'tags': ['integration:linux_psi_test'], 'resources': ['cpu']}
    check = make_check(instance, str(proc_dir))
    check.check(None)

    aggregator.assert_metric('system.pressure.cpu.some.avg10', value=0.0)
    for excluded in ('memory', 'io'):
        leaked = [m for m in aggregator.metric_names
                  if m.startswith(f'system.pressure.{excluded}.')]
        assert leaked == [], f'{excluded} should not have emitted, got {leaked}'
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_resources_config_rejects_unknown(proc_dir):
    """An unknown resource name should fail check construction with a clear
    ConfigurationError, not silently degrade."""
    from datadog_checks.base import ConfigurationError

    instance = {'resources': ['cpu', 'gpu', 'network']}
    with pytest.raises(ConfigurationError, match=r'gpu.*network'):
        LinuxPSICheck('linux_psi', {}, [instance])


def test_resources_config_preserves_order_and_dedups(proc_dir):
    """User ordering is preserved and duplicates are silently removed."""
    instance = {'resources': ['memory', 'io', 'cpu', 'memory']}
    check = LinuxPSICheck('linux_psi', {}, [instance])
    assert check._resources == ('memory', 'io', 'cpu')


def test_multi_file_permission_denied_is_critical(aggregator, instance, proc_dir, monkeypatch):
    """When some files read OK but others raise PermissionError, the service
    check should still be CRITICAL (worst observed status wins) and the
    message should point at the offending file."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    real_open = open

    def fake_open(path, *args, **kwargs):
        if str(path).endswith('/io'):
            raise PermissionError(13, 'Permission denied', path)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr('builtins.open', fake_open)

    check = make_check(instance, str(proc_dir))
    check.check(None)

    # cpu and memory emitted; the service check is CRITICAL because io was denied
    aggregator.assert_metric('system.pressure.cpu.some.avg10')
    aggregator.assert_metric('system.pressure.memory.some.avg10')
    # Find the CRITICAL service check and confirm the offending path is in the message
    critical = [sc for sc in aggregator.service_checks('linux_psi.can_read')
                if sc.status == AgentCheck.CRITICAL]
    assert critical, 'Expected at least one CRITICAL service check'
    assert '/io' in critical[0].message
