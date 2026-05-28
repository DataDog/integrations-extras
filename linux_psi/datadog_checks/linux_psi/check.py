# (C) voseghale 2026-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""
Linux PSI (Pressure Stall Information) check.

Reads /proc/pressure/{cpu,memory,io} (Linux kernel 4.20+) and emits per-resource
some/full avg10/avg60/avg300 (gauges, percent) and total (monotonic_count,
microseconds) metrics. Gracefully handles older kernels where /proc/pressure/cpu
does not have a `full` line (added in kernel 5.13) or where PSI is not enabled
at all (boot parameter `psi=1` not set).

The check namespace is `system.pressure.` to slot alongside Datadog's existing
`system.*` Linux metrics (cpu, memory, io, processes).

See https://docs.kernel.org/accounting/psi.html for the kernel feature.
"""
from __future__ import annotations

import os
import re

from datadog_checks.base import AgentCheck, ConfigurationError

try:
    # Available inside the Agent runtime; not in unit tests on a bare interpreter.
    import datadog_agent
except ImportError:  # pragma: no cover - exercised only by Agent runtime
    datadog_agent = None


PRESSURE_FILES = ('cpu', 'memory', 'io')
VALID_KINDS = ('some', 'full')
AVG_KEYS = ('avg10', 'avg60', 'avg300')

HOST_NAMESPACE = 'system.pressure'
CGROUP_NAMESPACE = 'system.pressure.cgroup'

DEFAULT_CGROUPFS_PATH = '/sys/fs/cgroup'
DEFAULT_CGROUP_MAX_DEPTH = 2
DEFAULT_CGROUP_MAX_COUNT = 200

# Datadog tag values longer than this get truncated by the backend anyway;
# truncating in-band with a visible sentinel keeps the truncation auditable
# and avoids the silent backend cut.
TAG_VALUE_MAX_LENGTH = 200
TAG_TRUNCATION_SENTINEL = '...truncated'

# Matches major.minor.patch at the start of /proc/sys/kernel/osrelease.
# The string typically looks like '5.15.0-91-generic' or '6.5.0' or '4.4.302+'.
KERNEL_VERSION_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)')


class LinuxPSICheck(AgentCheck):
    """Read /proc/pressure/* (host) and optionally /sys/fs/cgroup/.../*.pressure
    (per-cgroup) and emit PSI metrics."""

    SERVICE_CHECK_NAME = 'linux_psi.can_read'
    CGROUP_SERVICE_CHECK_NAME = 'linux_psi.cgroup.can_read'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = list(self.instance.get('tags', []))
        self._resources = self._resolve_resources()
        self._set_paths()
        self._setup_cgroup_config()

    def _resolve_resources(self):
        """Return the tuple of PSI resources to collect for this instance.
        Defaults to all three; user can restrict via the `resources` config."""
        configured = self.instance.get('resources')
        if not configured:
            return PRESSURE_FILES
        invalid = [r for r in configured if r not in PRESSURE_FILES]
        if invalid:
            raise ConfigurationError(
                f'Unknown PSI resource(s) {invalid!r} in `resources` config. '
                f'Allowed values: {list(PRESSURE_FILES)}'
            )
        # Preserve user ordering, deduplicate.
        seen = set()
        result = []
        for r in configured:
            if r not in seen:
                seen.add(r)
                result.append(r)
        return tuple(result)

    def _set_paths(self):
        """Resolve the procfs root and the pressure directory, honoring the
        Agent's procfs_path config so container deployments that mount /proc
        at /host/proc work out of the box."""
        proc_location = '/proc'
        if datadog_agent is not None:
            configured = datadog_agent.get_config('procfs_path')
            if configured:
                proc_location = configured
        self._proc_root = proc_location.rstrip('/')
        self.pressure_dir = os.path.join(self._proc_root, 'pressure')

    def _setup_cgroup_config(self):
        """Per-cgroup PSI is opt-in. If `cgroup_roots` is empty/missing, no
        cgroup walking happens. When set, walk each named root under
        `cgroupfs_path` up to `cgroup_max_depth` levels deep, emitting metrics
        for at most `cgroup_max_count` cgroups per run.

        Validates each cgroup_roots entry against path-traversal patterns
        (parent-directory references, absolute paths) so a misconfigured
        conf.yaml cannot make the check read directories outside the
        cgroupfs root. A second check at walk time (`_is_within_cgroupfs`)
        defends against symlinks under the cgroupfs root that point outside.
        """
        roots = self.instance.get('cgroup_roots') or []
        if not isinstance(roots, (list, tuple)):
            raise ConfigurationError(
                '`cgroup_roots` must be a list of strings, got {!r}'.format(type(roots).__name__)
            )
        validated = []
        for r in roots:
            s = str(r).strip()
            if os.path.isabs(s):
                raise ConfigurationError(
                    f'cgroup_roots entries must be relative paths under cgroupfs_path, '
                    f'got absolute path: {s!r}'
                )
            # Normalize separators and check each segment for parent-directory references.
            segments = [seg for seg in s.replace('\\', '/').split('/') if seg]
            if '..' in segments:
                raise ConfigurationError(
                    f'cgroup_roots entries cannot contain parent-directory references (..), '
                    f'got: {s!r}'
                )
            validated.append(s)
        self._cgroup_roots = tuple(validated)
        self._cgroupfs_path = self.instance.get('cgroupfs_path', DEFAULT_CGROUPFS_PATH)
        self._cgroup_max_depth = int(self.instance.get('cgroup_max_depth', DEFAULT_CGROUP_MAX_DEPTH))
        self._cgroup_max_count = int(self.instance.get('cgroup_max_count', DEFAULT_CGROUP_MAX_COUNT))

    def _truncate_tag(self, key, value):
        """Build a `key:value` tag, truncating the value with a visible
        sentinel if the full tag would exceed TAG_VALUE_MAX_LENGTH."""
        tag = f'{key}:{value}'
        if len(tag) <= TAG_VALUE_MAX_LENGTH:
            return tag
        # Reserve room for the sentinel and rebuild
        keep = TAG_VALUE_MAX_LENGTH - len(TAG_TRUNCATION_SENTINEL)
        return tag[:keep] + TAG_TRUNCATION_SENTINEL

    def _is_within_cgroupfs(self, path):
        """Resolve symlinks and confirm `path` is at or below cgroupfs_path.
        Returns True if safe, False if the resolved path escapes."""
        try:
            real_path = os.path.realpath(path)
            real_base = os.path.realpath(self._cgroupfs_path)
        except OSError:
            return False
        if real_path == real_base:
            return True
        return real_path.startswith(real_base + os.sep)

    @AgentCheck.metadata_entrypoint
    def _submit_kernel_version(self):
        """Surface the running kernel version as integration metadata so it
        appears in the tile's Integration metadata. Useful for fleet-wide
        audits like 'how many hosts are on a kernel that supports cpu.full
        PSI?' (added in 5.13)."""
        osrelease_path = os.path.join(self._proc_root, 'sys/kernel/osrelease')
        try:
            with open(osrelease_path, 'r') as f:
                raw = f.read().strip()
        except OSError as e:
            self.log.debug('Could not read kernel version from %s: %s',
                           osrelease_path, e)
            return

        m = KERNEL_VERSION_RE.match(raw)
        if not m:
            self.log.debug('Unexpected kernel version format: %r', raw)
            return
        major, minor, patch = m.groups()
        version = f'{major}.{minor}.{patch}'
        self.set_metadata(
            'version', version,
            scheme='semver',
            part_map={'major': major, 'minor': minor, 'patch': patch},
        )

    def check(self, _):
        self._submit_kernel_version()
        self._check_system_pressure()
        if self._cgroup_roots:
            self._check_cgroup_pressure()

    def _check_system_pressure(self):
        """Read /proc/pressure/* and emit host-level metrics + service check."""
        if not os.path.isdir(self.pressure_dir):
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.WARNING,
                tags=self.tags,
                message=(
                    'PSI is not enabled on this kernel. PSI requires Linux 4.20+ '
                    'and the kernel must be booted with `psi=1` if the distro '
                    'disables it by default. See the integration README for '
                    'enabling it.'
                ),
            )
            return

        emitted = False
        worst_status = AgentCheck.OK
        worst_message = ''
        for resource in self._resources:
            path = os.path.join(self.pressure_dir, resource)
            try:
                self._read_one(resource, path)
                emitted = True
            except FileNotFoundError:
                # One of the three may be missing on some kernels (e.g. io
                # in restricted cgroups). Not an error overall.
                self.log.debug('PSI file not found: %s', path)
            except PermissionError as e:
                worst_status = AgentCheck.CRITICAL
                worst_message = f'Permission denied reading {path}: {e}'
            except OSError as e:
                # Soft-fail on other IO errors; report them but keep going.
                self.log.warning('Error reading %s: %s', path, e)

        if worst_status == AgentCheck.CRITICAL:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL,
                               tags=self.tags, message=worst_message)
        elif emitted:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK,
                               tags=self.tags)
        else:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.WARNING,
                tags=self.tags,
                message='No PSI files could be read; nothing emitted.',
            )

    def _read_one(self, resource, path, namespace=HOST_NAMESPACE, tags=None):
        """Open one PSI file and emit each line's metrics under `namespace`,
        tagged with `tags`. Used by both host-level and per-cgroup paths."""
        if tags is None:
            tags = self.tags
        with open(path, 'r') as f:
            for line in f:
                self._emit_line(resource, line.strip(), namespace=namespace, tags=tags)

    def _emit_line(self, resource, line, namespace=HOST_NAMESPACE, tags=None):
        """Parse a line like:
            'some avg10=0.18 avg60=0.09 avg300=0.04 total=294183'
        and emit one metric per field under `<namespace>.<resource>.<kind>.<key>`,
        tagged with `tags`.
        """
        if tags is None:
            tags = self.tags
        if not line:
            return
        parts = line.split()
        if not parts:
            return
        kind = parts[0]
        if kind not in VALID_KINDS:
            self.log.debug('Skipping unknown PSI line for %s: %s', resource, line)
            return
        metric_prefix = f'{namespace}.{resource}.{kind}'
        for field in parts[1:]:
            if '=' not in field:
                continue
            key, value = field.split('=', 1)
            try:
                fval = float(value)
            except ValueError:
                self.log.debug('Non-numeric PSI value %s=%s', key, value)
                continue
            if key in AVG_KEYS:
                self.gauge(f'{metric_prefix}.{key}', fval, tags=tags)
            elif key == 'total':
                # `total` is microseconds since boot; emit as monotonic_count
                # so Datadog computes the per-interval rate automatically.
                self.monotonic_count(f'{metric_prefix}.total', fval, tags=tags)
            else:
                self.log.debug('Skipping unknown PSI field %s=%s', key, value)

    def _check_cgroup_pressure(self):
        """Walk the configured cgroup_roots under cgroupfs_path and emit PSI
        for each cgroup that has *.pressure files. Idempotent; cardinality
        bounded by cgroup_max_count."""
        if not os.path.isdir(self._cgroupfs_path):
            self.service_check(
                self.CGROUP_SERVICE_CHECK_NAME, AgentCheck.WARNING,
                tags=self.tags,
                message=(
                    f'cgroup filesystem not found at {self._cgroupfs_path}. '
                    f'cgroup PSI requires cgroup v2; this host appears to be on '
                    f'cgroup v1 or has the filesystem mounted elsewhere. Set '
                    f'`cgroupfs_path` if the mount point is non-standard.'
                ),
            )
            return

        # Quick cgroup v2 sanity check: v2 root has a `cgroup.controllers` file.
        if not os.path.exists(os.path.join(self._cgroupfs_path, 'cgroup.controllers')):
            self.service_check(
                self.CGROUP_SERVICE_CHECK_NAME, AgentCheck.WARNING,
                tags=self.tags,
                message=(
                    'cgroup v2 not detected (cgroup.controllers missing). '
                    'cgroup PSI is only available on the unified cgroup v2 hierarchy.'
                ),
            )
            return

        emitted_count = 0
        cap_hit = False
        for root_name in self._cgroup_roots:
            if cap_hit:
                break
            root_path = os.path.join(self._cgroupfs_path, root_name)
            if not os.path.isdir(root_path):
                self.log.debug('cgroup root not found: %s', root_path)
                continue
            if not self._is_within_cgroupfs(root_path):
                self.log.warning(
                    'cgroup root %s resolves outside cgroupfs_path %s '
                    '(possible symlink escape); skipping',
                    root_path, self._cgroupfs_path,
                )
                continue
            for cgroup_dir, rel_path in self._walk_cgroups(root_path, root_name):
                if emitted_count >= self._cgroup_max_count:
                    self.log.warning(
                        'cgroup_max_count (%d) reached, stopping enumeration. '
                        'Some cgroups will not be reported.',
                        self._cgroup_max_count,
                    )
                    cap_hit = True
                    break
                if self._emit_cgroup(cgroup_dir, rel_path, root_name):
                    emitted_count += 1

        self.service_check(self.CGROUP_SERVICE_CHECK_NAME, AgentCheck.OK,
                           tags=self.tags)

    def _walk_cgroups(self, root_path, root_name, current_depth=0):
        """Yield (absolute_path, relative_path) for the root and each subdirectory
        up to self._cgroup_max_depth levels below the root. The relative path
        is for tagging (e.g., 'system.slice/sshd.service')."""
        # Root cgroup itself
        rel = root_name if current_depth == 0 else None
        if rel is not None:
            yield (root_path, rel)
        if current_depth >= self._cgroup_max_depth:
            return
        try:
            entries = os.scandir(root_path)
        except OSError as e:
            self.log.debug('error scanning %s: %s', root_path, e)
            return
        with entries:
            for entry in entries:
                if not entry.is_dir(follow_symlinks=False):
                    continue
                sub_rel = f'{root_name}/{entry.name}'
                yield (entry.path, sub_rel)
                if current_depth + 1 < self._cgroup_max_depth:
                    yield from self._walk_cgroups_inner(
                        entry.path, sub_rel, current_depth + 1
                    )

    def _walk_cgroups_inner(self, parent_path, parent_rel, current_depth):
        """Inner recursion helper that yields deeper subdirectories already
        beyond the top-level root and its immediate children."""
        try:
            entries = os.scandir(parent_path)
        except OSError as e:
            self.log.debug('error scanning %s: %s', parent_path, e)
            return
        with entries:
            for entry in entries:
                if not entry.is_dir(follow_symlinks=False):
                    continue
                sub_rel = f'{parent_rel}/{entry.name}'
                yield (entry.path, sub_rel)
                if current_depth + 1 < self._cgroup_max_depth:
                    yield from self._walk_cgroups_inner(
                        entry.path, sub_rel, current_depth + 1
                    )

    def _emit_cgroup(self, cgroup_dir, rel_path, root_name):
        """Read this cgroup's PSI files and emit metrics tagged with the
        cgroup path. Returns True if at least one file was read successfully."""
        cgroup_tags = list(self.tags) + [
            self._truncate_tag('cgroup_path', rel_path),
            f'cgroup_root:{root_name}',
        ]
        any_read = False
        for resource in self._resources:
            path = os.path.join(cgroup_dir, f'{resource}.pressure')
            try:
                self._read_one(resource, path,
                               namespace=CGROUP_NAMESPACE, tags=cgroup_tags)
                any_read = True
            except FileNotFoundError:
                # Many cgroups lack one or more pressure files (e.g., a cgroup
                # without an I/O controller). Skip silently.
                continue
            except OSError as e:
                self.log.debug('error reading cgroup PSI %s: %s', path, e)
        return any_read
