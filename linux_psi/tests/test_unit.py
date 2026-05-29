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
    aggregator.assert_metric('psi.system.pressure.cpu.some.avg10', value=0.0, tags=expected_tags)
    aggregator.assert_metric('psi.system.pressure.cpu.some.avg60', value=0.05, tags=expected_tags)
    aggregator.assert_metric('psi.system.pressure.cpu.some.avg300', value=0.12, tags=expected_tags)
    aggregator.assert_metric('psi.system.pressure.cpu.some.total', tags=expected_tags)

    # CPU full (present in this fixture, kernel 5.13+)
    aggregator.assert_metric('psi.system.pressure.cpu.full.avg10', value=0.0, tags=expected_tags)
    aggregator.assert_metric('psi.system.pressure.cpu.full.total', tags=expected_tags)

    # Memory and IO sanity
    aggregator.assert_metric('psi.system.pressure.memory.some.avg300', value=0.0, tags=expected_tags)
    aggregator.assert_metric('psi.system.pressure.io.some.avg10', value=0.18, tags=expected_tags)
    aggregator.assert_metric('psi.system.pressure.io.full.avg60', value=0.09, tags=expected_tags)

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK, tags=expected_tags)


def test_cpu_without_full_line(aggregator, instance, proc_dir):
    """Pre-5.13 kernels: /proc/pressure/cpu has only the `some` line."""
    _copy_fixture('pressure_cpu_no_full', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    check = make_check(instance, str(proc_dir))
    check.check(None)

    # `some` for cpu should still appear
    aggregator.assert_metric('psi.system.pressure.cpu.some.avg10')
    # but `full` should NOT have been emitted
    full_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.cpu.full.')]
    assert full_metrics == [], f'cpu.full.* should not be emitted but got {full_metrics}'

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_pressure_dir_missing(aggregator, instance, tmp_path):
    """Kernel < 4.20 or psi=1 not set: /proc/pressure does not exist."""
    missing = tmp_path / 'definitely_does_not_exist' / 'pressure'
    check = make_check(instance, str(missing))
    check.check(None)

    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.WARNING)
    metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.')]
    assert metrics == [], 'No pressure metrics should be emitted when PSI is unavailable'


def test_one_file_missing(aggregator, instance, proc_dir):
    """If io is restricted (some cgroups), the others should still emit."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    # No io file at all.

    check = make_check(instance, str(proc_dir))
    check.check(None)

    aggregator.assert_metric('psi.system.pressure.cpu.some.avg10', value=0.0)
    aggregator.assert_metric('psi.system.pressure.memory.some.avg10', value=0.0)
    io_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.io.')]
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
    aggregator.assert_metric('psi.system.pressure.io.some.avg60', value=0.09)
    aggregator.assert_metric('psi.system.pressure.io.some.total')
    # The "unrecognized_kind" line should be skipped entirely.
    aggregator.assert_metric('psi.system.pressure.io.full.avg10', value=0.18)
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
        'psi.system.pressure.cpu.some.total',
        metric_type=aggregator.MONOTONIC_COUNT,
    )


def test_procfs_path_override(instance, monkeypatch):
    """Containerized agents pass procfs_path: /host/proc; the check should
    resolve its pressure_dir to /host/proc/pressure."""
    from datadog_checks.linux_psi import check as check_mod

    fake_agent = type(
        'FakeAgent',
        (),
        {
            'get_config': staticmethod(lambda key: '/host/proc' if key == 'procfs_path' else None),
        },
    )()
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
    aggregator.assert_metric('psi.system.pressure.cpu.some.avg10', value=0.0)
    aggregator.assert_metric('psi.system.pressure.io.some.avg10', value=0.18)
    memory_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.memory.')]
    assert memory_metrics == [], f'memory should not have emitted, got {memory_metrics}'
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)


def test_all_files_missing_yields_warning(aggregator, instance, tmp_path):
    """Directory exists but no resource files in it. Should fire WARNING,
    not OK, since nothing useful was collected."""
    pressure = tmp_path / 'empty_pressure'
    pressure.mkdir()

    check = make_check(instance, str(pressure))
    check.check(None)

    psi_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.')]
    assert psi_metrics == [], 'No metrics expected when all resource files are missing'
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.WARNING)


@pytest.mark.parametrize(
    'osrelease,expected',
    [
        ('5.15.0-91-generic\n', ('5.15.0', '5', '15', '0')),
        ('6.5.0\n', ('6.5.0', '6', '5', '0')),
        ('4.4.302+\n', ('4.4.302', '4', '4', '302')),
        ('4.19.0-amd64\n', ('4.19.0', '4', '19', '0')),
    ],
)
def test_kernel_version_metadata_parses(instance, tmp_path, monkeypatch, osrelease, expected):
    """The kernel version metadata should extract major.minor.patch from a
    variety of distro-specific osrelease strings."""
    osrel_dir = tmp_path / 'sys' / 'kernel'
    osrel_dir.mkdir(parents=True)
    (osrel_dir / 'osrelease').write_text(osrelease)

    check = LinuxPSICheck('linux_psi', {}, [instance])
    check._proc_root = str(tmp_path)

    captured = {}
    monkeypatch.setattr(check, 'set_metadata', lambda name, value, **kw: captured.setdefault(name, (value, kw)))

    check._submit_kernel_version()

    version, major, minor, patch = expected
    assert captured['version'][0] == version
    assert captured['version'][1]['scheme'] == 'semver'
    assert captured['version'][1]['part_map'] == {
        'major': major,
        'minor': minor,
        'patch': patch,
    }


def test_kernel_version_metadata_missing_file_is_silent(instance, tmp_path, monkeypatch):
    """If /proc/sys/kernel/osrelease is missing or unreadable, the metadata
    submission should silently no-op (not raise) and not call set_metadata."""
    check = LinuxPSICheck('linux_psi', {}, [instance])
    check._proc_root = str(tmp_path / 'nonexistent')

    called = []
    monkeypatch.setattr(check, 'set_metadata', lambda *a, **kw: called.append((a, kw)))

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
    monkeypatch.setattr(check, 'set_metadata', lambda *a, **kw: called.append((a, kw)))

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

    aggregator.assert_metric('psi.system.pressure.cpu.some.avg10', value=0.0)
    for excluded in ('memory', 'io'):
        leaked = [m for m in aggregator.metric_names if m.startswith(f'psi.system.pressure.{excluded}.')]
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


def _make_cgroup_tree(tmp_path):
    """Build a fake /sys/fs/cgroup v2 layout for tests."""
    root = tmp_path / 'sys' / 'fs' / 'cgroup'
    root.mkdir(parents=True)
    # v2 marker file
    (root / 'cgroup.controllers').write_text('cpu io memory\n')
    # Root-level pressure files (the root cgroup itself)
    (root / 'cpu.pressure').write_text(
        'some avg10=0.10 avg60=0.05 avg300=0.02 total=12345\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n'
    )
    return root


def _make_slice(root, slice_name, services):
    """Create a fake systemd-style slice with N services, each with PSI files."""
    slice_dir = root / slice_name
    slice_dir.mkdir()
    (slice_dir / 'cpu.pressure').write_text(
        'some avg10=1.0 avg60=0.5 avg300=0.1 total=99999\nfull avg10=0.0 avg60=0.0 avg300=0.0 total=0\n'
    )
    for service in services:
        svc = slice_dir / service
        svc.mkdir()
        (svc / 'cpu.pressure').write_text(
            'some avg10=5.0 avg60=3.0 avg300=1.0 total=555555\nfull avg10=2.0 avg60=1.0 avg300=0.5 total=222222\n'
        )
        (svc / 'memory.pressure').write_text(
            'some avg10=0.0 avg60=0.0 avg300=0.0 total=0\nfull avg10=0.0 avg60=0.0 avg300=0.0 total=0\n'
        )
    return slice_dir


def test_cgroup_disabled_by_default(aggregator, instance, proc_dir, tmp_path):
    """When cgroup_roots is empty, no cgroup walking happens and no
    linux_psi.cgroup.can_read service check is emitted."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    check = make_check(instance, str(proc_dir))
    check.check(None)

    cgroup_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.cgroup.')]
    assert cgroup_metrics == []
    # The cgroup service check must not be emitted when the feature is off
    cgroup_scs = aggregator.service_checks('linux_psi.cgroup.can_read')
    assert list(cgroup_scs) == []


def test_cgroup_collects_metrics(aggregator, proc_dir, tmp_path):
    """With cgroup_roots set, the check walks the slice and emits per-cgroup
    metrics with cgroup_path tags."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    _make_slice(cgroup_root, 'system.slice', ['sshd.service', 'postgresql.service'])

    instance = {
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(cgroup_root),
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    # The slice itself should have emitted (it has cpu.pressure)
    aggregator.assert_metric(
        'psi.system.pressure.cgroup.cpu.some.avg10',
        value=1.0,
        tags=['cgroup_path:system.slice', 'cgroup_root:system.slice'],
    )
    # And each child service
    aggregator.assert_metric(
        'psi.system.pressure.cgroup.cpu.some.avg10',
        value=5.0,
        tags=['cgroup_path:system.slice/sshd.service', 'cgroup_root:system.slice'],
    )
    aggregator.assert_metric(
        'psi.system.pressure.cgroup.cpu.some.avg10',
        value=5.0,
        tags=['cgroup_path:system.slice/postgresql.service', 'cgroup_root:system.slice'],
    )
    aggregator.assert_service_check('linux_psi.cgroup.can_read', status=AgentCheck.OK)


def test_cgroup_v1_host_warns(aggregator, instance, proc_dir, tmp_path):
    """Configured cgroup_roots but no cgroup.controllers file (i.e., a host
    on cgroup v1) should warn cleanly."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    fake_v1_root = tmp_path / 'cgroup_v1_root'
    fake_v1_root.mkdir()  # exists but no cgroup.controllers marker
    (fake_v1_root / 'system.slice').mkdir()

    instance_v1 = {
        **instance,
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(fake_v1_root),
    }
    check = make_check(instance_v1, str(proc_dir))
    check.check(None)

    # Host-level should still be OK
    aggregator.assert_service_check('linux_psi.can_read', status=AgentCheck.OK)
    # Cgroup service check should be WARNING with a v2-related message
    warnings = [sc for sc in aggregator.service_checks('linux_psi.cgroup.can_read') if sc.status == AgentCheck.WARNING]
    assert warnings, 'Expected at least one WARNING service check for cgroup PSI'
    assert 'v2' in warnings[0].message.lower()


def test_cgroup_max_count_breaks_across_multiple_roots(aggregator, proc_dir, tmp_path, caplog):
    """When the cgroup_max_count cap is hit while walking the first root,
    subsequent roots must not be walked at all - and the cap-hit warning
    must be logged exactly once, not per root."""
    import logging

    caplog.set_level(logging.WARNING)

    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    _make_slice(cgroup_root, 'system.slice', ['a.service', 'b.service', 'c.service'])
    _make_slice(cgroup_root, 'user.slice', ['session-1.scope', 'session-2.scope'])

    instance = {
        'cgroup_roots': ['system.slice', 'user.slice'],
        'cgroupfs_path': str(cgroup_root),
        'cgroup_max_count': 1,
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    # At most one cgroup_path tag value should be present across all emitted
    # cgroup metrics (cap is 1)
    cgroup_paths = set()
    for call in aggregator.metrics('psi.system.pressure.cgroup.cpu.some.avg10'):
        for tag in call.tags or ():
            if tag.startswith('cgroup_path:'):
                cgroup_paths.add(tag)
    assert len(cgroup_paths) <= 1, f'cap=1 should yield at most 1 cgroup_path tag value, got {cgroup_paths}'

    # And the cap-hit warning must be logged exactly once
    cap_warnings = [r for r in caplog.records if 'cgroup_max_count' in r.getMessage()]
    assert len(cap_warnings) == 1, f'expected exactly one cap-hit warning across both roots, got {len(cap_warnings)}'


def test_cgroup_max_count_caps_cardinality(aggregator, proc_dir, tmp_path):
    """When more cgroups exist than cgroup_max_count, the walker stops cleanly."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    # 5 services but cap at 2
    _make_slice(cgroup_root, 'system.slice', ['a.service', 'b.service', 'c.service', 'd.service', 'e.service'])

    instance = {
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(cgroup_root),
        'cgroup_max_count': 2,
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    # Count distinct cgroup_path tags emitted for the cgroup-namespaced metric
    cgroup_paths = set()
    for call in aggregator.metrics('psi.system.pressure.cgroup.cpu.some.avg10'):
        for tag in call.tags or ():
            if tag.startswith('cgroup_path:'):
                cgroup_paths.add(tag)
    assert len(cgroup_paths) <= 2, f'Expected <=2, got {cgroup_paths}'


def test_cgroupfs_path_missing_entirely_warns(aggregator, instance, proc_dir, tmp_path):
    """If the configured cgroupfs_path does not exist at all (distinct from
    'exists but no v2 marker'), the cgroup service check must WARN with a
    clear message and no metrics emit."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    instance_bogus = {
        **instance,
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(tmp_path / 'does_not_exist'),
    }
    check = make_check(instance_bogus, str(proc_dir))
    check.check(None)

    aggregator.assert_service_check('linux_psi.cgroup.can_read', status=AgentCheck.WARNING)
    cgroup_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.cgroup.')]
    assert cgroup_metrics == []


def test_cgroup_root_in_config_does_not_exist_on_disk(aggregator, proc_dir, tmp_path):
    """A user-supplied cgroup_roots entry that simply does not exist on the
    host (e.g., 'kubepods.slice' on a host without k8s) is logged at debug
    and skipped silently. The service check stays OK because the rest of the
    feature is working - the host just doesn't have that slice."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    # Build only system.slice; kubepods.slice will be configured but missing

    instance = {
        'cgroup_roots': ['system.slice', 'kubepods.slice'],
        'cgroupfs_path': str(cgroup_root),
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    aggregator.assert_service_check('linux_psi.cgroup.can_read', status=AgentCheck.OK)


def test_walker_skips_scandir_permission_error(aggregator, proc_dir, tmp_path, monkeypatch):
    """When os.scandir raises PermissionError on a cgroup subdirectory, the
    walker must skip cleanly without aborting the whole check run. The root
    cgroup itself should still emit; other roots / siblings should still emit."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    _make_slice(cgroup_root, 'system.slice', ['ok.service'])
    blocked = cgroup_root / 'system.slice' / 'blocked.service'
    blocked.mkdir()
    (blocked / 'cpu.pressure').write_text('some avg10=2.0 avg60=2.0 avg300=2.0 total=2\n')

    real_scandir = os.scandir

    def fake_scandir(path, *args, **kwargs):
        if str(path).endswith('blocked.service'):
            raise PermissionError(13, 'Permission denied', path)
        return real_scandir(path, *args, **kwargs)

    monkeypatch.setattr('os.scandir', fake_scandir)

    instance = {
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(cgroup_root),
        'cgroup_max_depth': 3,
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    # The ok.service emit should still appear
    ok_paths = set()
    for call in aggregator.metrics('psi.system.pressure.cgroup.cpu.some.avg10'):
        for tag in call.tags or ():
            if tag.startswith('cgroup_path:'):
                ok_paths.add(tag)
    assert any('ok.service' in p for p in ok_paths), (
        f'sibling cgroup must still emit despite the PermissionError, got {ok_paths}'
    )
    aggregator.assert_service_check('linux_psi.cgroup.can_read', status=AgentCheck.OK)


def test_emit_cgroup_handles_pressure_file_oserror(aggregator, proc_dir, tmp_path, monkeypatch):
    """If reading one cgroup's pressure file raises a generic OSError
    (e.g., EIO), the check logs and continues to the next resource and
    next cgroup; no exception escapes."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    _make_slice(cgroup_root, 'system.slice', ['svc.service'])

    real_open = open

    def fake_open(path, *args, **kwargs):
        # Make only the cgroup-level cpu.pressure raise EIO; other reads work
        if 'svc.service' in str(path) and str(path).endswith('cpu.pressure'):
            raise OSError(5, 'I/O error', str(path))
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr('builtins.open', fake_open)

    instance = {
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(cgroup_root),
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)  # Should not raise

    aggregator.assert_service_check('linux_psi.cgroup.can_read', status=AgentCheck.OK)


def test_cgroup_path_tag_is_truncated_at_max_length(aggregator, proc_dir, tmp_path):
    """A pathologically-long cgroup name (or a deeply-nested kubepods path)
    must not produce a tag value longer than the Datadog 200-character limit.
    Truncated tags must end with a sentinel so the truncation is visible."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    slice_dir = cgroup_root / 'system.slice'
    slice_dir.mkdir()
    (slice_dir / 'cpu.pressure').write_text(
        'some avg10=0.0 avg60=0.0 avg300=0.0 total=0\nfull avg10=0.0 avg60=0.0 avg300=0.0 total=0\n'
    )
    # Filename limit on most Linux filesystems is 255 chars. We need the
    # *full* tag (`cgroup_path:system.slice/<name>`) to exceed 200 chars
    # so we nest to produce a long path with short-enough segments.
    deep_a = slice_dir / ('a' * 200 + '.scope')
    deep_a.mkdir()
    (deep_a / 'cpu.pressure').write_text('some avg10=1.0 avg60=1.0 avg300=1.0 total=1\n')
    huge_marker = 'a' * 200

    instance = {
        'cgroup_roots': ['system.slice'],
        'cgroupfs_path': str(cgroup_root),
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    # Find the metric emitted for the huge-name cgroup and verify the
    # cgroup_path tag is bounded.
    for call in aggregator.metrics('psi.system.pressure.cgroup.cpu.some.avg10'):
        for tag in call.tags or ():
            if tag.startswith('cgroup_path:') and huge_marker[:100] in tag:
                # tag includes the 'cgroup_path:' prefix in length
                assert len(tag) <= 200, f'cgroup_path tag exceeds 200 chars: {len(tag)} chars'
                assert tag.endswith('...truncated'), f'truncated tag must end with sentinel: {tag!r}'
                return
    pytest.fail('did not find the huge-name cgroup_path tag among emitted metrics')


def test_cgroup_roots_rejects_non_list(proc_dir):
    """A scalar (non-list) cgroup_roots should fail with ConfigurationError."""
    from datadog_checks.base import ConfigurationError

    instance = {'cgroup_roots': 'system.slice'}  # string, not list
    with pytest.raises(ConfigurationError, match='list of strings'):
        LinuxPSICheck('linux_psi', {}, [instance])


@pytest.mark.parametrize(
    'bad_root',
    [
        '../etc',
        '..',
        'system.slice/../etc',
        'a/b/../../etc',
    ],
)
def test_cgroup_roots_rejects_parent_traversal(bad_root):
    """Entries containing `..` segments must be rejected at config time
    so a misconfigured conf.yaml cannot escape the cgroupfs root."""
    from datadog_checks.base import ConfigurationError

    instance = {'cgroup_roots': [bad_root]}
    with pytest.raises(ConfigurationError, match='parent-directory'):
        LinuxPSICheck('linux_psi', {}, [instance])


@pytest.mark.parametrize(
    'bad_root',
    [
        '/etc',
        '/sys/fs/cgroup/system.slice',
        '/',
    ],
)
def test_cgroup_roots_rejects_absolute_paths(bad_root):
    """Absolute paths in cgroup_roots must be rejected; the entries are
    interpreted relative to cgroupfs_path and an absolute value implies
    the user is trying to escape that boundary."""
    from datadog_checks.base import ConfigurationError

    instance = {'cgroup_roots': [bad_root]}
    with pytest.raises(ConfigurationError, match='relative'):
        LinuxPSICheck('linux_psi', {}, [instance])


def test_cgroup_root_outside_cgroupfs_is_skipped(aggregator, proc_dir, tmp_path):
    """Even with a clean relative name, if the resolved path escapes
    cgroupfs_path via a symlink the check must skip that root, not
    silently emit metrics for outside content."""
    _copy_fixture('pressure_cpu_normal', proc_dir / 'cpu')
    _copy_fixture('pressure_memory_normal', proc_dir / 'memory')
    _copy_fixture('pressure_io_normal', proc_dir / 'io')

    cgroup_root = _make_cgroup_tree(tmp_path)
    # Create a hostile target outside the cgroupfs root
    hostile_target = tmp_path / 'outside_cgroupfs'
    hostile_target.mkdir()
    (hostile_target / 'cpu.pressure').write_text('some avg10=99.9 avg60=99.9 avg300=99.9 total=99999\n')
    # Symlink a "cgroup root" name to point at it
    (cgroup_root / 'sneaky.slice').symlink_to(hostile_target)

    instance = {
        'cgroup_roots': ['sneaky.slice'],
        'cgroupfs_path': str(cgroup_root),
    }
    check = make_check(instance, str(proc_dir))
    check.check(None)

    # No metrics should have been emitted from outside the cgroupfs root
    cgroup_metrics = [m for m in aggregator.metric_names if m.startswith('psi.system.pressure.cgroup.')]
    assert cgroup_metrics == [], f'Symlink escaping cgroupfs root must not emit metrics; got {cgroup_metrics}'


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
    aggregator.assert_metric('psi.system.pressure.cpu.some.avg10')
    aggregator.assert_metric('psi.system.pressure.memory.some.avg10')
    # Find the CRITICAL service check and confirm the offending path is in the message
    critical = [sc for sc in aggregator.service_checks('linux_psi.can_read') if sc.status == AgentCheck.CRITICAL]
    assert critical, 'Expected at least one CRITICAL service check'
    assert '/io' in critical[0].message
